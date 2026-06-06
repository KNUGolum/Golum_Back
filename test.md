# 테스트 계획

## 1. 테스트 대상

본 테스트 계획은 현재 `Golum_Back` 저장소에 구현된 FastAPI 백엔드 기능을 기준으로 한다. 세부 테스트 케이스는 이후 항목에서 블랙박스 테스트와 화이트박스 테스트로 나누어 설계한다.

### 1.1 인증 및 사용자 관리

- 이메일/닉네임 중복 확인
- 회원가입
- 로그인
- 토큰 재발급 및 로그아웃
- 사용자 정보 및 크레딧 조회
- 닉네임 변경
- 인증 필요 API 접근 제어

### 1.2 투표 게시물

- 투표 생성
- 투표 목록 조회
- 투표 상세 조회
- 투표 상태별 조회
- 투표 목록 정렬 및 페이지 단위 조회
- 내가 참여한 투표 조회
- 투표 상태별 사용자 액션 정보 조회

### 1.3 투표 참여

- 투표하기
- 투표 참여 제한
- 투표 이력 조회
- 투표 참여 보상 크레딧 지급

### 1.4 베팅

- 베팅하기
- 베팅 참여 제한
- 베팅 포기하기
- 베팅 참여 보상 크레딧 지급
- 베팅 이력 조회

### 1.5 투표 결과 판정 및 정산

- 투표 결과 판정
- 승리/무승부/무효 결과 처리
- 배당금 계산
- 정산 처리
- 정산 상태 기록
- 만료된 투표 자동 판정 및 정산

### 1.6 칭호 상점

- 칭호 상점 목록 조회
- 칭호 구매
- 보유 칭호 목록 조회
- 칭호 장착 및 해제
- 칭호 구매/장착 제한

### 1.7 WebSocket 알림

- WebSocket 연결
- WebSocket 연결 해제
- 투표 종료 및 정산 완료 알림

### 1.8 데이터 및 실행 환경

- DB 연결 설정
- DB 테이블 자동 생성
- Docker Compose 기반 실행
- Seed 데이터 초기화
- 스케줄러 시작 및 종료

## 2. 테스트 케이스 설계

테스트 케이스는 테스트 수준에 따라 단위 테스트, 통합 테스트, 시스템 테스트로 나누어 설계한다. 단위 테스트는 블랙박스 관점과 화이트박스 관점을 모두 적용하고, 통합 테스트와 시스템 테스트는 세부 내부 분기보다 연결 결과와 전체 동작 확인이 중요하므로 블랙박스 관점을 중심으로 설계한다.

블랙박스 테스트는 요구사항과 API의 입력·출력을 기준으로 선정하며, 정상 입력, 잘못된 입력, 필수값 누락, 경계값, 존재하지 않는 데이터, 중복 요청, 인증 오류, 실행 불가 상태를 확인한다.

화이트박스 테스트는 실제 코드 내부 구조와 실행 흐름을 기준으로 선정하며, 조건 분기, 정상/예외 경로, 반복문 실행 횟수, DB 상태 변경, 의존 함수 호출 여부, 주요 변수의 생성과 변경 흐름을 확인한다.

현재 라우터에는 투표 결과 판정과 정산을 수동으로 호출하는 공개 API가 등록되어 있지 않다. 따라서 결과 판정과 정산은 공개 API 블랙박스 테스트가 아니라 단위 테스트, 통합 테스트의 CRUD 검증, 시스템 테스트의 스케줄러 동작 검증에서 다룬다.

### 테스트 수준별 대상 분류

1항목에서 선정한 테스트 대상은 아래 기준으로 단위 테스트, 통합 테스트, 시스템 테스트에 배치한다. 테스트 수의 비율을 고정하기보다는, 함수 내부 분기와 경계값은 단위 테스트에 두고, 여러 계층이 함께 동작해야 확인되는 항목만 통합 테스트와 시스템 테스트로 분리한다. 따라서 단위 테스트는 CRUD 함수, 스키마, 유틸리티, 스케줄러 내부 함수처럼 분기와 예외 경로가 많은 대상을 중심으로 상대적으로 많이 선정한다.

| 테스트 대상 영역 | 단위 테스트 | 통합 테스트 | 시스템 테스트 |
| --- | --- | --- | --- |
| 인증 및 사용자 관리 | 비밀번호 해시/검증, JWT 생성/디코딩, 입력 스키마 검증, 사용자 CRUD 함수 분기, endpoint 결과 코드 매핑 | 회원가입, 로그인, 토큰 재발급, 로그아웃, 보호 API 인증 의존성과 DB 연동 | 회원가입부터 로그아웃까지의 전체 인증 흐름 |
| 투표 게시물 | 투표 종료 판단, 사용자 액션 상태 계산, 득표율 계산, 선택지 매핑, 결과 계산, 목록 필터/정렬/페이지 계산 | 투표 생성, 목록 조회, 상세 조회, 상태/정렬/페이지/mine query 응답 | 사용자가 투표를 만들고 다른 사용자가 참여하는 전체 흐름 |
| 투표 참여 | 선택값 스키마 검증, 투표 가능/불가 조건 분기 | 투표 API와 Vote/PollOption/PollStat/User DB 변경 연동 | 투표 참여 후 목록/상세 상태가 바뀌는 사용자 흐름 |
| 베팅 | 베팅 입력 스키마 검증, 베팅 가능/불가 조건 분기, 베팅 포기 로직 | 베팅 API와 Bet/User DB 변경 연동, 베팅 이력 조회 | 투표 후 베팅하고 상세 상태와 크레딧이 바뀌는 사용자 흐름 |
| 투표 결과 판정 및 정산 | 승리/무승부/무효 판정, 배당금 계산, 정산 분기 | 공개 수동 API가 없으므로 별도 통합 API 케이스는 두지 않음 | 만료 투표 자동 판정, 자동 정산, 정산 후 상태 확인 |
| 칭호 상점 | 구매/장착 가능 조건 분기, 보유 목록 조회 함수 | 상점 조회, 구매, 장착/해제 API와 DB 연동 | 칭호 조회, 구매, 장착, 인벤토리 확인 전체 흐름 |
| WebSocket 알림 | 연결 저장/삭제, 개인/전체 메시지 전송 함수, WebSocket endpoint 해제 경로 | WebSocket 연결/해제와 manager 연동 | 실제 WebSocket 연결에서 투표 종료/정산 알림 수신 |
| 데이터 및 실행 환경 | 환경변수 설정, DB 세션 lifecycle, timezone 설정, 라우터 등록, 스케줄러 lifecycle | API와 테스트 DB 연동 | Docker Compose 실행, DB 테이블 자동 생성, seed 데이터 초기화, 서버 헬스 체크 |

### 2.1 단위 테스트

단위 테스트는 함수, 메서드, 클래스와 같이 작은 코드 단위가 의도한 대로 동작하는지 확인하는 테스트이다. 외부 시스템과의 연결은 최소화하고, 개별 로직의 반환값, 조건 분기, 예외 처리 등을 검증한다.

#### 2.1.1 블랙박스 관점

단위 테스트의 블랙박스 관점은 내부 구현을 몰라도 입력값만으로 검증할 수 있는 Pydantic 요청 스키마 검증에 한정한다. 함수 내부 조건 분기, 상태 변경, 계산 로직은 화이트박스 테스트에서 다룬다.

| 테스트 ID | 테스트 대상 | 테스트 시나리오 | 사전 조건 | 입력값 | 기대 결과 |
| --- | --- | --- | --- | --- | --- |
| UT-BB-SCHEMA-01 | 회원가입/로그인 입력 검증 | 이메일 형식이 잘못되거나 필수값이 누락된 입력을 검증한다. | 별도 사전 조건 없음 | 잘못된 email, password 누락 | 검증 실패가 발생한다. API에서는 `422 Unprocessable Entity`로 처리된다. |
| UT-BB-SCHEMA-02 | 투표 생성 입력 검증 | 투표 진행 시간의 경계값을 검증한다. | 별도 사전 조건 없음 | `durationHours=0`, `1`, `24`, `25` | 1과 24는 통과, 0과 25는 검증 실패 |
| UT-BB-SCHEMA-03 | 투표 선택값 검증 | 허용되지 않는 투표 선택값을 검증한다. | 별도 사전 조건 없음 | `selection=A`, `B`, `C` | A/B는 통과, C는 검증 실패 |
| UT-BB-SCHEMA-04 | 베팅 입력 검증 | 베팅 선택값과 금액 경계값을 검증한다. | 별도 사전 조건 없음 | `optionId=A/B/C`, `amount=-1/0/100` | A/B와 0 이상 금액은 통과, C와 음수 금액은 검증 실패 |
| UT-BB-SCHEMA-05 | 칭호 장착 입력 검증 | 칭호 장착/해제 요청의 titleId 입력 형식을 검증한다. | 별도 사전 조건 없음 | `titleId=1`, `None`, 잘못된 타입 | 정수와 None은 통과, 잘못된 타입은 검증 실패 |

#### 2.1.2 화이트박스 관점

