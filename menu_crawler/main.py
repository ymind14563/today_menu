from crawlers.naver import get_naver_menu_image_url
from utils.logger import logger
from crawlers.kakao import get_kakao_menu_image_url
from utils.storage import load_last_urls, save_last_urls, is_new_url
from utils.date_utils import get_today_date_string
from datetime import datetime

def main():
    logger.info(f"[System] 오늘 날짜: {get_today_date_string()}")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    last_urls = load_last_urls()
    updated = {}

    # 네이버 처리
    naver_url = get_naver_menu_image_url()
    if naver_url:
        is_new, is_today = is_new_url("naver", naver_url, last_urls)
        if is_new:
            logger.info("[네이버 = 옆집] 새로운 메뉴 이미지 감지됨.")
            updated["naver"] = {"url": naver_url, "saved_date": now_str}
        else:
            logger.info("[네이버 = 옆집] 오늘 메뉴가 이미 수집됨." if is_today else "[네이버 = 옆집] 아직 오늘 메뉴가 올라오지 않음.")

    # 카카오 처리
    kakao_url = get_kakao_menu_image_url()
    if kakao_url:
        is_new, is_today = is_new_url("kakao", kakao_url, last_urls)
        if is_new:
            logger.info("[카카오 = 2층] 새로운 메뉴 이미지 감지됨.")
            updated["kakao"] = {"url": kakao_url, "saved_date": now_str}
        else:
            logger.info("[카카오 = 2층] 오늘 메뉴가 이미 수집됨." if is_today else "[카카오 = 2층] 아직 오늘 메뉴가 올라오지 않음.")

    # 저장 및 결과 출력
    if updated:
        last_urls.update(updated)
        save_last_urls(last_urls)
        if "naver" in updated:
            logger.info(f"[네이버 = 옆집] 2층 이미지 URL: {updated['naver']['url']}")
        if "kakao" in updated:
            logger.info(f"[카카오 = 2층] 옆집 이미지 URL: {updated['kakao']['url']}")
    else:
        logger.info("[네이버 = 옆집] 오늘 메뉴가 이미 수집됨.")
        logger.info("[카카오 = 2층] 오늘 메뉴가 이미 수집됨.")

if __name__ == "__main__":
    main()
