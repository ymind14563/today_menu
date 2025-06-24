from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageEnhance
import logging
import re
import numpy as np 
import cv2

# 로그 레벨 ERROR 이상만 출력
logging.getLogger().setLevel(logging.ERROR)

# PaddleOCR 객체 초기화
# - use_angle_cls=True: 글자 회전 보정
# - lang='korean': 한국어 OCR
# - use_gpu=False: CPU 사용
ocr = PaddleOCR(use_angle_cls=True, lang='korean', use_gpu=False)

# 이미지 전처리 (흑백, 대비 증가)
def ocr_from_image(image_path):

    # 흑백, 대비 증가
    img = Image.open(image_path).convert("L")  # 그레이스케일
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)  # 대비 2배 증가
    img = np.array(img) # PIL 이미지를 numpy 배열로 변환 (PIL로 전처리해서 생긴 상황)

    # OCR 수행 결과
    result = ocr.ocr(img, cls=True)


    print("/////////////////이미지 후처리 전 OCR 결과/////////////////")
    for line in result[0]:
        coords, (text, conf) = line
        print(f"[{text}] (conf: {conf:.3f}) → {coords}")

    # OCR 박스 시각화
    save_ocr_boxes_image(image_path, result)


    # 텍스트 박스가 1개만 감지된 경우
    # 이미지 전체가 하나의 박스(메뉴판 전체를 하나의 블록으로 본 경우)
    if len(result[0]) == 1:
        # result[0]: 텍스트 박스들의 리스트 (1개 이상의 박스)
        # result[0][0]: 첫 번째 박스 (tuple 구조)
        # result[0][0][1]: (text, confidence) 튜플
        # result[0][0][1][0]: text 값만 추출한 것 (실제 글자 내용)
        return clean_ocr_text(result[0][0][1][0]) # 후처리 반영한 텍스트를 리턴해야함
        # single_line = [result[0][0]]  # 1개짜리 박스를 리스트로 묶음
        # clustered = cluster_text_by_lines(single_line)
        # return clean_ocr_text("\n".join(clustered))

    # 텍스트 박스가 여러 개 감지된 경우
    # 왼쪽과 오른쪽에 텍스트가 분리되어 있는 구조
    # result[0][0]이 왼쪽 박스를 의미하는 보장은 없음 = 좌표 순 정렬을 보장하지 않음
    # result[0] 전체를 print()로 확인해봐도 좌표 순서가 불규칙적인 걸 볼 수 있음
    # 그래서 방법은 박스의 x좌표 기반 필터링뿐
    else:

        # 현재 img는 numpy.ndarray라서 .width 없음
        # img_width = img.width

        # numpy 배열의 shape는 (높이, 너비)이므로, [1]이 너비(width)를 의미함
        img_width = img.shape[1]

        left_texts = []

        for line in result[0]:
            coords, (text, conf) = line

            # 각 텍스트 박스의 4개 꼭짓점 좌표 중 x 좌표만 평균 계산
            x_avg = sum([pt[0] for pt in coords]) / 4

            # 평균 x 좌표가 이미지 너비의 절반보다 왼쪽이면 선택 
            # 사진이 매일 정확히 절반이 아니므로 주석 처리함
            # if x_avg < img_width * 0.6:
            #     left_texts.append((coords, (text, conf)))

        # Y 좌표 기준 군집화 후 줄 단위 병합
        clustered = cluster_text_by_lines(left_texts)
        clustered = cluster_text_by_lines(result[0])

        print("/////////////////이미지 전처리 결과/////////////////")
        print(result[0])

        # 왼쪽 텍스트들만 줄바꿈 포함하여 반환
        final_text = clean_ocr_text("\n".join(clustered))
        print("/////////////////최종 이미지 처리 결과/////////////////")
        print(final_text)

        return final_text






# ocr 텍스트 후처리(의미 없는 개행 및 특수문자 제거)
def clean_ocr_text(text: str) -> str:
    # 각 줄 기준으로 처리
    lines = text.splitlines()
    cleaned = []

    skip_keywords = ["모듬야채", "먹고싶은", "료류", "걱정없는한끼", "배터지게", "점심", 
                     "메뉴", "오늘", "밥상", "잡곡밥", "쌀밥", "백미밥", "라면", "탄산음료", 
                     "샐러드", "셀러드", "모듬야채샐러드", "단무지", "포기김치", "겉절이맛김치" ]

    for line in lines:

        # 공백 제거
        line = line.strip().replace(" ", "")

        # 고정 단어 제거
        for keyword in skip_keywords:
            line = line.replace(keyword, "")

        # 잡글자 제거 (앞 뒤 전부)
        line = re.sub(r"^[^가-힣]+|[^가-힣]+$", "", line)

        # 특수문자 제거
        line = re.sub(r"[★●☆※◎◇△▲▼○■□▽◆▶→←↑↓✦※…⊙◎◇◆■□▲△▼▽→←↑↓▶▷◀◁→←↑↓·•○●◎☆★★†‡‰※¤♠♣♥♦♤♧♡♢]", "", line)

        # 너무 짧거나 의미 없는 줄 제거
        if len(line) < 3:
            continue

        cleaned.append(line)

    cleaned = list(dict.fromkeys(cleaned))

    print("/////////////////이미지 후처리 결과/////////////////")
    print("\n".join(cleaned))
    return "\n".join(cleaned)


# y좌표 기준으로 클러스터링
def cluster_text_by_lines(result_lines, y_thresh=25):
    clusters = []

    for line in result_lines:
        coords, (text, conf) = line
        y_center = sum([pt[1] for pt in coords]) / 4

        inserted = False
        for cluster in clusters:
            if abs(cluster['y'] - y_center) < y_thresh:
                cluster['lines'].append((coords, text, conf))
                inserted = True
                break

        if not inserted:
            clusters.append({'y': y_center, 'lines': [(coords, text, conf)]})

    # 각 cluster 안에서 x좌표 기준 정렬 후 confidence 0.6 이상만 병합
    merged = []
    for cluster in sorted(clusters, key=lambda x: x['y']):
        sorted_line = sorted(cluster['lines'], key=lambda x: sum(pt[0] for pt in x[0]) / 4)
        merged_text = ' '.join(
            text for _, text, conf in sorted_line
            if conf >= 0.6 and re.search(r"[가-힣]{2,}", text)
        )

        # 한글 단어 2개 이상 포함된 줄만 필터
        if len(re.findall(r"[가-힣]{2,}", merged_text)) >= 2:
            merged.append(merged_text)

        
    print("/////////////////Y좌표 병합 결과/////////////////")
    print(merged)
    return merged



# OCR 인식 박스를 이미지에 시각화하여 저장
def save_ocr_boxes_image(image_path, result, output_path="ocr_boxes_only.jpg"):
    # 원본 이미지 (컬러)
    img_color = Image.open(image_path).convert("RGB")

    # draw_ocr용 정보 추출
    boxes = [line[0] for line in result[0]]

    # draw_ocr 실행 (폰트는 기본 경로 사용)
    img_with_boxes = draw_ocr(img_color, boxes, txts=None, scores=None, font_path=None)

    # OpenCV 형식으로 변환 후 저장
    cv2_img = cv2.cvtColor(np.array(img_with_boxes), cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, cv2_img)




# ocr만 바로 실행할 때 사용
if __name__ == "__main__":
    image_path = r"C:\PROJECTS\today_menu\docs\images\naver.jpg"
    ocr_from_image(image_path)