| 테스트 ID | 코드 대상 | 검증 요소 | 실행 경로·조건 | 사전 상태·Mock | 입력값 | 기대 결과 |
| --- | --- | --- | --- | --- | --- | --- |
| UT-WB-AUTH-01 | `app/core/security.py::hashPassword`, `verifyPassword` | 비밀번호 해시와 검증 경로 | 같은 비밀번호 검증, 다른 비밀번호 검증 | 별도 Mock 없음 | plainPassword, hashedPassword | 같은 비밀번호는 `True`, 다른 비밀번호는 `False` |
| UT-WB-AUTH-02 | `app/core/security.py::createAccessToken`, `createRefreshToken`, `decodeToken` | 토큰 payload 생성과 JWT 예외 분기 | 정상 토큰 디코딩, 잘못된 토큰 디코딩 | settings의 SECRET_KEY, ALGORITHM 사용 | subject, invalid token | 정상 토큰은 payload 반환, 잘못된 토큰은 `None` 반환 |
| UT-WB-POLL-01 | `app/crud/poll_detail.py::isPollEnded`, `isPollActive` | 종료 상태 조건식 | ENDED, INVALID, end_time 과거/미래 | Poll 객체 상태별 준비 | poll, now | 종료 여부와 활성 여부가 규칙과 일치 |
| UT-WB-POLL-02 | `app/crud/poll_detail.py::getPollActionState` | 사용자 액션 상태 계산 | 생성자/참여자/미참여자, 투표 여부, 베팅 여부, 종료 여부 | Poll, Vote, Bet 객체 조합 준비 | poll, userId, myVote, myBet, now | canVote, canBet, hasVoted, hasBet, resultsVisible 반환값 일치 |
| UT-WB-POLL-03 | `app/crud/poll_detail.py::calculateVoteRatio` | 0 나눗셈 방지와 반올림 | totalVotes 0, totalVotes 양수 | 별도 Mock 없음 | voteCount, totalVotes | 0표는 0.0, 양수는 소수 둘째 자리 반올림 |
| UT-WB-POLL-04 | `app/crud/poll_detail.py::resolveOptionBySelection`, `getMySelection` | A/B 선택지 매핑 | A, B, 잘못된 선택값, 옵션 개수 부족 | 정렬된 PollOption 목록 준비 | options, selection 또는 myVote | 올바른 option 또는 A/B 반환, 불가 시 `None` |
| UT-WB-POLL-05 | `app/crud/poll_detail.py::calculatePollResult`, `calculatePollResultStatus` | 승리/무승부/무효 판정 | A 승리, B 승리, 무승부, 총 투표 0, 옵션 개수 부족 | PollOption 목록을 케이스별로 준비 | options, isEnded | winningOptionId, isDraw, resultStatus가 규칙과 일치 |
| UT-WB-PAYOUT-01 | `app/crud/payout.py::calculateRewardAmount` | 배당 계산 | 일반 승리와 무승부 | 별도 Mock 없음 | betAmount, isDraw, multiplier | 일반 승리는 `amount * 1.5`, 무승부는 원금 반환 |
| UT-WB-WS-01 | `app/core/websocket.py::ConnectionManager.connect`, `disconnect` | 연결 저장과 제거 | 새 사용자 연결, 연결된 사용자 제거, 없는 사용자 제거 | WebSocket Mock, active_connections 준비 | user_id, websocket | accept 호출, active_connections 추가/삭제 |
| UT-WB-WS-02 | `app/core/websocket.py::send_personal_message`, `broadcast` | 메시지 전송 반복 | 개인 전송, 전체 전송, 전송 중 예외 | WebSocket Mock 여러 개 준비 | message, user_id | 대상 WebSocket에 send_json 호출, broadcast는 전체 연결 순회 |
| UT-WB-WS-03 | `app/api/endpoints/websocket.py::websocket_endpoint` | WebSocket receive loop와 해제 경로 | 정상 연결, WebSocketDisconnect, 일반 예외 | manager와 WebSocket receive_text Mock | websocket, user_id | connect 호출 후 수신 대기, disconnect/예외 시 manager.disconnect 호출 |
| UT-WB-ENV-01 | `app/core/config.py::Settings` | 환경변수 기본값과 override | 환경변수 있음/없음 | os.getenv 또는 환경변수 상태 준비 | DATABASE_URL, SECRET_KEY 등 | 환경변수가 있으면 해당 값, 없으면 기본값 사용 |
| UT-WB-AUTH-03 | `app/crud/user.py::createUser` | 사용자 생성 데이터 흐름 | 신규 사용자 생성 경로 | DB 세션 Mock, 중복 없음 | UserCreate | User 생성, credit 1000, password_hash 저장 |
| UT-WB-AUTH-04 | `app/crud/user.py::upsertRefreshToken` | insert/update 분기 | 기존 AuthToken 없음, 기존 AuthToken 있음 | AuthToken 조회 결과를 케이스별로 Mock | userId, refreshToken, expiresAt | 신규 생성 또는 기존 token/expires_at 갱신 |
| UT-WB-AUTH-05 | `app/crud/user.py::deleteRefreshToken` | 삭제 분기 | 저장된 토큰 있음, 저장된 토큰 없음 | AuthToken 조회 결과를 케이스별로 Mock | userId | 있으면 삭제 후 객체 반환, 없으면 `None` 반환 |
| UT-WB-AUTH-06 | `app/crud/user.py::getUserCredit`, `updateNickname` | 사용자 존재 여부 분기 | 사용자 있음, 사용자 없음 | User 조회 결과를 케이스별로 Mock | userId, newNickname | credit 반환 또는 None, nickname 변경 또는 None |
| UT-WB-AUTH-07 | `app/api/deps.py::getDb` | 세션 lifecycle | dependency 종료 경로 | SessionLocal Mock | 없음 | yield 후 close 호출 |
| UT-WB-AUTH-08 | `app/api/deps.py::getCurrentUser` | 인증 예외 분기 | 정상 토큰, 잘못된 토큰, userId 없음, 사용자 없음 | jwt.decode와 User 조회 결과 Mock | bearer token | 정상은 User 반환, 실패는 `401` 예외 |
| UT-WB-AUTH-09 | `app/api/endpoints/auth.py::signUp`, `signIn`, `reissueAccessToken`, `logOut` | endpoint 결과 매핑 | 중복 이메일/닉네임, 로그인 실패, refresh token 불일치/만료, 로그아웃 대상 없음 | userCrud와 token 함수 반환값을 케이스별로 Mock | 인증 요청 데이터 | 각 결과 코드에 맞는 `HTTPException` 또는 정상 응답 반환 |
| UT-WB-AUTH-10 | `app/api/endpoints/auth.py::getMyInfo`, `getCurrentUserCredit`, `changeNickname` | 사용자 정보 endpoint 분기 | 내 정보 조회, credit 조회 성공/실패, 닉네임 중복/사용자 없음 | currentUser와 userCrud 반환값을 케이스별로 Mock | currentUser, NicknameUpdateRequest | UserResponse/CreditResponse 반환 또는 `404`/`409` 예외 |
| UT-WB-AUTH-11 | `app/api/endpoints/auth.py::checkEmailDuplication`, `checkNicknameDuplication`, `swaggerLogin` | 중복 확인과 Swagger 로그인 분기 | 이메일/닉네임 중복 있음/없음, Swagger 로그인 성공/실패 | userCrud, verifyPassword, token 함수 반환값 Mock | EmailCheckRequest, NicknameCheckRequest, OAuth2 formData | 중복 없음은 성공 메시지, 중복/로그인 실패는 `HTTPException`, Swagger 로그인 성공은 access token 반환 |
| UT-WB-POLL-06 | `app/crud/poll_detail.py::getRemainingSeconds` | 남은 시간 계산 | 종료됨, end_time 없음, 미래 end_time | Poll 객체와 now 준비 | poll, isEnded, now | 종료/시간 없음은 0, 진행 중은 남은 초 반환 |
| UT-WB-POLL-07 | `app/crud/poll_detail.py::getParticipantCount`, `getTotalBetCredits`, `getBetCreditsByOption` | 집계 결과 분기 | 데이터 있음, 데이터 없음 | DB query 결과 Mock | pollId | 참여자 수, 총 베팅 금액, 선택지별 베팅 금액 반환 |
| UT-WB-POLL-08 | `app/api/endpoints/poll_detail.py::buildOptionDetails` | 옵션 상세 조립 | 투표수 있음, 투표수 0, 베팅 있음/없음 | PollOption 목록과 betCreditsByOption 준비 | options, betCreditsByOption | voteRatio와 betCredits가 포함된 상세 목록 반환 |
| UT-WB-POLL-09 | `app/crud/poll_detail.py::hasBinaryOptions` | 선택지 개수 조건 | 옵션 0개, 1개, 2개, 3개 | PollOption 목록을 개수별로 준비 | options | 정확히 2개일 때만 `True`, 나머지는 `False` |
| UT-WB-POLL-10 | `app/crud/poll_detail.py::getEffectiveStatus` | 표시 상태 변환 분기 | ONGOING이 종료된 경우, 이미 ENDED/INVALID인 경우, 진행 중인 경우 | Poll 상태와 isEnded 값을 케이스별로 준비 | poll, isEnded | 종료된 ONGOING은 ENDED, 그 외에는 기존 status 반환 |
| UT-WB-POLL-11 | `app/crud/poll.py::createPoll` | 투표 생성 트랜잭션 분기 | 정상 생성, DB 예외 발생 | DB 세션 add/flush/commit/rollback Mock | PollCreateRequest, endTime, creatorId | Poll, option 2개, stat 생성 또는 예외 시 rollback |
| UT-WB-POLL-12 | `app/crud/poll.py::getPolls` | 목록 필터/정렬/페이지 계산 | ongoing, ended, latest, popular, page/limit 조합 | Query chain과 count/all 결과 Mock | status, sort, page, limit | 조건에 맞는 filter/order_by/offset/limit 호출 및 totalCount 반환 |
| UT-WB-POLL-13 | `app/crud/poll.py::getPolls` | 내가 참여한 투표 필터 | mine True/False, userId 있음/없음 | Vote join과 creator 제외 조건 Mock | mine, userId | mine 조건에서 참여 투표만 조회하고 본인 생성 투표는 제외 |
| UT-WB-POLL-14 | `app/crud/poll.py::getPolls` | 목록 응답 조립 반복문 | 조회 결과 없음, 옵션 1개/2개, 사용자 vote/bet 있음/없음 | Poll/PollStat/PollOption/Vote/Bet 조회 결과 Mock | pollRecords, userId | 빈 목록 또는 optionA/B와 action flag가 포함된 pollList 반환 |
| UT-WB-POLL-15 | `app/api/endpoints/poll.py::createPoll`, `getPollList` | endpoint 응답과 예외 매핑 | 생성 성공, 목록 성공, SQLAlchemyError, 일반 예외 | crudPoll과 now_kst_naive 반환값 Mock | PollCreateRequest, Query Parameter | 성공 응답 스키마 반환 또는 `500` 예외 반환 |
| UT-WB-POLL-16 | `app/api/endpoints/poll_detail.py::readPollDetail` | 상세 endpoint 분기와 응답 조립 | Poll 없음, 옵션 개수 오류, 생성자 조회, 투표/베팅 상태별 조회 | pollDetailCrud와 DB query 반환값 Mock | pollId, currentUser | `404`/`409` 예외 또는 상세 응답에 action flag, mySelection, winner 정보 반영 |
| UT-WB-VOTE-01 | `app/crud/vote.py::createVote` | 정상 투표 상태 변경 | 진행 중 투표, 생성자 아님, 중복 없음 | Poll, PollOption, PollStat, User 조회 Mock | pollId, userId, selection | Vote 생성, vote_count 증가, total_votes 증가, credit 증가 |
| UT-WB-VOTE-02 | `app/crud/vote.py::createVote` | 실패 분기 | Poll 없음, 종료됨, 생성자, 이미 투표함, 선택지 없음 | 각 상황별 DB 조회 Mock | pollId, userId, selection | `INVALID_POLL`, `POLL_CLOSED`, `CREATOR_CANNOT_VOTE`, `ALREADY_VOTED` 반환 |
| UT-WB-VOTE-03 | `app/crud/vote.py::getVoteHistoryByUserId` | 정렬 경로 | 투표 이력 있음, 없음 | Vote query 결과 Mock | userId | created_at 내림차순 목록 또는 빈 목록 반환 |
| UT-WB-VOTE-04 | `app/crud/vote.py::createVote` | 제외 항목 | User 또는 PollStat이 없는 상태에서 Vote가 생성되는 현재 구현 동작 확인 | PollOption은 존재하고 PollStat/User 조회 결과 None | pollId, userId, selection | 데이터 무결성 기대 결과와 모순되어 유효 케이스에서 제외하고 `UT-WB-VOTE-10`, `UT-WB-VOTE-11`으로 대체 |
| UT-WB-VOTE-05 | `app/api/endpoints/vote.py::submitVote`, `getMyVoteHistory` | endpoint 결과 매핑 | 투표 성공, 중복, 없는 투표, 종료, 생성자, 이력 있음/없음 | createVote와 getVoteHistoryByUserId 반환값 Mock | pollId, VoteRequest | 성공 응답 또는 결과 코드별 `HTTPException`, 이력 응답 목록 반환 |
| UT-WB-VOTE-06 | `app/crud/vote.py::createVote` | Vote 생성 데이터 | 정상 투표 시 Vote 생성만 확인 | 진행 중 Poll, 선택지, User, PollStat Mock | pollId, userId, selection | Vote 객체가 add되고 poll_id, user_id, option_id가 일치 |
| UT-WB-VOTE-07 | `app/crud/vote.py::createVote` | 선택지 투표수 상태 변경 | 정상 투표 시 option vote_count 증가만 확인 | vote_count가 있는 PollOption Mock | selection A | 대상 PollOption의 vote_count가 정확히 1 증가 |
| UT-WB-VOTE-08 | `app/crud/vote.py::createVote` | 전체 투표수 상태 변경 | 정상 투표 시 PollStat total_votes 증가만 확인 | PollStat Mock | selection A | PollStat이 있으면 total_votes가 정확히 1 증가 |
| UT-WB-VOTE-09 | `app/crud/vote.py::createVote` | 투표 보상 상태 변경 | 정상 투표 시 사용자 credit 보상만 확인 | User credit Mock | selection A | User가 있으면 credit이 100 증가 |
| UT-WB-VOTE-10 | `app/crud/vote.py::createVote` | User 누락 데이터 무결성 | User가 없는 상태에서 투표 시도 | User 조회 결과 None | userId | 사용자 없는 Vote 생성이 발생하지 않아야 함 |
| UT-WB-VOTE-11 | `app/crud/vote.py::createVote` | PollStat 누락 데이터 무결성 | PollStat이 없는 상태에서 투표 시도 | PollStat 조회 결과 None | pollId | 집계 불일치를 만들지 않아야 함 |
| UT-WB-VOTE-12 | `app/crud/vote.py::createVote` | 중복 투표 부작용 차단 | 이미 투표한 사용자 | Vote 조회 결과 있음 | pollId, userId | `ALREADY_VOTED`, Vote/credit/count 변경 없음 |
| UT-WB-VOTE-13 | `app/crud/vote.py::createVote` | 생성자 투표 부작용 차단 | 생성자가 본인 Poll에 투표 | poll.creator_id == userId | pollId, userId | `CREATOR_CANNOT_VOTE`, 변경 없음 |
| UT-WB-VOTE-14 | `app/crud/vote.py::createVote` | 종료 시간 경계 | poll end_time이 현재 시각과 같음 | now 고정 | pollId | 종료된 poll로 처리되어 `POLL_CLOSED` |
| UT-WB-VOTE-15 | `app/crud/vote.py::createVote` | 트랜잭션 실패 경로 | commit 실패 | db.commit이 SQLAlchemyError 발생 | 정상 투표 입력 | rollback 호출 및 예외 전파 |
| UT-WB-BET-01 | `app/crud/bet.py::createBet` | 정상 베팅 상태 변경 | 투표 완료, 같은 선택지, 잔액 충분, amount 양수 | User, Poll, Option, Vote 조회 Mock | userId, pollId, optionId, amount | Bet 생성, credit 차감 후 100 보상 |
| UT-WB-BET-02 | `app/crud/bet.py::createBet` | 베팅 포기 경로 | 투표 완료, 같은 선택지, amount 0 | User, Poll, Option, Vote 조회 Mock | amount 0 | Bet 생성, credit 차감 없음, 참여 보상 없음 |
| UT-WB-BET-03 | `app/crud/bet.py::createBet` | 실패 분기 | 사용자 없음, 음수 금액, Poll 없음, 종료됨, 투표 없음, 옵션 불일치, 중복, 잔액 부족 | 각 상황별 DB 조회 Mock | userId, pollId, optionId, amount | 각 상황에 맞는 실패 코드 반환 |
| UT-WB-BET-04 | `app/crud/bet.py::getBetHistoryByUserId` | 정렬 경로 | 베팅 이력 있음, 없음 | Bet query 결과 Mock | userId | created_at 내림차순 목록 또는 빈 목록 반환 |
| UT-WB-BET-05 | `app/crud/bet.py::createBet` | 선택지 유효성 분기 | 투표 옵션 개수 부족, optionId가 A/B가 아님 | PollOption 조회 결과와 요청 optionId를 케이스별로 Mock | optionId | 유효하지 않은 선택지는 `INVALID_POLL_OPTIONS` 또는 옵션 불일치 코드 반환 |
| UT-WB-BET-06 | `app/api/endpoints/bet.py::createBetParticipation`, `getMyBetHistory` | endpoint 결과 매핑 | 베팅 성공, 포기, 미투표, 종료, 중복, 잔액 부족, 이력 있음/없음 | crudBet 반환값을 결과 코드별로 Mock | pollId, BetCreate | 성공/포기 메시지 또는 결과 코드별 `HTTPException`, 이력 응답 목록 반환 |
| UT-WB-BET-07 | `app/crud/bet.py::createBet` | 베팅 금액 경계 | amount 1 베팅의 credit 변화 | User credit 1000, 투표 완료 | amount=1 | 1 credit 차감 후 참여 보상 100 credit 지급, 최종 credit 1099 |
| UT-WB-BET-08 | `app/crud/bet.py::createBet` | 베팅 금액 경계 | amount 99 베팅의 credit 변화 | User credit 1000, 투표 완료 | amount=99 | 99 credit 차감 후 참여 보상 100 credit 지급, 최종 credit 1001 |
| UT-WB-BET-09 | `app/crud/bet.py::createBet` | 베팅 금액 경계 | amount 100 베팅의 credit 변화 | User credit 1000, 투표 완료 | amount=100 | 차감 100과 보상 100으로 credit 순변화 없음 |
| UT-WB-BET-10 | `app/crud/bet.py::createBet` | 베팅 금액 경계 | amount 101 베팅의 credit 변화 | User credit 1000, 투표 완료 | amount=101 | credit 순감 1 |
| UT-WB-BET-11 | `app/crud/bet.py::createBet` | 베팅 포기 상태 | amount 0 베팅이 Bet과 hasBet 상태를 만드는지 확인 | 투표 완료, 중복 Bet 없음 | amount=0 | Bet 생성, credit 변화 없음 |
| UT-WB-BET-12 | `app/crud/bet.py::createBet` | 포기 후 재베팅 제한 | amount 0 Bet이 이미 있는 상태에서 유료 베팅 | alreadyBet Mock | amount>0 | `ALREADY_BET`, credit 변경 없음 |
| UT-WB-BET-13 | `app/crud/bet.py::createBet` | 선택지 불일치 차단 | 투표한 option과 다른 option에 베팅 | Vote option_id와 selectedOption.id 불일치 | optionId | `VOTE_OPTION_MISMATCH`, credit/Bet 변경 없음 |
| UT-WB-BET-14 | `app/crud/bet.py::createBet` | 잔액 부족 경계 | 잔액보다 1 큰 금액 베팅 | User credit 99 | amount=100 | `INSUFFICIENT_CREDIT`, credit/Bet 변경 없음 |
| UT-WB-BET-15 | `app/crud/bet.py::createBet` | 잔액 정확히 일치 경계 | 잔액과 같은 금액 베팅 | User credit 100 | amount=100 | 성공 후 참여 보상 100 credit이 남음 |
| UT-WB-BET-16 | `app/crud/bet.py::createBet` | 트랜잭션 실패 경로 | commit 실패 | db.commit이 SQLAlchemyError 발생 | 정상 베팅 입력 | rollback 호출 및 예외 전파 |
| UT-WB-RESULT-01 | `app/crud/poll_result.py::evaluatePollResult` | 판정 성공 경로 | 만료된 ONGOING 투표 | Poll과 PollOption 조회 Mock | pollId | poll.status가 ENDED 또는 INVALID로 변경 |
| UT-WB-RESULT-02 | `app/crud/poll_result.py::evaluatePollResult` | 판정 실패 분기 | Poll 없음, 이미 판정됨, 아직 진행 중, 옵션 부족 | 각 상황별 DB 조회 Mock | pollId | `POLL_NOT_FOUND`, `ALREADY_EVALUATED`, `POLL_STILL_ONGOING`, `NOT_ENOUGH_OPTIONS` 반환 |
| UT-WB-PAYOUT-02 | `app/crud/payout.py::payoutDividends` | 정산 성공 경로 | 종료된 투표, 승자/패자 베팅 존재 | Poll, Option, Bet, User, Settlement 조회 Mock | pollId | Bet result/reward, User credit, Settlement status 변경 |
| UT-WB-PAYOUT-03 | `app/crud/payout.py::payoutDividends` | 무승부 및 반복문 경로 | 무승부, 베팅 0개/1개/여러 개 | Bet 목록을 개수별로 Mock | pollId | 무승부는 원금, 반복 횟수별 payoutUserCount 반영 |
| UT-WB-PAYOUT-04 | `app/crud/payout.py::payoutDividends` | 정산 실패 분기 | 이미 정산됨, Poll 없음, 미종료, 옵션 부족 | 각 상황별 DB 조회 Mock | pollId | `ALREADY_SETTLED`, `POLL_NOT_FOUND`, `POLL_NOT_ENDED`, `INVALID_POLL_OPTIONS` 반환 |
| UT-WB-PAYOUT-05 | `app/crud/payout.py::payoutDividends` | 정산 대상 사용자 조회 분기 | 승자 Bet은 있으나 해당 User 조회 실패 | Bet 목록과 User 조회 결과 None Mock | pollId | Bet result/reward는 계산되며 존재하는 사용자 credit만 갱신 |
| UT-WB-TITLE-01 | `app/crud/title.py::purchaseTitle` | 구매 성공/실패 분기 | 성공, 사용자 없음, 칭호 없음, 이미 보유, 잔액 부족 | User, Title, UserTitle 조회 Mock | userId, titleId | 성공 시 UserTitle 생성/credit 감소, 실패 시 코드 반환 |
| UT-WB-TITLE-02 | `app/crud/title.py::equipTitle`, `unequipTitle` | 장착/해제 분기 | 성공, 사용자 없음, 미보유, 이미 장착, 해제 | User, UserTitle 조회 Mock | userId, titleId | equipped_title_id 변경 또는 실패 코드 반환 |
| UT-WB-TITLE-03 | `app/crud/title.py::getShopTitles`, `getOwnedTitleIds`, `getUserInventoryTitles` | 조회 경로 | 보유 데이터 있음, 없음, ownership table 없음 | DB query와 inspect 결과 Mock | userId | 상점 목록, 보유 titleId set, 인벤토리 목록 반환 |
| UT-WB-TITLE-04 | `app/crud/title.py::unequipTitle` | 해제 단독 분기 | 사용자 있음, 사용자 없음 | User 조회 결과를 케이스별로 Mock | userId | 사용자가 있으면 equipped_title_id가 None, 없으면 `USER_NOT_FOUND` 반환 |
| UT-WB-TITLE-05 | `app/api/endpoints/title.py::getTitleShopList`, `purchaseTitle`, `updateEquippedTitle`, `getTitleInventory` | endpoint 결과 매핑 | 상점 조회, 구매 실패 코드, 장착/해제 실패 코드, 인벤토리 있음/없음 | title CRUD 반환값을 케이스별로 Mock | titleId, EquipTitleRequest | 정상 응답 또는 결과 코드별 `HTTPException`, 보유 여부와 장착 여부 반영 |
| UT-WB-TITLE-06 | `app/crud/title.py::purchaseTitle` | 구매 금액 경계 | title 가격과 credit이 정확히 같은 경우 | User credit == title.price | userId, titleId | 구매 성공, credit 0, UserTitle 생성 |
| UT-WB-TITLE-07 | `app/crud/title.py::purchaseTitle` | 잔액 부족 경계 | title 가격보다 credit이 1 부족한 경우 | User credit = price - 1 | userId, titleId | `INSUFFICIENT_CREDIT`, credit/UserTitle 변경 없음 |
| UT-WB-TITLE-08 | `app/crud/title.py::purchaseTitle` | 중복 구매 차단 | 이미 보유한 title 구매 | UserTitle 조회 결과 있음 | userId, titleId | `ALREADY_OWNED`, credit 변경 없음 |
| UT-WB-TITLE-09 | `app/crud/title.py::purchaseTitle` | 0원 칭호 경계 | price 0 title 구매 | title.price = 0 | userId, titleId | 구매 성공, credit 변화 없음 |
| UT-WB-TITLE-10 | `app/crud/title.py::purchaseTitle` | 음수 가격 방어 | 음수 price title 구매 | title.price < 0 | userId, titleId | credit이 증가하지 않아야 함 |
| UT-WB-TITLE-11 | `app/crud/title.py::purchaseTitle` | 트랜잭션 실패 경로 | commit 실패 | db.commit이 SQLAlchemyError 발생 | userId, titleId | rollback 호출 및 예외 전파 |
| UT-WB-TITLE-12 | `app/crud/title.py::equipTitle` | 미보유 장착 차단 | 보유하지 않은 title 장착 | UserTitle 조회 결과 None | userId, titleId | `TITLE_NOT_OWNED`, equipped_title_id 변경 없음 |
| UT-WB-TITLE-13 | `app/crud/title.py::equipTitle` | 중복 장착 차단 | 이미 장착한 title 재장착 | equipped_title_id == titleId | userId, titleId | `ALREADY_EQUIPPED`, 상태 유지 |
| UT-WB-TITLE-14 | `app/crud/title.py::unequipTitle` | 해제 no-op 경로 | 장착 칭호가 없는 상태에서 해제 | equipped_title_id None | userId | 성공 여부와 equipped_title_id None 유지 확인 |
| UT-WB-ENV-02 | `app/db/session.py::setTimeZone` | DB 연결 이벤트 | connect event 실행 | DBAPI connection/cursor Mock | dbapiConnection | `SET TIME ZONE 'Asia/Seoul'` 실행 후 cursor close |
| UT-WB-ENV-03 | `app/core/time.py::now_kst`, `now_kst_naive` | 시간대 변환 | timezone 포함 KST 반환, timezone 제거 반환 | datetime.now 결과 또는 ZoneInfo 기준 준비 | 없음 | now_kst는 Asia/Seoul timezone 포함, now_kst_naive는 tzinfo 없는 datetime 반환 |
| UT-WB-ENV-04 | `app/main.py::readRoot`, `start_scheduler`, `stop_scheduler` | 앱 보조 함수 분기 | root 응답, scheduler 미실행/실행 상태, shutdown 호출 | scheduler.running과 start/shutdown Mock | 없음 | root message 반환, 실행 중이 아니면 start 호출, 종료 시 shutdown 호출 |
| UT-WB-ENV-05 | `app/api/routers.py::apiRouter`, `app/main.py::app.include_router` | 라우터 등록 상태 | auth, vote, bet, websocket, poll, poll_detail, title router 포함, app에 `/api` prefix 등록 | apiRouter.routes와 app.routes 상태 준비 | 없음 | 주요 router prefix와 `/api` 하위 경로가 등록되어 있음 |
| UT-WB-SCHED-01 | `app/core/scheduler.py::check_and_evaluate_polls` | 만료 투표 조회 분기 | 만료 투표 없음, 만료 투표 있음 | SessionLocal과 Poll query Mock | 없음 | 없음이면 종료, 있으면 판정/정산 함수 호출 |
| UT-WB-SCHED-02 | `app/core/scheduler.py::send_notifications` | 알림 전송 분기 | winningOptionId 있음, 없음 | manager와 Bet query Mock | result_data | 항상 종료 알림 broadcast, winner가 있으면 개인 알림 전송 |
| UT-WB-SCHED-03 | `app/core/scheduler.py::send_notifications` | 승자 알림 반복문 | winningOptionId가 있고 승자 Bet이 0개, 1개, 여러 개인 경우 | manager와 Bet query 결과를 개수별로 Mock | result_data, poll_id | 승자 수만큼 개인 메시지를 보내고 전체 종료 알림은 1회 전송 |
| UT-WB-SCHED-04 | `app/core/scheduler.py::check_and_evaluate_polls` | 실패 경로와 자원 정리 | 판정 실패, 정산 실패, 처리 중 예외 발생 | evaluatePollResult, payoutDividends, SessionLocal Mock | 만료 Poll 목록 | 실패 시 다음 경로로 분기하고 예외 발생 여부와 관계없이 db.close 호출 |

