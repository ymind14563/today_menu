from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageEnhance
import cv2, numpy as np, re, logging, sys
from sklearn.cluster import KMeans

# ───────────── 설정 ─────────────
logging.getLogger().setLevel(logging.ERROR)
ocr = PaddleOCR(use_angle_cls=True, lang='korean', use_gpu=False)
HEADER = re.compile(r"^(점심|오늘의|메뉴|샐러드|밥상)$")
MIN_CONF, GAP_X, GAP_Y = 0.80, 15, 0.7

# ───────────── 전처리 + OCR ─────────────
def ocr_from_image(img_path: str) -> list[str]:
    img = Image.open(img_path).convert("L")
    img = cv2.medianBlur(np.array(img), 3)
    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    img = ImageEnhance.Sharpness(Image.fromarray(img)).enhance(2.0)
    img = ImageEnhance.Brightness(img).enhance(1.2)
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img_np = np.array(img)

    res = ocr.ocr(img_np, cls=False)[0]
    print("/////////////////RAW OCR/////////////////")
    for b,(t,c) in res:
        print(f"[{t}] ({c:.3f}) → {b}")

    # ─ 왼쪽 영역 추출 ─
    mids = np.array([[np.mean([p[0] for p in b])] for b,_ in res])
    lbl  = KMeans(n_clusters=2, n_init=10).fit_predict(mids)
    left = np.argmin([mids[lbl==i].mean() for i in (0,1)])
    left_res = [r for r,l in zip(res,lbl) if l==left]
    print("/////////////////LEFT FILTER/////////////////")
    for b,(t,c) in left_res: print(f"[{t}] ({c:.3f})")

    # ─ 기본 필터 ─
    cand=[]
    heights=[] # 글자높이 수집용

    STOP_LINES = ["싱싱한", "모듬야채", "먹고싶은", "걱정없는한끼", "배터지게", "점심", 
                    "메뉴", "오늘", "밥상", "잡곡밥", "쌀밥", "백미밥", "라면", "탄산음료", 
                    "샐러드", "셀러드", "모듬야채샐러드", "단무지", "포기김치", "겉절이맛김치" ]


    for box,(txt,conf) in left_res:
        if conf < MIN_CONF or HEADER.match(txt):          continue
        txt2 = re.sub(r"[^가-힣\s]", "", txt).lstrip("*")  # 특수문자, 별 제거
        if not re.search(r"[가-힣]{2,}", txt2):        continue

        heights.append(abs(box[3][1]-box[0][1])) # 높이 기록
        xc,yc = np.mean([p[0] for p in box]), np.mean([p[1] for p in box])

        if txt2 in STOP_LINES:     continue
        cand.append((yc, xc, txt2))

    if not cand:
        print("후보 없음 ― 파라미터 조정 필요")
        return []

    h_mean = np.mean(heights)    # 평균 높이 산출


    print("/////////////////CLEAN CANDIDATE/////////////////")
    for _,_,t in cand: print(t)

    # ─ 줄 병합 ─
    cand.sort(key=lambda v:v[0])
    lines, cur, y_prev = [], [], None
    for y,x,t in cand:
        if y_prev is None or y - y_prev < h_mean*GAP_Y:
            cur.append((x,t))
        else:
            lines.append(_merge(cur)); cur=[(x,t)]
        y_prev = y
    if cur: lines.append(_merge(cur))

    #  중복 제거·좌우 공백 제거 후 선두 9행
    lines = list(dict.fromkeys(l.strip() for l in lines))[:9]

    print("/////////////////MERGED LINE/////////////////")
    # for l in lines: print(l) # 줄바꿈
    formatted = " / ".join(lines)  # 리스트를 슬래시로 연결
    print(formatted)  # 한 줄로 출력
    return lines   

def _merge(arr):
    arr.sort(key=lambda v:v[0])
    parts, px = [], None
    for x,t in arr:
        if px is not None and x - px > GAP_X:
            parts.append(" ")
        parts.append(t); px = x
    return "".join(parts).strip()

# ───────────── 실행 ─────────────
if __name__ == "__main__":
    img_path = r"C:\PROJECTS\today_menu\docs\images\naver.jpg" if len(sys.argv)==1 else sys.argv[1]
    ocr_from_image(img_path)
