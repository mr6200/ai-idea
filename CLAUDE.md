# 작업 규칙

## 소통
- 작업 과정 설명(진행 상황, 중간 보고)은 영어가 아닌 한글로 쓴다.

## 쇼츠 제작
- 지식 쇼츠 제작 순서·도구·주의점은 `shorts/WORKFLOW.md`에 정리되어 있다. 이어서 작업할 때 먼저 읽는다.
- 편 번호: 「예금 vs 적금」과 「은행의 탄생」은 둘 다 5편이다 (사용자 지정). 다음 편은 6편.
- 「은행의 탄생」(5편)부터 영상 길이는 2분(120초), 내용 분량은 그대로, TTS 속도는 1.2배(`RATE = 1.2`)로 만든다. 자세한 내용은 `shorts/WORKFLOW.md`의 「2분 규격」.
- 화면 스타일: 9편 「비행기 창문은 왜 둥글까?」부터 **설계도+팝아트** 스타일이 기본 (사용자 지정, 앞으로 계속). 자막은 도현(Do Hyeon), 나머지 글꼴은 판단해서 사용 (제목 Black Han Sans, 감탄사 Jua). 화면 오른쪽 아래 도면 표제란 문구(「DWG. 0NN · 지식 쇼츠」)는 10편부터 넣지 않는다 (사용자 요청). 자세한 규칙은 `shorts/WORKFLOW.md`의 「설계도+팝아트 스타일」.
- 15편 「국민연금, 낸 돈보다 더 받을까?」는 노후 준비 시리즈 3편, 같은 1분 30초 · 3D 클레이 AI + 인포그래픽. 15편부터 렌더 전에 `build/tts_check.py`로 TTS 어색함을 검사하고 고친다 (사용자 요청).
- 14편 「국민연금, 일찍 받을까 늦게 받을까?」는 13편 후속, 같은 1분 30초 · 3D 클레이 AI + 인포그래픽 (사용자 승인).
- 13편 「60세 퇴직, 연금은 65세?」는 1분 30초(90초), 3D 클레이 AI + 미니멀 인포그래픽 스타일 (사용자 선택). 다음 편 길이·스타일도 사용자에게 확인한다.
- 12편 「타이타닉은 왜 가라앉았을까?」는 사용자 지정으로 1분 10초(70초), 빈티지 포스터 + AI 동판화 스타일, RunPod 그림을 켄 번즈로 움직여 영상미 있게 만든다. 다음 편 길이·스타일은 사용자에게 확인한다.
- 8편부터 조회수 회복을 위해 흥미로운 질문형 주제, 9편부터는 금융이 아닌 주제도 다룬다. 영상 길이는 1분 30초(90초)를 계속 쓴다.
- 6편·7편은 시청 지속률 비교를 위해 1분 30초(90초)로 만든다. TTS 속도는 1.2배 그대로, 장면을 12개 안팎으로 줄여 내용을 덜어낸다. 5편(2분)과 비교한 뒤 규격을 정한다. 자세한 내용은 `shorts/WORKFLOW.md`의 「1분 30초 시험」.

## 완성 파일 전달
- 완성된 결과물(영상, 이미지, 문서 등 최종 파일)은 사용자의 Google Drive에 업로드한다.
- Google Drive 커넥터가 세션에 연결되어 있지 않으면, 업로드하지 못했다고 알리고
  https://claude.ai/customize/connectors 에서 연결한 뒤 새 세션을 열어 달라고 안내한다.
- 중간 산출물(스크래치, 테스트 렌더)은 업로드하지 않는다.
- Drive 커넥터는 파일 내용을 base64로 한 번에 보내야 해서 큰 바이너리(영상 등)는 올릴 수 없다.
  그런 파일은 GitHub 링크를 담은 메모를 Drive 폴더에 올리고, 사용자에게 그렇게 했다고 말한다.
- 기존 폴더: "복리의 마법 쇼츠" (id 13pq1Rpo-BD7anVeYfYg30VEEplezJ6Ff), "72의 법칙 쇼츠" (id 1-bXT4wqmQr0SQ5y7Cjikz61cpqiFsU-r), "4%의 법칙 쇼츠" (id 1d5LAWlVkBuNWuHLhUwDPeFMI2lATuccV), "적립식 vs 거치식 쇼츠" (id 1ROEb8W9iU2bGKot9KzdwNHegwlnVwfJR), "예금 vs 적금 쇼츠" (id 1-Pjspc__xyiAxM2nltxYdcsC2omMJrRg), "은행의 탄생 쇼츠" (id 1B_Z-pxMtxFYA745ITXJIy8up5qYzSdsL), "은행의 돈벌이 쇼츠" (id 1RJiF3lGZde5708EaxF6LOf98qxD2K1Hu), "이자와 세금 쇼츠" (id 1apUwroQgv0np0KxzW3Q2KlMb0Y5g4gDO), "무이자 할부 쇼츠" (id 1gpmtE9-eXTMoL3bXtcm7SRqxo6Db9ygS), "비행기 창문 쇼츠" (id 10vuq4xTbwq6cbtON0yTtExck9KwP_HeQ), "귀가 먹먹한 이유 쇼츠" (id 1Bvv3wnIWGczgACwLt_A-N4L6L26GsjEq), "엘리베이터 쇼츠" (id 1P6mgZ3jJeVrJ1h3BpNUH_xHm0eWOIzd0), "타이타닉 쇼츠" (id 1ULBkCI8_IumPwv8HVqor53ICZrGk9eep), "노후 소득 공백 쇼츠" (id 1lq1mQCeXRrOU5ALChQ5Nnj35A9_c46g9), "국민연금 받는 나이 쇼츠" (id 1MjRwHxivPI68a5Aka2_CXyf1IcNDU1s0)
- 새 편은 Drive에도 새 폴더를 만들어 올린다.