### 2.2 통합 테스트

통합 테스트는 여러 컴포넌트가 서로 연결되었을 때 정상적으로 동작하는지 확인하는 테스트이다. FastAPI 백엔드에서는 라우터, 의존성, CRUD, 데이터베이스 등이 함께 올바르게 동작하는지를 검증한다.

개별 함수의 조건 분기, 경계값, 단독 반환값 검증은 단위 테스트에서 다룬다. 통합 테스트에서는 API 요청이 라우터와 인증 의존성을 지나 CRUD를 호출하고, 실제 테스트 DB 상태가 함께 변경되는지에 집중한다.

#### 2.2.1 블랙박스 관점

| 테스트 ID | 테스트 대상 | API / Method | 테스트 시나리오 | 사전 조건 | 입력값·요청 | 기대 결과 |
| --- | --- | --- | --- | --- | --- | --- |
| IT-BB-AUTH-01 | 인증 흐름 | `POST /api/auth/signup`, `POST /api/auth/signin`, `POST /api/auth/reissue`, `POST /api/auth/logout` | 회원가입, 로그인, 토큰 재발급, 로그아웃 연동을 확인한다. | 중복되지 않는 사용자 정보와 테스트 DB가 준비되어 있다. | 회원가입/로그인/재발급/로그아웃 요청 | 사용자와 AuthToken 상태가 API 응답과 함께 올바르게 변경 |
| IT-BB-AUTH-02 | 보호 API 인증 제어 | `GET /api/auth/me`, `GET /api/auth/credit`, `PUT /api/auth/nickname` | 인증 토큰이 필요한 API의 접근 제어와 사용자 DB 조회 연동을 확인한다. | 테스트 사용자와 유효/무효 토큰이 준비되어 있다. | Authorization Header 있음/없음/잘못됨, 닉네임 변경 요청 | 유효 토큰은 정상 응답, 없거나 잘못된 토큰은 `401`, DB 상태는 요청 결과와 일치 |
| IT-BB-POLL-01 | 투표 생성 및 조회 | `POST /api/poll`, `GET /api/poll`, `GET /api/polls/{pollId}` | 투표 생성 후 목록과 상세에서 조회되는지 확인한다. | 인증된 사용자와 테스트 DB가 준비되어 있다. | 투표 생성 요청 후 목록/상세 조회 | Poll, PollOption, PollStat이 생성되고 조회 응답에 반영 |
| IT-BB-POLL-02 | 투표 목록 조건 조회 | `GET /api/poll` | 목록의 상태, 정렬, 페이지, 내가 참여한 투표 조건이 응답에 반영되는지 확인한다. | 여러 상태의 투표와 사용자 참여 데이터가 준비되어 있다. | `status`, `sort`, `page`, `limit`, `mine` Query Parameter | 조건에 맞는 목록과 totalCount/currentPage가 반환되고 사용자 action flag가 반영 |
| IT-BB-VOTE-01 | 투표 참여 | `POST /api/poll/{pollId}/vote`, `GET /api/polls/{pollId}` | 투표 후 상세 상태와 집계 값이 변경되는지 확인한다. | 진행 중 투표와 참여 가능한 사용자가 있다. | selection A/B, 인증 토큰 | Vote 생성, vote_count/total_votes/credit 증가, 상세 상태 변경 |
| IT-BB-BET-01 | 베팅 참여 | `POST /api/bets/{pollId}/bet`, `GET /api/bets/history` | 투표 후 베팅하고 이력에서 확인한다. | 사용자가 해당 투표에 먼저 투표했다. | optionId, amount, 인증 토큰 | Bet 생성, credit 변경, 베팅 이력 반환 |
| IT-BB-TITLE-01 | 칭호 구매 및 장착 | `GET /api/titles/shop`, `POST /api/titles/{titleId}/purchase`, `PUT /api/titles/equipped` | 칭호 조회, 구매, 장착이 연동되는지 확인한다. | 칭호 데이터와 충분한 credit이 있다. | titleId, 인증 토큰 | UserTitle 생성, credit 감소, equippedTitleId 변경 |
| IT-BB-WS-01 | WebSocket 연결 및 해제 | `WebSocket /api/ws/{user_id}` | WebSocket endpoint와 ConnectionManager의 연결/해제 연동을 확인한다. | API 앱이 테스트 클라이언트로 실행 중이다. | user_id path parameter, WebSocket connect/disconnect | 연결이 수락되고 해제 후 같은 사용자 연결 상태가 정리됨 |

