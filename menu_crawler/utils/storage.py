# 이미지 URL을 저장하고 비교하는 기능

import json
import os
from config import LAST_URLS_PATH
from datetime import datetime, timedelta, timezone

# KST 시간대 정의
KST = timezone(timedelta(hours=9))

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
    saved = last_data.get(site_key)
    if not saved:
        return True, False

    saved_url = saved.get("url")
    saved_datetime = saved.get("saved_date")  # "2025-04-19 18:35"

    try:
        saved_date_only = saved_datetime.split(" ")[0]  # "2025-04-19"
    except:
        saved_date_only = None

    today = datetime.now(KST).strftime("%Y-%m-%d")
    is_today = saved_date_only == today
    is_new = url != saved_url

    return is_new, is_today

