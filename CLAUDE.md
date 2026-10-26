# 작업 규칙

## 소통
- 작업 과정 설명(진행 상황, 중간 보고)은 영어가 아닌 한글로 쓴다.

## 쇼츠 제작
- 지식 쇼츠 제작 순서·도구·주의점은 `shorts/WORKFLOW.md`에 정리되어 있다. 이어서 작업할 때 먼저 읽는다.
- 편 번호: 「예금 vs 적금」과 「은행의 탄생」은 둘 다 5편이다 (사용자 지정). 다음 편은 6편.
- 「은행의 탄생」(5편)부터 영상 길이는 2분(120초), 내용 분량은 그대로, TTS 속도는 1.2배(`RATE = 1.2`)로 만든다. 자세한 내용은 `shorts/WORKFLOW.md`의 「2분 규격」.

## 완성 파일 전달
- 완성된 결과물(영상, 이미지, 문서 등 최종 파일)은 사용자의 Google Drive에 업로드한다.
- Google Drive 커넥터가 세션에 연결되어 있지 않으면, 업로드하지 못했다고 알리고
  https://claude.ai/customize/connectors 에서 연결한 뒤 새 세션을 열어 달라고 안내한다.
- 중간 산출물(스크래치, 테스트 렌더)은 업로드하지 않는다.
- Drive 커넥터는 파일 내용을 base64로 한 번에 보내야 해서 큰 바이너리(영상 등)는 올릴 수 없다.
  그런 파일은 GitHub 링크를 담은 메모를 Drive 폴더에 올리고, 사용자에게 그렇게 했다고 말한다.
- 기존 폴더: "복리의 마법 쇼츠" (id 13pq1Rpo-BD7anVeYfYg30VEEplezJ6Ff), "72의 법칙 쇼츠" (id 1-bXT4wqmQr0SQ5y7Cjikz61cpqiFsU-r), "4%의 법칙 쇼츠" (id 1d5LAWlVkBuNWuHLhUwDPeFMI2lATuccV), "적립식 vs 거치식 쇼츠" (id 1ROEb8W9iU2bGKot9KzdwNHegwlnVwfJR), "예금 vs 적금 쇼츠" (id 1-Pjspc__xyiAxM2nltxYdcsC2omMJrRg), "은행의 탄생 쇼츠" (id 1B_Z-pxMtxFYA745ITXJIy8up5qYzSdsL)
- 새 편은 Drive에도 새 폴더를 만들어 올린다.