통합 테스트의 화이트박스 관점은 별도 케이스로 선정하지 않는다. 라우터, 인증 의존성, CRUD, DB의 연결 여부는 위 블랙박스 통합 테스트의 기대 결과에서 실제 DB 상태 변경까지 함께 확인하며, 각 함수 내부 분기와 예외 경로는 단위 테스트에서 다룬다.

### 2.3 시스템 테스트

시스템 테스트는 개발된 소프트웨어 전체를 실제 또는 실제와 유사한 실행 환경에서 검증하는 테스트이다. API 서버, 데이터베이스, 스케줄러, WebSocket, Docker 실행 환경 등을 포함한 전체 시스템의 동작을 확인한다.

시스템 테스트는 세부 분기보다 실제 실행 환경에서 전체 서비스가 연결되어 동작하는지를 확인한다. 따라서 Docker 실행, 주요 사용자 흐름, 자동 스케줄러, WebSocket 알림처럼 단위 또는 통합 테스트만으로 확인하기 어려운 항목만 선정한다.

#### 2.3.1 블랙박스 관점

| 테스트 ID | 테스트 대상 | 테스트 시나리오 | 사전 조건 | 수행 절차 | 기대 결과 |
| --- | --- | --- | --- | --- | --- |
| ST-BB-ENV-01 | Docker Compose 기반 실행 | DB와 API 컨테이너를 실제 실행하고 앱 시작 시 DB 테이블이 생성되는지 확인한다. | Docker와 `.env`가 준비되어 있다. | `docker compose up --build -d` 실행 후 health/root API와 DB 접속 확인 | API는 `8002`, DB는 `5434`로 접근 가능하고 주요 테이블이 생성됨 |
| ST-BB-ENV-02 | Seed 데이터 초기화 | seed.sql을 실제 DB에 적용해 데모 데이터로 시스템을 초기화한다. | DB 컨테이너가 실행 중이고 seed.sql이 준비되어 있다. | `docker compose exec -T db psql -U golum_user -d golum_db < seed.sql` 실행 후 로그인/목록 조회 | 데모 계정과 초기 투표/칭호 데이터가 조회 가능 |
| ST-BB-E2E-01 | 핵심 사용자 흐름 | 인증 후 투표 생성, 투표 참여, 베팅, 칭호 구매를 순서대로 수행한다. | API와 DB가 실행 중이고 seed 데이터가 준비되어 있다. | 로그인 → 투표 생성 → 투표 → 베팅 → 칭호 구매/장착 | 주요 API가 연속 성공하고 DB 상태와 응답 상태가 일관됨 |
| ST-BB-E2E-02 | 자동 판정/정산 및 알림 흐름 | 만료된 투표가 자동 판정·정산되고 WebSocket 알림을 수신한다. | WebSocket 연결, 만료 대상 투표, 베팅 데이터, 스케줄러 실행 상태 | WebSocket 연결 후 스케줄러 주기 대기 또는 작업 실행 | 투표/베팅/정산 상태가 변경되고 종료/정산 알림 수신 |

