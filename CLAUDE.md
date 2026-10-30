# 작업 규칙

## 소통
- 작업 과정 설명(진행 상황, 중간 보고)은 영어가 아닌 한글로 쓴다.

## 쇼츠 제작
- 지식 쇼츠 제작 순서·도구·주의점은 `shorts/WORKFLOW.md`에 정리되어 있다. 이어서 작업할 때 먼저 읽는다.
- 편 번호: 「예금 vs 적금」과 「은행의 탄생」은 둘 다 5편이다 (사용자 지정). 다음 편은 6편.
- 「은행의 탄생」(5편)부터 영상 길이는 2분(120초), 내용 분량은 그대로, TTS 속도는 1.2배(`RATE = 1.2`)로 만든다. 자세한 내용은 `shorts/WORKFLOW.md`의 「2분 규격」.
- 화면 스타일: 9편 「비행기 창문은 왜 둥글까?」부터 **설계도+팝아트** 스타일이 기본 (사용자 지정, 앞으로 계속). 자막은 도현(Do Hyeon), 나머지 글꼴은 판단해서 사용 (제목 Black Han Sans, 감탄사 Jua). 화면 오른쪽 아래 도면 표제란 문구(「DWG. 0NN · 지식 쇼츠」)는 10편부터 넣지 않는다 (사용자 요청). 자세한 규칙은 `shorts/WORKFLOW.md`의 「설계도+팝아트 스타일」.
- 18편부터 **60초 + 썸네일 1초** (사용자 지정, 2026-10-30, 조회수 회복용). 주제는 돈·생활. 18편 「로또 1등은 정말 망할까?」(`shorts/lotto-winners/`)는 3D 클레이 AI + 인포그래픽 (사용자 선택). 「편의점 1+1, 정말 이득일까?」(`shorts/convenience-deals/`)는 완성했지만 사용자가 **폐기** (2026-10-30, 흥미가 적을 것 같다는 이유). 19편 번호는 새 주제에 다시 쓴다. 주제는 "와, 진짜?" 하는 반전·이야기형으로 고른다. 새 19편 「내 통장에 잠자는 숨은 돈」(`shorts/hidden-money/`)은 같은 3D 클레이 AI + 인포그래픽 (사용자 선택 주제).
- 17편 「여자는 왜 더 오래 살까?」(`shorts/women-longevity/`)는 1분 30초 + 썸네일 1.5초, **실사 다큐** 스타일: Seedream 4.0 세로 사진 → WAN 2.2 I2V 영상 (RunPod 공개 엔드포인트, 사용자 요청). 한 편 약 $5로 이전보다 훨씬 비싸므로 다음 편 스타일은 사용자에게 확인한다. 자세한 내용은 `shorts/women-longevity/README.md`.
- 16편 「신호등은 왜 빨강·노랑·초록일까?」(`shorts/traffic-light/`)는 1분 30초 + 썸네일 1.5초, 빈티지 포스터 + AI 동판화 (사용자 선택).
- 「주택연금, 집 한 채로 매달 얼마 받을까?」(`shorts/house-pension/`)는 사용자가 **폐기** (2026-10-30). 16편 번호는 새 주제에 다시 쓴다. 이 작업에서 만든 썸네일 인트로 규칙은 유지: 영상 맨 앞에 썸네일을 1.5초 넣는다 (사용자 요청, `WORKFLOW.md`의 「썸네일 인트로」).
- 15편 「국민연금, 낸 돈보다 더 받을까?」는 노후 준비 시리즈 3편, 같은 1분 30초 · 3D 클레이 AI + 인포그래픽. 15편부터 렌더 전에 `build/tts_check.py`로 TTS 어색함을 검사하고 고친다 (사용자 요청).
- 14편 「국민연금, 일찍 받을까 늦게 받을까?」는 13편 후속, 같은 1분 30초 · 3D 클레이 AI + 인포그래픽 (사용자 승인).
- 13편 「60세 퇴직, 연금은 65세?」는 1분 30초(90초), 3D 클레이 AI + 미니멀 인포그래픽 스타일 (사용자 선택). 다음 편 길이·스타일도 사용자에게 확인한다.
- 12편 「타이타닉은 왜 가라앉았을까?」는 사용자 지정으로 1분 10초(70초), 빈티지 포스터 + AI 동판화 스타일, RunPod 그림을 켄 번즈로 움직여 영상미 있게 만든다. 다음 편 길이·스타일은 사용자에게 확인한다.
- 8편부터 조회수 회복을 위해 흥미로운 질문형 주제, 9편부터는 금융이 아닌 주제도 다룬다. 영상 길이는 1분 30초(90초)를 계속 쓴다.
- 6편·7편은 시청 지속률 비교를 위해 1분 30초(90초)로 만든다. TTS 속도는 1.2배 그대로, 장면을 12개 안팎으로 줄여 내용을 덜어낸다. 5편(2분)과 비교한 뒤 규격을 정한다. 자세한 내용은 `shorts/WORKFLOW.md`의 「1분 30초 시험」.

