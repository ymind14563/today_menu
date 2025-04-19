# 모든 설정값을 중앙에서 관리

from datetime import datetime, timedelta, timezone
import os

# KST 시간대 정의
KST = timezone(timedelta(hours=9))

# 사이트 URL
NAVER_BLOG_URL = "https://blog.naver.com/skfoodcompany"
KAKAO_CHANNEL_URL = "https://pf.kakao.com/_xdxagIn"

# 날짜 포맷 (오늘 날짜 기준, 예: '4월 18일')
TODAY = datetime.now(KST)
TODAY_DATE_STR = f"{TODAY.month}월 {TODAY.day}일"

# 비교용 저장 파일 경로
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAST_URLS_PATH = os.path.join(PROJECT_ROOT, "docs/last_urls.json")

# 유저 에이전트 공통 상수
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# 크롬 실행 옵션
CHROME_HEADLESS = True   # headless 모드 사용 여부
CHROME_DRIVER_WAIT = 10  # 암묵적 대기시간 (초)

# 기타 설정
DEBUG = True  # 디버그용 로그 출력 여부
