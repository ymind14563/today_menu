from crawlers.naver import get_naver_menu_image_url
from crawlers.kakao import get_kakao_menu_image_url
from utils.storage import load_last_urls, save_last_urls, is_new_url
from utils.date_utils import get_today_date_string
from datetime import datetime

def main():
    print("[디버그] get_today_date_string 결과:", get_today_date_string())

    today_str = datetime.now().strftime("%Y-%m-%d")
    last_urls = load_last_urls()
    updated = {}


    # 네이버 처리
    naver_url = get_naver_menu_image_url()
    if naver_url:
        is_new, is_today = is_new_url("naver", naver_url, last_urls)
        if is_new:
            print("[네이버 = 2층] 새로운 메뉴 이미지 감지됨.")
            updated["naver"] = {"url": naver_url, "saved_date": today_str}
        else:
            print("[네이버 = 2층] 오늘 메뉴가 이미 수집됨." if is_today else "[네이버 = 2층] 아직 오늘 메뉴가 올라오지 않음.")

    # 카카오 처리
    kakao_url = get_kakao_menu_image_url()
    if kakao_url:
        is_new, is_today = is_new_url("kakao", kakao_url, last_urls)
        if is_new:
            print("[카카오 = 옆집] 새로운 메뉴 이미지 감지됨.")
            updated["kakao"] = {"url": kakao_url, "saved_date": today_str}
        else:
            print("[카카오 = 옆집] 오늘 메뉴가 이미 수집됨." if is_today else "[카카오 = 옆집] 아직 오늘 메뉴가 올라오지 않음.")


    # 저장 및 결과 출력
    if updated:
        last_urls.update(updated)
        save_last_urls(last_urls)
        print("\n📌 오늘의 메뉴 이미지 URL:")
        for k, v in updated.items():
            print(f"- {k}: {v['url']}")
    else:
        print("\n🔁 오늘 메뉴는 이미 수집됨.")

if __name__ == "__main__":
    main()
