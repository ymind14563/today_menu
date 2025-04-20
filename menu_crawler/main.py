from crawlers.naver import get_naver_menu_image_url
from crawlers.kakao import get_kakao_menu_image_url
from utils.storage import load_last_urls, save_last_urls, is_new_url
from utils.date_utils import get_today_date_string
from utils.logger import logger
from datetime import datetime, timedelta, timezone
from utils.image import save_image_from_url

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

    # ==================== 네이버 시작 ====================
    logger.info("=" * 25 + " [네이버 = 옆집] " + "=" * 25)
    naver_url = get_naver_menu_image_url()
    last_urls.setdefault("naver", {})["last_checked"] = now_str

    if naver_url:
        is_new, is_today = is_new_url("naver", naver_url, last_urls)
        if is_new:
            logger.info("[네이버 = 옆집] 새로운 메뉴 이미지 감지됨.")
            updated["naver"] = {"url": naver_url, "saved_date": now_str}
            save_image_from_url(naver_url, "naver")
            naver_result = f"[네이버 = 옆집] 2층 이미지 URL: {naver_url}"
        else:
            msg = "[네이버 = 옆집] 오늘 메뉴가 이미 수집됨."
            logger.info(msg)
            naver_result = msg
    else:
            msg = "[네이버 = 옆집] 아직 오늘 메뉴가 올라오지 않음."
            logger.info(msg)
            naver_result = msg

    logger.info("\n")

    # ==================== 카카오 시작 ====================
    logger.info("=" * 25 + " [카카오 = 2층] " + "=" * 25)
    kakao_url = get_kakao_menu_image_url()
    last_urls.setdefault("kakao", {})["last_checked"] = now_str

    if kakao_url:
        is_new, is_today = is_new_url("kakao", kakao_url, last_urls)
        if is_new:
            logger.info("[카카오 = 2층] 새로운 메뉴 이미지 감지됨.")
            updated["kakao"] = {"url": kakao_url, "saved_date": now_str}
            save_image_from_url(kakao_url, "kakao")
            kakao_result = f"[카카오 = 2층] 옆집 이미지 URL: {kakao_url}"
        else:
            # if is_today:
            #     msg = "[카카오 = 2층] 오늘 메뉴가 이미 수집됨."
            # else:
            #     msg = "[카카오 = 2층] 아직 오늘 메뉴가 올라오지 않음."

            msg = (
                "[카카오 = 2층] 오늘 메뉴가 이미 수집됨."
                if is_today else "[카카오 = 2층] 아직 오늘 메뉴가 올라오지 않음."
            )
            logger.info(msg)
            kakao_result = msg
    else:
            msg = "[카카오 = 2층] 프로필 사진이 비어 있음."
            logger.info(msg)
            kakao_result = msg

    logger.info("\n")

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
    logger.info("-" * 69 + "\n")

    logger.info("[System] 크롤링 및 저장 완료")

if __name__ == "__main__":
    main()
