# 이미지 다운로드 (doc/image)

import os
import time
import requests
from config import USER_AGENT
from utils.logger import logger

def save_image_from_url(url: str, label: str) -> bool:

    # label을 기준으로 파일명 자동 설정, 다운로드, 저장
    filename = f"{label}.jpg"
    path = os.path.join("docs/images", filename)

    # logger 용 한글 라벨 매핑
    display_name = {
        "naver": "네이버",
        "kakao": "카카오"
    }.get(label)

    try:
        # 저장 폴더 생성 (이미 있으면 무시)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        time.sleep(1.5)

        # 이미지 요청 (User-Agent 설정 및 타임아웃)
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)

        # 응답 실패 시 로그 출력 후 종료
        if response.status_code != 200:
            logger.info(f"[{display_name}] 응답 실패 (status: {response.status_code})")
            return False

        # 이미지 파일 저장
        with open(path, "wb") as f:
            f.write(response.content)

        logger.info(f"[{display_name}] 이미지 다운로드 및 저장 완료: {path}")
        return True

    except Exception as e:
        logger.info(f"[{display_name}] 이미지 저장 실패: {str(e)}")
        return False