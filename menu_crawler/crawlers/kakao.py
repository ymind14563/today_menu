# 1층

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import KAKAO_CHANNEL_URL, CHROME_HEADLESS, CHROME_DRIVER_WAIT, USER_AGENT
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional
from selenium.webdriver.chrome.service import Service
import time

def get_kakao_menu_image_url() -> Optional[str]:
    options = Options()
    if CHROME_HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"user-agent={USER_AGENT}") 

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(CHROME_DRIVER_WAIT)
    driver.get(KAKAO_CHANNEL_URL)

    try:
        print("[카_디버깅] 카카오 채널 접속 완료")

        # 프사 클릭
        thumb = WebDriverWait(driver, CHROME_DRIVER_WAIT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_thumb"))
        )
        thumb.click()
        print("[카_디버깅] 썸네일 클릭 완료")
        time.sleep(2)

        # 팝업 이미지 추출
        img = WebDriverWait(driver, CHROME_DRIVER_WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".layer_body .img_thumb"))
        )
        src = img.get_attribute("src")
        print("[카_디버깅] 이미지 URL 추출:", src)
        time.sleep(1) 
        driver.quit()
        time.sleep(1)
        return src if src else None

    except Exception as e:
        print("[카카오] 크롤링 실패:", e)
        driver.quit()
        return None
