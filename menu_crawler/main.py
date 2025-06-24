from crawlers.naver import get_naver_menu_image_url
from crawlers.kakao import get_kakao_menu_image_url
from crawlers.kakao_2 import get_kakao_2_menu_image_url
from utils.storage import load_last_urls, save_last_urls, is_new_url
from utils.date_utils import get_today_date_string
from utils.logger import logger
from datetime import datetime, timedelta, timezone
from utils.image import save_image_from_url
from utils.ocr import ocr_from_image

KST = timezone(timedelta(hours=9))

def main():
    logger.info(f"[System] 오늘 날짜: {get_today_date_string(KST)}\n")

    now = datetime.now(KST)
    now_str = now.strftime("%Y-%m-%d %H:%M")
    # today_date = now.strftime("%Y-%m-%d")

    last_urls = load_last_urls()
    updated = {}

    kakao_result = ""
    naver_result = ""
    kakao_2_result = ""

    # IMAGE_PATHS = {
    #     "naver": "docs/images/naver.jpg",
    #     "kakao": "docs/images/kakao.jpg",
    #     "kakao_2": "docs/images/kakao_2.jpg"
    # }

    # ==================== 네이버 시작 ====================
    logger.info("=" * 25 + " [네이버 = 옆집] " + "=" * 25)
    naver_url = get_naver_menu_image_url()
    last_urls.setdefault("naver", {})["last_checked"] = now_str

    if naver_url:
        is_new, is_today = is_new_url("naver", naver_url, last_urls)
        if is_new:
            logger.info("[네이버 = 옆집] 새로운 메뉴 이미지 감지됨.")
            updated["naver"] = {"url": naver_url, "saved_date": now_str}
            naver_result = f"[네이버 = 옆집] 2층 이미지 URL: {naver_url}"
            img_path = save_image_from_url(naver_url, "naver")
            if img_path:

                logger.info("[네이버 = 옆집] OCR 시작")
                ocr_result = ocr_from_image(img_path)
                if ocr_result:
                    last_urls["naver"]["ocr"] = {
                        "text": ocr_result,
                        "generated": now_str
                    }
                    logger.info("[네이버 = 옆집] OCR 완료")

        else:
            msg = "[네이버 = 옆집] 오늘 메뉴가 이미 수집됨."
            logger.info(msg)
            naver_result = msg
    else:
            msg = "[네이버 = 옆집] 아직 오늘 메뉴가 올라오지 않음."
            logger.info(msg)
            naver_result = msg

    logger.info("\n")

    # # ==================== 카카오 시작 ====================
    # logger.info("=" * 25 + " [카카오 = 2층] " + "=" * 25)
    # kakao_url = get_kakao_menu_image_url()
    # last_urls.setdefault("kakao", {})["last_checked"] = now_str

    # if kakao_url:
    #     is_new, is_today = is_new_url("kakao", kakao_url, last_urls)
    #     if is_new:
    #         logger.info("[카카오 = 2층] 새로운 메뉴 이미지 감지됨.")
    #         updated["kakao"] = {"url": kakao_url, "saved_date": now_str}
    #         kakao_result = f"[카카오 = 2층] 옆집 이미지 URL: {kakao_url}"
    #         if save_image_from_url(kakao_url, "kakao"):

    #             logger.info("[카카오 = 2층] OCR 시작")
    #             ocr_result = ocr_from_image(IMAGE_PATHS["kakao"])
    #             if ocr_result:
    #                 last_urls["kakao"]["ocr"] = {
    #                     "text": ocr_result,
    #                     "generated": now_str
    #                 }
    #                 logger.info("[카카오 = 2층] OCR 완료")

    #     else:
    #         # if is_today:
    #         #     msg = "[카카오 = 2층] 오늘 메뉴가 이미 수집됨."
    #         # else:
    #         #     msg = "[카카오 = 2층] 아직 오늘 메뉴가 올라오지 않음."

    #         msg = (
    #             "[카카오 = 2층] 오늘 메뉴가 이미 수집됨."
    #             if is_today else "[카카오 = 2층] 아직 오늘 메뉴가 올라오지 않음."
    #         )
    #         logger.info(msg)
    #         kakao_result = msg
    # else:
    #         msg = "[카카오 = 2층] 프로필 사진이 비어 있음."
    #         logger.info(msg)
    #         kakao_result = msg

    # logger.info("\n")


    # # ==================== 카카오_2 시작 ====================
    # logger.info("=" * 23 + " [카카오_2 = 건너집] " + "=" * 23)
    # kakao_2_url = get_kakao_2_menu_image_url()
    # last_urls.setdefault("kakao_2", {})["last_checked"] = now_str

    # if kakao_2_url:
    #     is_new, is_today = is_new_url("kakao_2", kakao_2_url, last_urls)
    #     if is_new:
    #         logger.info("[카카오_2 = 건너집] 새로운 메뉴 이미지 감지됨.")
    #         updated["kakao_2"] = {"url": kakao_2_url, "saved_date": now_str}
    #         kakao_2_result = f"[카카오_2 = 건너집] 2층 이미지 URL: {kakao_2_url}"
    #         if save_image_from_url(kakao_2_url, "kakao_2"):

    #             logger.info("[카카오_2 = 건너집] OCR 시작")
    #             ocr_result = ocr_from_image(IMAGE_PATHS["kakao_2"])
    #             if ocr_result:
    #                 last_urls["kakao_2"]["ocr"] = {
    #                     "text": ocr_result,
    #                     "generated": now_str
    #                 }
    #                 logger.info("[카카오_2 = 건너집] OCR 완료")

    #     else:
    #         msg = "[카카오_2 = 건너집] 오늘 메뉴가 이미 수집됨."
    #         logger.info(msg)
    #         kakao_2_result = msg
    # else:
    #         msg = "[카카오_2 = 건너집] 아직 오늘 메뉴가 올라오지 않음."
    #         logger.info(msg)
    #         kakao_2_result = msg

    # logger.info("\n")


    # 저장
    # 업데이트 된거만 덮어쓰기 (url, saved_date), last_checked 는 항상 수정
    if updated:
        for site, value in updated.items():
            last_urls[site].update(value)

    save_last_urls(last_urls)


    # 결과 요약 출력
    logger.info("-" * 29 + " 상태 요약 " + "-" * 29)
    logger.info(kakao_result)
    logger.info(naver_result)
    logger.info(kakao_2_result)
    logger.info("-" * 69 + "\n")

    logger.info("[System] 크롤링 및 저장 완료")

if __name__ == "__main__":
    main()
