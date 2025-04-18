# 날짜 판별 로직

from datetime import datetime
from typing import Optional
import re

# 오늘 날짜를 '4월 18일' 형식으로 변경
def get_today_date_string():
    now = datetime.now()
    return f"{now.month}월 {now.day}일"


# 글 제목에 오늘 날짜가 포함되어 있는지 확인
# -> '4월18일', '4 월 18 일', '4월 오전 18일' 등 포함 허용
def is_today_in_title(title: str) -> bool:
    today = datetime.now()
    m, d = today.month, today.day

    today_str = f"{m}월 {d}일"
    print(f"[디버그] 오늘 날짜 기준 문자열: '{today_str}' / 대상 제목: '{title}'") 
    
    # 정규식: 월과 일이 떨어져 있거나 중간 단어 있는 것도 허용
    pattern = rf"{m}\s*월[^0-9a-zA-Z가-힣]{{0,5}}{d}\s*일"
    # return re.search(pattern, title) is not None
    return re.search(pattern, title) is not None
    



# 정규식 기반, 글 제목에서 날짜 부분만 추출 (예: '4월 18일')
def extract_date_from_title(title: str) -> Optional[str]:
    match = re.search(r"\d{1,2}월\s*\d{1,2}일", title)
    return match.group() if match else None
