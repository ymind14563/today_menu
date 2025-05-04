## 🍱 today_menu

> **매일 자동으로 식당 메뉴 이미지를 수집하고 GitHub Pages를 통해 보여주는 프로젝트**

---

### ✅ 주요 기능

- 식당 3곳(네이버 블로그 / 카카오 채널)의 메뉴 이미지 **자동 수집**
- **오늘 날짜의 메뉴 여부만 식별**하여 업데이트
- **GitHub Actions** 스케줄 활용하여 정기적 업데이트
- **Python + Selenium + GitHub Actions** 기반 완전 자동화
- **GitHub Pages로 정적 웹페이지 배포**
- 성공 시 초록색, 실패 시 노란색 상태 메시지로 시각적 상태 표시

---

### 🧭 프로젝트 구조

```
.
├── .github/workflows/        # GitHub Actions 자동화 스크립트
├── menu_crawler/             # Python 크롤러 코드
│   ├── main.py               # 실행 진입점
│   └── crawlers/             # 사이트별 크롤링 모듈 (naver, kakao)
│   └── utils/                # 공통 유틸 (날짜, 저장소, 로깅 등)
├── docs/                     # GitHub Pages 정적 웹파일 루트
│   ├── index.html            # 메인 페이지
│   ├── images/               # 저장된 메뉴 이미지 (naver.jpg, kakao.jpg)
│   └── last_urls.json        # 이전 이미지 정보 (업데이트 시각 기록 포함)
├── requirements.txt          # Python 의존성 정의
├── README.md                 
```

---

### 🛠 사용 기술

| 기술           | 역할 |
|----------------|------|
| **Python 3**   | 크롤러 전체 작성 언어 |
| **Selenium**   | 웹 자동화 (DOM 탐색, 이미지 추출) |
| **Tailwind CSS** | 웹페이지 UI 구성 |
| **GitHub Actions** | 스케줄 기반 자동화 실행 |
| **GitHub Pages** | 결과 정적 웹페이지 호스팅 |

---

### 🥢 대상 사이트

#### 1. 네이버 블로그
- 고정 URL은 항상 최신 게시글을 가리키지 않음
- 게시글 제목에 날짜 포함됨 (ex. `4월 18일 (금)`)
- 게시글 본문 내 이미지 URL 추출
- 단, **내일/모레 메뉴가 먼저 올라올 수 있어 필터링 필요**

#### 2. 카카오 채널
- 채널 프로필 이미지(프사), 소식의 게시글 이미지가 메뉴판 이미지
- 클릭 시 모달로 원본 이미지 노출됨
- 판단할 날짜 정보 없음 → 이미지 URL이 바뀌면 오늘 메뉴로 간주

---

### ⚙️ 자동화 흐름

1. **Python + Selenium**으로 3곳에서 이미지 URL 수집
2. 이미지 URL을 `docs/last_urls.json`의 이전 값과 비교
3. 새 이미지인 경우:
   - 해당 이미지를 `docs/images/` 폴더에 다운로드
   - `last_urls.json`에 `url`, `saved_date`, `last_checked` 갱신
4. GitHub Actions가 변경된 파일을 자동 커밋 & 푸시
5. GitHub Pages가 새 HTML로 자동 배포
6. `index.html` 내 JS가 JSON을 불러와 실시간 렌더링

---

### 🕒 스케줄 (GitHub Actions 기준)

- KST 기준 자동 실행 시간:
  - `09:00 ~ 10:30`: 30분 간격
  - `11:00 ~ 11:50`: 10분 간격
  - `12:00 ~ 12:30`: 5분 간격

- 내부 로직에서 `saved_date`를 검사
  - 이미 오늘 메뉴가 수집되었으면 → **추가 크롤링 생략**
  - 오늘 메뉴가 아직 없으면 → **크롤링 실행**

- `cron`은 UTC 기준이며, `TZ=Asia/Seoul` 설정을 통해 KST로 처리

---

### 🌐 GitHub Pages 사이트

- `docs/index.html`에 정적 웹페이지로 렌더링
- 실시간 상태표시:
  - ✅ 오늘 메뉴가 수집되었을 경우: **초록색 박스 + 업데이트 시각**
  - ⚠️ 오늘 메뉴가 없을 경우: **노란색 박스 + 최근 확인 시각 표시**
- 캐시 우회를 위해 JS는 `last_urls.json?t=timestamp` 형식으로 요청

---

### 📦 설치 및 실행 (로컬 테스트용)

```bash
# 설치
pip install -r requirements.txt

# 실행
python menu_crawler/main.py

# 로컬 확인
python -m http.server 8080 --directory docs
```

→ http://localhost:8080/index.html 로 접속

---

### 📁 상태 저장 파일 구조 (`last_urls.json` 예시)

```json
{
  "kakao": {
    "url": "https://...",
    "saved_date": "2025-04-21 11:30",
    "last_checked": "2025-04-21 11:40"
  },
  "naver": {
    "url": "https://...",
    "saved_date": "2025-04-21 11:20",
    "last_checked": "2025-04-21 11:40"
  }
}
```

---

### 📌 참고 사항

- 메뉴가 게시되지 않았거나, 업로드 지연 시 **이전 이미지가 그대로 유지될 수 있음**
- 네이버 블로그는 **블로그 게시글 제목을 파싱하여 정규식으로 판단**
- 카카오 채널은 **이미지가 바뀌는 것만으로 오늘 메뉴로 판단**
- 브라우저 캐시 문제 발생 시 `Ctrl + Shift + R`로 강력 새로고침 필요

---

### 🙋 피드백

> 개선 아이디어, 오류 제보는 언제든 환영입니다.  
> 본 프로젝트는 개인 학습 및 실사용 목적이며, **완전 무료로 운영됩니다.**
> 
> 제작일: 2025년 4월 19일 (ver. 1)
> 
> made by ymind14563 👨‍💻
> 
> ✉️ 문의: ymind14563@gmail.com

---

### 🌐 저작권
- © 2025 ymind14563. 코드와 페이지 구성에 대한 저작권 보유, 무단 전재 및 재배포 금지.
- 메뉴 이미지는 공개 플랫폼에서 수집된 자료로, 이미지의 저작권은 각 게시자에게 있습니다.