시스템 테스트의 화이트박스 관점은 별도 케이스로 선정하지 않는다. 시스템 테스트는 실제 실행 환경에서 API 서버, DB, 스케줄러, WebSocket이 함께 동작하는지를 확인하는 단계이므로 내부 함수 분기는 단위 테스트로 분리하고, 시스템 단계에서는 사용자 관점의 전체 동작과 최종 상태만 확인한다.

### 2.4 테스트 ID별 적용 기법

각 테스트 케이스에 적용한 테스트 설계 기법은 다음과 같다. 한 테스트 케이스에 여러 기법이 함께 적용된 경우 쉼표로 함께 표시하였다.

| 테스트 ID | 테스트 수준 | 관점 | 적용 기법 | 적용 이유 |
| --- | --- | --- | --- | --- |
| UT-BB-SCHEMA-01 | 단위 | 블랙박스 | 동치분할 | 정상 입력 그룹과 비정상 입력 그룹을 나누어 스키마 검증 결과를 확인 |
| UT-BB-SCHEMA-02 | 단위 | 블랙박스 | 동치분할, 경곗값분석 | 허용 입력과 비허용 입력을 나누고 최소/최대 또는 0/양수 경계를 확인 |
| UT-BB-SCHEMA-03 | 단위 | 블랙박스 | 동치분할 | 정상 입력 그룹과 비정상 입력 그룹을 나누어 스키마 검증 결과를 확인 |
| UT-BB-SCHEMA-04 | 단위 | 블랙박스 | 동치분할, 경곗값분석 | 허용 입력과 비허용 입력을 나누고 최소/최대 또는 0/양수 경계를 확인 |
| UT-BB-SCHEMA-05 | 단위 | 블랙박스 | 동치분할 | 정상 입력 그룹과 비정상 입력 그룹을 나누어 스키마 검증 결과를 확인 |
| UT-WB-AUTH-01 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-AUTH-02 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-POLL-01 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-POLL-02 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-POLL-03 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-POLL-04 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-POLL-05 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-PAYOUT-01 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-WS-01 | 단위 | 화이트박스 | 데이터 흐름 테스팅 | 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-WS-02 | 단위 | 화이트박스 | 루프 테스팅, 데이터 흐름 테스팅 | 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-WS-03 | 단위 | 화이트박스 | 기본경로 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-ENV-01 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-AUTH-03 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-AUTH-04 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-AUTH-05 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-AUTH-06 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-AUTH-07 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-AUTH-08 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-AUTH-09 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-AUTH-10 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-AUTH-11 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-POLL-06 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-POLL-07 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-POLL-08 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-POLL-09 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-POLL-10 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-POLL-11 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-POLL-12 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-POLL-13 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-POLL-14 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-POLL-15 | 단위 | 화이트박스 | 기본경로 테스팅, 루프 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-POLL-16 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-VOTE-01 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-VOTE-02 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-VOTE-03 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-VOTE-04 | 단위 | 화이트박스 | 데이터 흐름 테스팅 | 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-VOTE-05 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 루프 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-VOTE-06 | 단위 | 화이트박스 | 기본경로 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-VOTE-07 | 단위 | 화이트박스 | 기본경로 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-VOTE-08 | 단위 | 화이트박스 | 기본경로 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-VOTE-09 | 단위 | 화이트박스 | 기본경로 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-VOTE-10 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-VOTE-11 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-VOTE-12 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-VOTE-13 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-VOTE-14 | 단위 | 화이트박스 | 조건 테스팅, 경곗값분석 | if/else 조건과 상태별 True/False 경로를 확인; 금액, 잔액, 시간, 가격 등 경계값과 경계 주변 값을 확인 |
| UT-WB-VOTE-15 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-BET-01 | 단위 | 화이트박스 | 기본경로 테스팅, 데이터 흐름 테스팅, 경곗값분석 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-BET-02 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-BET-03 | 단위 | 화이트박스 | 조건 테스팅, 경곗값분석 | if/else 조건과 상태별 True/False 경로를 확인; 금액, 잔액, 시간, 가격 등 경계값과 경계 주변 값을 확인 |
| UT-WB-BET-04 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-BET-05 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-BET-06 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 루프 테스팅, 경곗값분석 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-BET-07 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-BET-08 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-BET-09 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-BET-10 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-BET-11 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-BET-12 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-BET-13 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-BET-14 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-BET-15 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-BET-16 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-RESULT-01 | 단위 | 화이트박스 | 기본경로 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인 |
| UT-WB-RESULT-02 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-PAYOUT-02 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-PAYOUT-03 | 단위 | 화이트박스 | 루프 테스팅 | 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-PAYOUT-04 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-PAYOUT-05 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-TITLE-01 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-TITLE-02 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-TITLE-03 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-TITLE-04 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-TITLE-05 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-TITLE-06 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-TITLE-07 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-TITLE-08 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-TITLE-09 | 단위 | 화이트박스 | 기본경로 테스팅, 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-TITLE-10 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅, 경곗값분석 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-TITLE-11 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-TITLE-12 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-TITLE-13 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-TITLE-14 | 단위 | 화이트박스 | 기본경로 테스팅, 데이터 흐름 테스팅 | 정상 실행 경로와 주요 실패 경로의 반환값을 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-ENV-02 | 단위 | 화이트박스 | 데이터 흐름 테스팅 | 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-ENV-03 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-ENV-04 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-ENV-05 | 단위 | 화이트박스 | 조건 테스팅 | if/else 조건과 상태별 True/False 경로를 확인 |
| UT-WB-SCHED-01 | 단위 | 화이트박스 | 조건 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 함수 실행 전후 객체 상태 변경과 DB 저장/수정/삭제 흐름을 확인 |
| UT-WB-SCHED-02 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-SCHED-03 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| UT-WB-SCHED-04 | 단위 | 화이트박스 | 조건 테스팅, 루프 테스팅, 데이터 흐름 테스팅 | if/else 조건과 상태별 True/False 경로를 확인; 목록/반복 처리에서 0회, 1회, 여러 회 또는 정렬 결과를 확인 |
| IT-BB-AUTH-01 | 통합 | 블랙박스 | 동치분할, 시나리오 테스트 | 정상/비정상 상태 또는 사용자 흐름을 API 요청과 DB 변경 결과로 확인 |
| IT-BB-AUTH-02 | 통합 | 블랙박스 | 동치분할, 경곗값분석, 시나리오 테스트 | 인증/조회 조건별 입력 그룹과 page/limit 같은 경계 조건을 API 흐름에서 확인 |
| IT-BB-POLL-01 | 통합 | 블랙박스 | 동치분할, 시나리오 테스트 | 정상/비정상 상태 또는 사용자 흐름을 API 요청과 DB 변경 결과로 확인 |
| IT-BB-POLL-02 | 통합 | 블랙박스 | 동치분할, 경곗값분석, 시나리오 테스트 | 인증/조회 조건별 입력 그룹과 page/limit 같은 경계 조건을 API 흐름에서 확인 |
| IT-BB-VOTE-01 | 통합 | 블랙박스 | 동치분할, 시나리오 테스트 | 정상/비정상 상태 또는 사용자 흐름을 API 요청과 DB 변경 결과로 확인 |
| IT-BB-BET-01 | 통합 | 블랙박스 | 동치분할, 시나리오 테스트 | 정상/비정상 상태 또는 사용자 흐름을 API 요청과 DB 변경 결과로 확인 |
| IT-BB-TITLE-01 | 통합 | 블랙박스 | 동치분할, 시나리오 테스트 | 정상/비정상 상태 또는 사용자 흐름을 API 요청과 DB 변경 결과로 확인 |
| IT-BB-WS-01 | 통합 | 블랙박스 | 동치분할, 시나리오 테스트 | 정상/비정상 상태 또는 사용자 흐름을 API 요청과 DB 변경 결과로 확인 |
| ST-BB-ENV-01 | 시스템 | 블랙박스 | 시나리오 테스트 | 실제 실행 환경에서 서버, DB, seed 적용 흐름이 동작하는지 확인 |
| ST-BB-ENV-02 | 시스템 | 블랙박스 | 시나리오 테스트 | 실제 실행 환경에서 서버, DB, seed 적용 흐름이 동작하는지 확인 |
| ST-BB-E2E-01 | 시스템 | 블랙박스 | 시나리오 테스트, 데이터 흐름 테스팅 | 실제 환경의 전체 사용자 흐름과 최종 DB/알림 상태 변화를 확인 |
| ST-BB-E2E-02 | 시스템 | 블랙박스 | 시나리오 테스트, 데이터 흐름 테스팅 | 실제 환경의 전체 사용자 흐름과 최종 DB/알림 상태 변화를 확인 |