## RunPod 사용 보고
- RunPod을 쓴 편은 완성 보고에 **그 편에서 쓴 금액과 남은 잔액**을 꼭 적는다 (사용자 요청, 2026-10-29). 잔액은 GraphQL `myself { clientBalance }`, 사용액은 REST `GET /v1/billing/endpoints`·`/v1/billing/pods`(bucketSize=day)로 조회한다.
- 쓰고 나면 엔드포인트·템플릿을 지우고, 남은 엔드포인트·파드가 없는지 확인해 함께 보고한다.
- 파드 `360qr47tgkg9qo`(incredible_rose_gazelle)와 10월 네트워크 볼륨은 이 작업에서 만든 것이 아니다. 건드리지 않고 비용만 보고한다.

## 완성 파일 전달
- 완성된 결과물(영상, 이미지, 문서 등 최종 파일)은 사용자의 Google Drive에 업로드한다.
- Google Drive 커넥터가 세션에 연결되어 있지 않으면, 업로드하지 못했다고 알리고
  https://claude.ai/customize/connectors 에서 연결한 뒤 새 세션을 열어 달라고 안내한다.
- 중간 산출물(스크래치, 테스트 렌더)은 업로드하지 않는다.
- Drive 커넥터는 파일 내용을 base64로 한 번에 보내야 해서 큰 바이너리(영상 등)는 올릴 수 없다.
  그런 파일은 GitHub 링크를 담은 메모를 Drive 폴더에 올리고, 사용자에게 그렇게 했다고 말한다.
- 기존 폴더: "복리의 마법 쇼츠" (id 13pq1Rpo-BD7anVeYfYg30VEEplezJ6Ff), "72의 법칙 쇼츠" (id 1-bXT4wqmQr0SQ5y7Cjikz61cpqiFsU-r), "4%의 법칙 쇼츠" (id 1d5LAWlVkBuNWuHLhUwDPeFMI2lATuccV), "적립식 vs 거치식 쇼츠" (id 1ROEb8W9iU2bGKot9KzdwNHegwlnVwfJR), "예금 vs 적금 쇼츠" (id 1-Pjspc__xyiAxM2nltxYdcsC2omMJrRg), "은행의 탄생 쇼츠" (id 1B_Z-pxMtxFYA745ITXJIy8up5qYzSdsL), "은행의 돈벌이 쇼츠" (id 1RJiF3lGZde5708EaxF6LOf98qxD2K1Hu), "이자와 세금 쇼츠" (id 1apUwroQgv0np0KxzW3Q2KlMb0Y5g4gDO), "무이자 할부 쇼츠" (id 1gpmtE9-eXTMoL3bXtcm7SRqxo6Db9ygS), "비행기 창문 쇼츠" (id 10vuq4xTbwq6cbtON0yTtExck9KwP_HeQ), "귀가 먹먹한 이유 쇼츠" (id 1Bvv3wnIWGczgACwLt_A-N4L6L26GsjEq), "엘리베이터 쇼츠" (id 1P6mgZ3jJeVrJ1h3BpNUH_xHm0eWOIzd0), "타이타닉 쇼츠" (id 1ULBkCI8_IumPwv8HVqor53ICZrGk9eep), "노후 소득 공백 쇼츠" (id 1lq1mQCeXRrOU5ALChQ5Nnj35A9_c46g9), "국민연금 받는 나이 쇼츠" (id 1MjRwHxivPI68a5Aka2_CXyf1IcNDU1s0), "국민연금 수익비 쇼츠" (id 1DJv1LjwFbiwvpWwoNxhZJqGE3frEVYZB), "주택연금 쇼츠(폐기)" (id 1K48eioMu4IkEqdg1tLtNqTTBkATL0L5l), "신호등 쇼츠" (id 1ipD2PcPkEuID8xiNjShk02u214IP_KOc), "여자 수명 쇼츠" (id 1ywVxUPOs5J-JW9oLR8TA2c8LHJpf-Qx1), "로또 1등 쇼츠" (id 1aPmccFtY-6vkzdc39p4__Xw1iyyd6IDc), "편의점 1+1 쇼츠(폐기)" (id 1z9Pvrr4ULtxFe2y4j75gmWrxtToOO9v7), "숨은 돈 쇼츠" (id 1SmmhG6XQcYG-SD4f9hM5HLRhHy6nL9Rp)
- 새 편은 Drive에도 새 폴더를 만들어 올린다.
