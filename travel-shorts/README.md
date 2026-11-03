# 여행 숙소 실사 쇼츠 자동 제작기

사진 + 대본(JSON) → **1080×1920 유튜브 쇼츠(mp4)** 를 자동으로 만들어요.

- 사진마다 천천히 움직이는 **Ken Burns 효과** (가로 사진은 패닝, 세로 사진은 줌)
- 문장 단위 **AI 나레이션**(Edge TTS, 무료), 나레이션과 **딱 맞춘 큰 자막**, `*강조*` 단어는 노란색
- 상단 **숙소 카드**: 순위 배지, 숙소명, 위치, 가격·특징 칩
- 장면 전환 크로스페이드, **BGM 자동 덕킹**(나레이션 나올 때 음악 볼륨을 낮춤)
- 업로드용 `description.txt` (해시태그와 **사진 출처 표기**) 자동 생성

## 빠르게 시작하기

```bash
./setup.sh                                          # 패키지와 폰트 설치 (ffmpeg은 따로 설치)
python fetch_images.py projects/singapore-marina-bay-sands # 사진 다운로드와 credits.json 생성
python build_short.py  projects/singapore-marina-bay-sands --preview   # 장면별 미리보기 이미지
python build_short.py  projects/singapore-marina-bay-sands             # 최종 mp4
```

결과는 `projects/<이름>/output/` 에 저장돼요 (`<이름>.mp4`, `description.txt`).

## 새 영상 만들기

`projects/singapore-marina-bay-sands` 폴더를 복사한 뒤 `spec.json` 만 수정하면 돼요.

| 항목 | 설명 |
|---|---|
| `images` | `{"키": {"commons": "File:..."}}`, `{"url": "..."}`, `{"path": "내사진.jpg", "credit": "..."}` |
| `hotels` | 숙소 카드 정보. `badge`(TOP 1, 가성비 등), `name`, `place`, `chips` |
| `scenes[]` | 장면 하나가 사진 한 장. `image`, `hotel`, `lines`(문장마다 자막 1개와 나레이션 1개) |
| `lines` | `"문장"` 또는 `{"text": "자막", "say": "실제로 읽을 문장"}`. 자막에서 `\n` 은 줄바꿈, `*단어*` 는 강조 |
| `focus` | 0 ~ 1. 가로 사진에서 화면이 머물 가로 위치 (0 = 왼쪽, 1 = 오른쪽) |
| `motion` | `auto` / `pan` / `zoom` |
| `hook` / `outro` | 첫 장면과 마지막 장면의 큰 타이틀 (`top`, `big`), `captions: false` 와 함께 사용 |
| `voice`, `rate` | TTS 목소리와 속도. 예: `ko-KR-SunHiNeural`(여), `ko-KR-InJoonNeural`(남), `+12%` |
| `bgm` | `"synth"`(자체 생성 잔잔한 음악) 또는 mp3 경로. YouTube 오디오 보관함 음원을 추천해요 |

**기본 포맷 (예시 영상): 숙소 1곳 + 주변 명소.** 숙소 장면 4개 정도를 넣은 뒤 `hotels` 에 명소를 `badge: "주변 명소 1"` 처럼 추가하고, 명소마다 장면 1~2개를 이어 붙이면 돼요.

**한 숙소 집중 소개** 영상은 `hotels` 에 숙소 하나만 넣고, 외관 → 객실 → 수영장 → 조식 → 가격 순서로 장면 4~6개를 구성하면 돼요.
**모음집** 영상은 예시처럼 숙소마다 장면 2~3개씩 배치하면 돼요. 문장 15~20개가 대략 40~50초 분량이에요.

## ⚠️ 사진 저작권: 꼭 읽어주세요

아고다, 트립닷컴, 에어비앤비, 호텔스컴바인에 올라온 사진은 **호텔, 호스트, 또는 사진가의 저작물**이에요.
플랫폼 약관상 무단 재사용이 금지되어 있어서, 그대로 쓰면 유튜브 저작권 신고나 수익 창출 제한을 받을 수 있어요.
구글 이미지 검색 결과도 마찬가지예요. 아래처럼 안전한 사진을 사용하세요.

1. **Unsplash 무료 사진 (예시 영상에서 사용)**: 상업적 사용과 수익화가 가능하고 출처 표기도 필수는 아니에요. 단, 유료인 **Unsplash+** 사진은 제외하세요. spec 에 `page`(사진 페이지 링크)와 `credit` 을 적어두면 `description.txt` 에 다운로드 링크가 자동으로 들어가요. Pexels, Pixabay, 위키미디어 CC0 사진도 같은 방식으로 쓸 수 있어요.
2. **호텔 공식 미디어 키트 / 보도자료 사진**: 호텔 홍보팀에 사용 허락을 받으면 가장 고화질이에요.
3. **제휴(어필리에이트) 프로그램**: 아고다 파트너스, 트립닷컴 어필리에이트 등은 제휴 링크와 함께 쓸 수 있는 콘텐츠와 API를 제공해요. 제휴 링크로 수익도 낼 수 있어요.
4. **Unsplash / Pexels 무료 사진**, 또는 **직접 촬영한 사진과 영상**.

가격 칩(`1박 50만원대~`)은 예시용 대략적인 값이에요. 업로드 전에 실제 사이트에서 확인하고 수정하세요.

## 구글 드라이브 자동 업로드

`./upload_to_drive.sh projects/<이름> "드라이브 폴더 이름"` 을 실행하면 `output/` 의 mp4 와 txt 가 내 드라이브의 해당 폴더로 올라가요. 폴더가 없으면 새로 만들어요.

**처음 한 번만 준비하면 돼요.**
1. 내 컴퓨터에 rclone 을 설치해요: https://rclone.org/downloads/
2. 터미널에서 `rclone authorize "drive"` 를 실행해요. 브라우저가 열리면 구글 계정으로 로그인하고 허용을 눌러요.
3. 터미널에 출력된 `{"access_token": ... "refresh_token": ...}` 전체(JSON)를 복사해요.
4. Claude Code 클라우드 환경 설정에 `GDRIVE_TOKEN` 이라는 이름으로 저장해요 (세션 상단의 환경 메뉴 → Edit → 환경 변수 또는 Network secrets). 저장 후에는 새 세션에서 적용돼요.

⚠️ 이 토큰이 있으면 내 구글 드라이브 전체에 접근할 수 있어요. 채팅창에는 절대 붙여넣지 마세요. 필요 없어지면 https://myaccount.google.com/permissions 에서 rclone 권한을 해제하세요.
