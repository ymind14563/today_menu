# 로깅 기본 설정

import logging
import time
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 스트림 핸들러 생성
stream_handler = logging.StreamHandler()

# 한국 시간 (KST) 설정
KST = timezone(timedelta(hours=9))

# 로그 출력 형식 및 시간대 적용
def kst_converter(*args):
    dt = datetime.now(KST)
    return time.localtime(time.mktime(dt.timetuple()))

formatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
formatter.converter = kst_converter
stream_handler.setFormatter(formatter)

# 핸들러 연결
logger.addHandler(stream_handler)

# 내보내기
__all__ = ["logger"]
