# 옆집

from selenium import webdriver
from utils.logger import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from config import NAVER_BLOG_URL, CHROME_HEADLESS, CHROME_DRIVER_WAIT, USER_AGENT
from utils.date_utils import is_today_in_title
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional
import time

def get_naver_menu_image_url() -> Optional[str]:
    options = Options()
    if CHROME_HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"user-agent={USER_AGENT}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(CHROME_DRIVER_WAIT)
    driver.get(NAVER_BLOG_URL)

    try:
        # iframe 진입
        driver.switch_to.frame("mainFrame")
        logger.info("[네이버] iframe 'mainFrame' 진입 완료")
        time.sleep(2)

        # 전체보기 클릭
        menu = driver.find_element(By.LINK_TEXT, "전체보기")
        menu.click()
        logger.info("[네이버] '전체보기' 클릭 완료")
        time.sleep(2)

        # 글 목록 탐색
        container = driver.find_element(By.ID, "postBottomTitleListBody")
        posts = container.find_elements(By.CSS_SELECTOR, "a.pcol2")
        logger.info(f"[네이버] 글 목록 진입 완료")
        logger.info(f"[네이버] 추출된 글 개수: {len(posts)}")
        time.sleep(2)

        found = False
        for post in posts:
            title = post.text.strip()
            logger.info(f"[네이버] 제목 확인: {title}")
            if is_today_in_title(title):
                logger.info(f"[네이버] 오늘 날짜 글 발견: '{title}'")
                post.click()
                found = True
                time.sleep(1)
                break

        

        if not found:
            logger.info(">>> [네이버-결과] 유효한 메뉴 이미지 없음")
            driver.quit()
            time.sleep(2)
            return None
        
        time.sleep(2)

        # iframe 재지정
        driver.switch_to.default_content()
        driver.switch_to.frame("mainFrame")
        logger.info("[네이버] iframe 'mainFrame' 재진입 완료")
        time.sleep(2)

        # 이미지 추출
        images = driver.find_elements(By.CSS_SELECTOR, "div[id^='post-view'] img")
        logger.info(f"[네이버] 이미지 추출 시작")

        for img in images:
            src = img.get_attribute("src")
            if src and src.startswith("https://postfiles.pstatic.net"):
                logger.info(f">>> [네이버-결과] 메뉴 이미지 추출 완료: {src}")
                time.sleep(1) 
                driver.quit()
                time.sleep(1)
                return src

        logger.info(">>> [네이버-결과] 유효한 메뉴 이미지 없음")
        driver.quit()
        time.sleep(1)
        return None

    except Exception as e:
        import traceback
        logger.info(">>> [네이버-결과] 크롤링 실패", type(e).__name__)
        time.sleep(1)
        traceback.print_exc()
        driver.quit()
        time.sleep(1)
        return None
