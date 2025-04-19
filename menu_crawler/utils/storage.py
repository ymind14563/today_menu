# 이미지 URL을 저장하고 비교하는 기능

import json
import os
from config import LAST_URLS_PATH
from datetime import datetime


# 이전 이미지 URL 목록 불러오기
def load_last_urls() -> dict:
    if not os.path.exists(LAST_URLS_PATH):
        return {}
    with open(LAST_URLS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 현재 이미지 URL 목록 저장
def save_last_urls(data: dict):
    with open(LAST_URLS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 새로운 이미지 URL인지 확인
def is_new_url(site_key: str, url: str, last_data: dict) -> tuple[bool, bool]:
    today_str = datetime.now().strftime("%Y-%m-%d")
    info = last_data.get(site_key)
    if isinstance(info, dict):
        saved_url = info.get("url")
        saved_date = info.get("saved_date")
        if url == saved_url:
            return False, saved_date == today_str  # (같음, 오늘 저장된 것인지)
    return True, False  # (다름, 저장된 게 없음)