## 3. 테스트 실행 결과

설계한 테스트 중 단위 테스트, 통합 테스트, 시스템 테스트를 실행하고 기대 결과와 실제 결과를 비교하였다.

실행 명령은 다음과 같다.

```bash
DATABASE_URL=postgresql://golum_user:golum_password@localhost:5434/golum_db .venv/bin/python -m pytest tests/v1/unit
DATABASE_URL=postgresql://golum_user:golum_password@localhost:5434/golum_db .venv/bin/python -m pytest tests/v2/unit
```

통합 테스트 실행 명령은 다음과 같다.

```bash
DATABASE_URL=postgresql://golum_user:golum_password@localhost:5434/golum_db .venv/bin/python -m pytest tests/v1/integration
```

시스템 테스트 실행 전 Docker Compose 환경을 기동하고 seed 데이터를 적용하였다.

```bash
docker compose up --build -d
docker compose exec -T db psql -U golum_user -d golum_db < seed.sql
```

시스템 테스트 실행 명령은 다음과 같다.

```bash
SYSTEM_BASE_URL=http://localhost:8002 SYSTEM_WS_URL=ws://localhost:8002 SYSTEM_DATABASE_URL=postgresql://golum_user:golum_password@localhost:5434/golum_db .venv/bin/python -m pytest tests/v1/system
```

### 3.1 테스트 결과 요약

| 테스트 수준 | 전체 | Pass | Fail | Blocked | 통과율 |
| --- | -: | -: | -: | -: | -: |
| 단위 테스트 | 95 | 92 | 3 | 0 | 96.84% |
| 통합 테스트 | 8 | 8 | 0 | 0 | 100% |
| 시스템 테스트 | 4 | 4 | 0 | 0 | 100% |
| 합계 | 107 | 104 | 3 | 0 | 97.20% |

통과율은 `Pass / (Pass + Fail) × 100`으로 계산하였다.

단위 테스트는 기존 단위 테스트와 핵심 도메인 단위 테스트를 합쳐 95개 유효 테스트 ID를 실행했다. 기존 단위 테스트는 75개 pytest 테스트 함수로 실행되어 `75 passed, 14 warnings`였고, 핵심 도메인 단위 테스트는 29개 pytest 테스트 함수로 실행되어 `26 passed, 3 failed`였다. 다만 기존 단위 테스트 중 `UT-WB-VOTE-04`는 User 또는 PollStat이 없어도 Vote가 생성되는 현재 구현 동작을 Pass로 기록했으나, 핵심 도메인 재점검에서 데이터 무결성 기대 결과와 모순되는 것으로 판단하여 유효 테스트 ID 집계에서 제외하고 `UT-WB-VOTE-10`, `UT-WB-VOTE-11` 실패 케이스로 대체하였다. 경고는 Pydantic/FastAPI deprecation warning과 passlib 관련 warning이며, 테스트 실패로 처리하지 않았다.

통합 테스트는 8개 테스트 ID를 8개 pytest 테스트 함수로 실행했으며, 실행 결과는 `8 passed, 15 warnings`이다. 경고는 TestClient, Pydantic/FastAPI deprecation warning과 passlib 관련 warning이며, 테스트 실패로 처리하지 않았다.

단위 테스트와 통합 테스트를 함께 실행한 최종 확인 결과는 `83 passed, 15 warnings`이다.

시스템 테스트는 4개 테스트 ID를 3개 pytest 테스트 함수로 실행했으며, 실행 결과는 `3 passed`이다. `ST-BB-ENV-01`과 `ST-BB-ENV-02`는 Docker 실행 환경과 seed 데이터 적용 여부를 하나의 pytest 함수에서 함께 확인했다. 시스템 테스트 첫 실행 중 `ST-BB-E2E-01`의 credit 기대값을 750으로 잘못 계산한 자동화 테스트 오류가 있었으며, 실제 정책 계산값인 850으로 수정 후 재실행하여 통과하였다. 애플리케이션 코드 수정은 없었다.

기존 단위, 통합, 시스템 테스트 전체를 `tests/v1`에서 함께 실행한 결과는 `86 passed, 15 warnings`이다. 이후 핵심 도메인 단위 테스트를 `tests/v2/unit`에서 추가 실행하여 `26 passed, 3 failed`가 나왔다.

### 3.2 세부 실행 결과

