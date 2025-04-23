# 건너집

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import logger
from utils.date_utils import is_today_in_title  # 오늘 날짜 포함 확인 함수
from config import KAKAO_2_CHANNEL_URL, CHROME_HEADLESS, CHROME_DRIVER_WAIT, USER_AGENT
from typing import Optional
import time

def get_kakao_2_menu_image_url() -> Optional[str]:
    options = Options()
    if CHROME_HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"user-agent={USER_AGENT}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(CHROME_DRIVER_WAIT)
    driver.get(KAKAO_2_CHANNEL_URL)

    try:
        logger.info("[카카오_2] 채널 접속 완료")
        time.sleep(2)

        cards = driver.find_elements(By.CSS_SELECTOR, ".box_list_board .link_board")
        logger.info(f"[카카오_2] 소식 카드 개수: {len(cards)}")

        for card in cards:
            title = card.text.strip()
            if is_today_in_title(title):
                logger.info(f"[카카오_2] 오늘 날짜 소식 발견: {title}")
                thumb_div = card.find_element(By.CSS_SELECTOR, ".wrap_fit_thumb")
                style = thumb_div.get_attribute("style")
                if "background-image" in style:
                    start = style.find("url(") + 4
                    end = style.find(")", start)
                    image_url = style[start:end].strip('"').strip("'")
                    logger.info(f">>> [카카오_2-결과] 메뉴 이미지 추출 완료: {image_url}")
                    driver.quit()
                    return image_url

        logger.info(">>> [카카오_2-결과] 오늘 날짜 소식 없음")
        driver.quit()
        return None

    except Exception as e:
        import traceback
        logger.info(">>> [카카오_2-결과] 크롤링 실패", type(e).__name__)
        traceback.print_exc()
        driver.quit()
        return None