| 테스트 ID | 실행 회차 | 상태 | 결과 |
| --- | ---: | --- | --- |
| UT-BB-SCHEMA-01 | 1차 | Pass | 잘못된 이메일 형식과 필수값 누락 입력에서 Pydantic 검증 실패가 발생함. API의 HTTP 422 응답은 통합 테스트에서 확인 대상임 |
| UT-BB-SCHEMA-02 | 1차 | Pass | `durationHours` 1과 24는 통과하고 0과 25는 검증 실패함 |
| UT-BB-SCHEMA-03 | 1차 | Pass | 투표 선택값 A/B는 통과하고 C는 검증 실패함 |
| UT-BB-SCHEMA-04 | 1차 | Pass | 베팅 선택값 A/B와 0 이상 금액은 통과하고 잘못된 선택값과 음수 금액은 검증 실패함 |
| UT-BB-SCHEMA-05 | 1차 | Pass | 칭호 장착 요청에서 정수 titleId와 None은 통과하고 잘못된 타입은 검증 실패함 |
| UT-WB-AUTH-01 | 1차 | Pass | 같은 비밀번호는 검증 성공하고 다른 비밀번호는 검증 실패함 |
| UT-WB-AUTH-02 | 1차 | Pass | access token과 refresh token은 payload가 디코딩되고 잘못된 토큰은 None을 반환함 |
| UT-WB-AUTH-03 | 1차 | Pass | 사용자 생성 시 email, nickname, 기본 credit, password_hash가 기대값으로 설정됨 |
| UT-WB-AUTH-04 | 1차 | Pass | refresh token이 없으면 생성되고 기존 token 객체는 새 값으로 갱신됨 |
| UT-WB-AUTH-05 | 1차 | Pass | 저장된 refresh token이 있으면 삭제 후 대상 객체를 반환하고, 저장된 token이 없으면 None을 반환함 |
| UT-WB-AUTH-06 | 1차 | Pass | 사용자 credit 조회와 nickname 변경은 사용자 존재 여부에 따라 값 또는 None을 반환함 |
| UT-WB-AUTH-07 | 1차 | Pass | DB dependency 종료 시 session close가 호출됨 |
| UT-WB-AUTH-08 | 1차 | Pass | 정상 토큰은 User를 반환하고 userId 없음, 사용자 없음, 잘못된 토큰은 401 예외가 발생함 |
| UT-WB-AUTH-09 | 1차 | Pass | 회원가입, 로그인, 토큰 재발급, 로그아웃 endpoint가 결과 코드에 맞는 응답 또는 예외를 반환함 |
| UT-WB-AUTH-10 | 1차 | Pass | 내 정보, credit 조회, 닉네임 변경 endpoint가 성공/404/409 경로를 처리함 |
| UT-WB-AUTH-11 | 1차 | Pass | 이메일/닉네임 중복 확인과 Swagger 로그인 성공/실패 경로가 기대 상태로 처리됨 |
| UT-WB-POLL-01 | 1차 | Pass | ENDED/INVALID/만료된 ONGOING 투표는 종료로, 유효한 ONGOING 투표는 활성으로 판단됨 |
| UT-WB-POLL-02 | 1차 | Pass | 생성자, 투표자, 베팅자의 canVote, canBet, resultsVisible 상태가 규칙과 일치함 |
| UT-WB-POLL-03 | 1차 | Pass | 총 투표수 0은 0.0을 반환하고 양수 투표율은 소수 둘째 자리로 반올림됨 |
| UT-WB-POLL-04 | 1차 | Pass | A/B 선택지는 정렬된 옵션에 매핑되고 잘못된 선택값 또는 옵션 부족은 None을 반환함 |
| UT-WB-POLL-05 | 1차 | Pass | 승리, 무승부, 무효 결과 계산이 득표수와 옵션 개수에 맞게 반환됨 |
| UT-WB-POLL-06 | 1차 | Pass | 종료된 투표와 end_time 없음은 남은 시간이 0이고 미래 end_time은 남은 초를 반환함 |
| UT-WB-POLL-07 | 1차 | Pass | 참여자 수, 총 베팅 금액, 선택지별 베팅 금액 조회가 데이터 있음/없음 상태에 맞게 반환됨 |
| UT-WB-POLL-08 | 1차 | Pass | 옵션 상세 응답에 voteRatio와 betCredits가 기대값으로 조립됨 |
| UT-WB-POLL-09 | 1차 | Pass | 옵션이 정확히 2개일 때만 binary option으로 판단됨 |
| UT-WB-POLL-10 | 1차 | Pass | 종료된 ONGOING 투표는 ENDED로 표시되고 그 외 상태는 기존 status를 유지함 |
| UT-WB-POLL-11 | 1차 | Pass | 투표 생성 시 Poll, PollOption, PollStat 저장 흐름과 DB 예외 시 rollback이 확인됨 |
| UT-WB-POLL-12 | 1차 | Pass | 목록 조회의 상태, 정렬, page/limit 조건이 query 흐름에 반영됨 |
| UT-WB-POLL-13 | 1차 | Pass | mine 조건에서 사용자 참여 투표 조회와 본인 생성 투표 제외 조건이 적용됨 |
| UT-WB-POLL-14 | 1차 | Pass | 목록 조회 결과 없음은 빈 목록을 반환하고, 옵션 부족은 빈 option 문자열을 반환하며, 사용자 Vote/Bet은 action flag 조립에 전달됨 |
| UT-WB-POLL-15 | 1차 | Pass | 투표 생성/목록 endpoint가 성공 응답과 500 예외 경로를 처리함 |
| UT-WB-POLL-16 | 1차 | Pass | 투표 상세 endpoint가 Poll 없음, 옵션 개수 오류, 상세 응답 조립 경로를 처리함 |
| UT-WB-VOTE-01 | 1차 | Pass | 정상 투표 시 Vote 생성, option vote_count 증가, total_votes 증가, user credit 증가가 확인됨 |
| UT-WB-VOTE-02 | 1차 | Pass | 없는 투표, 종료 투표, 생성자 투표, 중복 투표, 잘못된 선택지 실패 코드가 반환됨 |
| UT-WB-VOTE-03 | 1차 | Pass | 사용자 투표 이력이 있으면 created_at 내림차순 query 결과를 반환하고, 이력이 없으면 빈 목록을 반환함 |
| UT-WB-VOTE-04 | 1차 | Excluded | User 또는 PollStat이 없어도 Vote가 생성되는 현재 구현 동작을 확인한 항목이나, `UT-WB-VOTE-10`, `UT-WB-VOTE-11`의 데이터 무결성 기대 결과와 모순되어 유효 결과 집계에서 제외함 |
| UT-WB-VOTE-05 | 1차 | Pass | 투표 endpoint가 성공 응답과 중복/없는 투표/종료/생성자 예외를 처리하고, 내 투표 이력은 목록 또는 빈 목록으로 응답함 |
| UT-WB-BET-01 | 1차 | Pass | 정상 베팅 시 Bet이 생성되고 credit 차감 후 참여 보상 지급 흐름이 확인됨 |
| UT-WB-BET-02 | 1차 | Pass | amount 0 베팅은 Bet이 생성되지만 credit 차감과 참여 보상이 발생하지 않음 |
| UT-WB-BET-03 | 1차 | Pass | 사용자 없음, 음수 금액, Poll 없음, 종료, 미투표, 투표 선택지와 베팅 선택지 불일치, 중복, 잔액 부족 실패 코드가 반환됨 |
| UT-WB-BET-04 | 1차 | Pass | 사용자 베팅 이력이 created_at 내림차순 query 결과로 반환됨 |
| UT-WB-BET-05 | 1차 | Pass | 옵션 개수 부족 또는 잘못된 optionId에서 유효하지 않은 선택지 실패 코드가 반환됨 |
| UT-WB-BET-06 | 1차 | Pass | 베팅 endpoint가 성공/포기 응답과 결과 코드별 HTTP 예외, 이력 응답을 처리함 |
| UT-WB-RESULT-01 | 1차 | Pass | 만료된 ONGOING 투표는 승자가 있으면 ENDED와 winningOptionId를 반환하고, 득표가 없으면 INVALID 상태로 처리됨 |
| UT-WB-RESULT-02 | 1차 | Pass | Poll 없음, 이미 판정됨, 아직 진행 중, 옵션 부족 실패 코드가 반환됨 |
| UT-WB-PAYOUT-01 | 1차 | Pass | 일반 승리는 1.5배 보상, 무승부는 원금 반환으로 계산됨 |
| UT-WB-PAYOUT-02 | 1차 | Pass | 종료된 투표 정산 시 승자 Bet과 사용자 credit, Settlement 상태가 변경됨 |
| UT-WB-PAYOUT-03 | 1차 | Pass | 무승부 및 반복문 경로에서 payoutUserCount와 보상 계산이 기대값과 일치함 |
| UT-WB-PAYOUT-04 | 1차 | Pass | 이미 정산됨, Poll 없음, 미종료, 옵션 부족 실패 코드가 반환됨 |
| UT-WB-PAYOUT-05 | 1차 | Pass | 정산 대상 User 조회 실패 시 Bet result/reward 계산은 유지되고 존재하는 사용자만 credit 갱신됨 |
| UT-WB-TITLE-01 | 1차 | Pass | 칭호 구매 성공 시 credit 감소와 UserTitle 생성이 확인되고 실패 코드가 반환됨 |
| UT-WB-TITLE-02 | 1차 | Pass | 칭호 장착 성공과 사용자 없음, 미보유, 이미 장착 실패 경로가 처리됨. 해제 경로는 UT-WB-TITLE-04에서 별도 확인함 |
| UT-WB-TITLE-03 | 1차 | Pass | 상점 목록, 보유 titleId, 인벤토리 조회 helper가 데이터 상태에 맞게 반환됨 |
| UT-WB-TITLE-04 | 1차 | Pass | 칭호 해제 성공 시 equipped_title_id가 None이 되고 사용자 없음은 실패 코드가 반환됨 |
| UT-WB-TITLE-05 | 1차 | Pass | 칭호 endpoint가 상점, 구매, 장착/해제, 인벤토리 응답과 실패 예외를 처리함 |
| UT-WB-WS-01 | 1차 | Pass | WebSocket 연결 시 accept와 active_connections 추가가 발생하고, 연결된 사용자와 존재하지 않는 사용자 disconnect가 안전하게 처리됨 |
| UT-WB-WS-02 | 1차 | Pass | 개인 메시지는 대상 연결에 전송되고 예외 발생 시 예외가 전파되며, broadcast는 전체 연결 순회와 전송 예외 처리 경로를 수행함 |
| UT-WB-WS-03 | 1차 | Pass | 정상 연결 후 receive loop에 진입하고, WebSocketDisconnect 및 일반 예외 발생 시 manager.disconnect가 호출됨 |
| UT-WB-ENV-01 | 1차 | Pass | 환경변수가 있으면 override 값을 사용하고, 환경변수가 없으면 Settings 기본값을 사용함 |
| UT-WB-ENV-02 | 1차 | Pass | DB connect 이벤트에서 `SET TIME ZONE 'Asia/Seoul'` 실행 후 cursor가 닫힘 |
| UT-WB-ENV-03 | 1차 | Pass | now_kst는 KST timezone을 포함하고 now_kst_naive는 timezone 없는 datetime을 반환함 |
| UT-WB-ENV-04 | 1차 | Pass | root 응답, scheduler start 조건, shutdown 호출 경로가 확인됨 |
| UT-WB-ENV-05 | 1차 | Pass | auth, poll, bets, titles 등 주요 router prefix와 `/api` 등록 상태가 확인됨 |
| UT-WB-SCHED-01 | 1차 | Pass | 만료 투표가 없으면 종료하고 있으면 판정/정산/알림 호출 흐름으로 진입함 |
| UT-WB-SCHED-02 | 1차 | Pass | winningOptionId 유무와 관계없이 종료 알림 broadcast가 호출됨 |
| UT-WB-SCHED-03 | 1차 | Pass | 승자 Bet 목록 개수만큼 개인 정산 완료 메시지가 전송됨 |
| UT-WB-SCHED-04 | 1차 | Pass | 판정 실패, 정산 실패, 일반 예외 발생 경로에서 후속 처리를 건너뛰거나 중단하고 모든 경우 DB session close가 호출됨 |
| IT-BB-AUTH-01 | 1차 | Pass | 회원가입 후 User가 생성되고 로그인 시 access/refresh token과 AuthToken이 저장되며, 재발급 성공 후 로그아웃 시 AuthToken이 삭제됨 |
| IT-BB-AUTH-02 | 1차 | Pass | 보호 API는 토큰 없음/잘못된 토큰에서 401을 반환하고, 유효 토큰에서는 내 정보/credit 조회와 nickname 변경이 DB 상태에 반영됨 |
| IT-BB-POLL-01 | 1차 | Pass | 투표 생성 API 호출 후 Poll, PollOption 2개, PollStat이 생성되고 목록/상세 조회 응답에 생성한 투표와 선택지가 반영됨 |
| IT-BB-POLL-02 | 1차 | Pass | 상태, 정렬, page/limit, mine 조건 조회가 200으로 응답하고, 참여한 투표의 hasVoted flag와 종료 투표 조회가 응답에 반영됨 |
| IT-BB-VOTE-01 | 1차 | Pass | 투표 참여 후 Vote가 생성되고 option vote_count, PollStat total_votes, 사용자 credit이 증가하며 상세 응답의 hasVoted/canVote/voteCount가 변경됨 |
| IT-BB-BET-01 | 1차 | Pass | 투표 후 베팅하면 Bet이 생성되고 amount 50 기준 credit이 순증 50으로 변경되며 베팅 이력에 pollId와 amount가 반환됨 |
| IT-BB-TITLE-01 | 1차 | Pass | 칭호 상점 조회, 구매, 장착, 인벤토리 조회가 연동되고 UserTitle 생성, credit 감소, equippedTitleId 변경이 확인됨 |
| IT-BB-WS-01 | 1차 | Pass | TestClient WebSocket으로 `/api/ws/{user_id}` 연결이 수락되고 메시지 송신 후 context 종료로 연결 해제 흐름이 수행됨 |
| ST-BB-ENV-01 | 1차 | Pass | Docker Compose로 API/DB 컨테이너가 실행되고 root API가 200 응답을 반환하며 public schema의 주요 테이블 10개가 생성됨 |
| ST-BB-ENV-02 | 1차 | Pass | seed.sql 적용 후 demo 계정 로그인이 성공하고 투표 목록과 칭호 상점 데이터가 조회됨 |
| ST-BB-E2E-01 | 1차 | Pass | 실제 API 서버에서 회원가입/로그인, 투표 생성, 투표 참여, 베팅, 칭호 구매/장착이 연속 성공하고 DB의 credit, equipped_title_id, Vote, Bet 상태가 일관됨 |
| ST-BB-E2E-02 | 1차 | Pass | 만료 처리한 투표가 스케줄러에 의해 ENDED/COMPLETED로 변경되고 WebSocket으로 POLL_END와 PAYOUT_COMPLETE 알림을 수신함 |
| UT-WB-VOTE-06 | 1차 | Pass | 정상 투표 시 Vote 객체가 생성되고 poll_id, user_id, option_id가 선택지와 일치함 |
| UT-WB-VOTE-07 | 1차 | Pass | 정상 투표 시 대상 PollOption의 vote_count가 1회 증가함 |
| UT-WB-VOTE-08 | 1차 | Pass | 정상 투표 시 PollStat total_votes가 1회 증가함 |
| UT-WB-VOTE-09 | 1차 | Pass | 정상 투표 시 사용자 credit이 100 증가함 |
| UT-WB-VOTE-10 | 1차 | Fail | 기대 결과는 User가 없으면 Vote 미생성이었으나 실제로 Vote가 생성되고 SUCCESS가 반환됨 |
| UT-WB-VOTE-11 | 1차 | Fail | 기대 결과는 PollStat이 없으면 집계 불일치 방지를 위해 실패였으나 실제로 Vote와 option vote_count가 갱신되고 SUCCESS가 반환됨 |
| UT-WB-VOTE-12 | 1차 | Pass | 이미 투표한 사용자는 ALREADY_VOTED가 반환되고 add/commit이 호출되지 않음 |
| UT-WB-VOTE-13 | 1차 | Pass | 생성자 투표는 CREATOR_CANNOT_VOTE가 반환되고 add/commit이 호출되지 않음 |
| UT-WB-VOTE-14 | 1차 | Pass | poll end_time이 현재 시각과 같으면 종료된 poll로 처리되어 POLL_CLOSED가 반환됨 |
| UT-WB-VOTE-15 | 1차 | Pass | commit 실패 시 rollback이 호출되고 SQLAlchemyError가 전파됨 |
| UT-WB-BET-07 | 1차 | Pass | amount 1 베팅은 1 credit 차감 후 참여 보상 100 credit이 지급되어 credit이 1099가 됨 |
| UT-WB-BET-08 | 1차 | Pass | amount 99 베팅은 99 credit 차감 후 참여 보상 100 credit이 지급되어 credit이 1001이 됨 |
| UT-WB-BET-09 | 1차 | Pass | amount 100 베팅은 차감 100과 참여 보상 100으로 credit 순변화가 없음 |
| UT-WB-BET-10 | 1차 | Pass | amount 101 베팅은 credit이 1 감소함 |
| UT-WB-BET-11 | 1차 | Pass | amount 0 베팅은 Bet을 생성하고 credit은 변경하지 않음 |
| UT-WB-BET-12 | 1차 | Pass | amount 0 Bet이 이미 있으면 유료 베팅은 ALREADY_BET로 거부되고 credit 변경이 없음 |
| UT-WB-BET-13 | 1차 | Pass | 투표 선택지와 다른 선택지 베팅은 VOTE_OPTION_MISMATCH로 거부되고 credit/Bet 변경이 없음 |
| UT-WB-BET-14 | 1차 | Pass | 잔액보다 1 큰 금액 베팅은 INSUFFICIENT_CREDIT으로 거부되고 credit/Bet 변경이 없음 |
| UT-WB-BET-15 | 1차 | Pass | 잔액과 같은 금액 베팅은 성공하고 참여 보상 100 credit이 남음 |
| UT-WB-BET-16 | 1차 | Pass | commit 실패 시 rollback이 호출되고 SQLAlchemyError가 전파됨 |
| UT-WB-TITLE-06 | 1차 | Pass | title 가격과 credit이 같으면 구매 성공 후 credit이 0이 되고 UserTitle이 생성됨 |
| UT-WB-TITLE-07 | 1차 | Pass | title 가격보다 credit이 1 부족하면 INSUFFICIENT_CREDIT으로 거부되고 상태 변경이 없음 |
| UT-WB-TITLE-08 | 1차 | Pass | 이미 보유한 title 구매는 ALREADY_OWNED로 거부되고 credit 변경이 없음 |
| UT-WB-TITLE-09 | 1차 | Pass | price 0 title 구매는 성공하고 credit 변화가 없음 |
| UT-WB-TITLE-10 | 1차 | Fail | 기대 결과는 음수 price title 구매 거부였으나 실제로 구매 성공 처리되고 사용자 credit이 100 증가함 |
| UT-WB-TITLE-11 | 1차 | Pass | commit 실패 시 rollback이 호출되고 SQLAlchemyError가 전파됨 |
| UT-WB-TITLE-12 | 1차 | Pass | 보유하지 않은 title 장착은 TITLE_NOT_OWNED로 거부되고 equipped_title_id 변경이 없음 |
| UT-WB-TITLE-13 | 1차 | Pass | 이미 장착한 title 재장착은 ALREADY_EQUIPPED로 거부되고 상태가 유지됨 |
| UT-WB-TITLE-14 | 1차 | Pass | 장착 칭호가 없는 상태의 해제 요청은 성공하고 equipped_title_id는 None으로 유지됨 |
