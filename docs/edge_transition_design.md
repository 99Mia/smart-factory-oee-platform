# Edge Transition Design

## 1. 목적
Edge는 PLC Raw Tag를 상태 전이 기반 이벤트로 변환하여 Kafka로 전송한다.

---

## 2. State Store
equipmentId별로 In-Memory State를 유지한다.

저장 항목:
- lastState
- lastMode
- lastAlarmCode
- lastTotalCount
- lastGoodCount
- lastRejectCount
- lastStateChangeTimestamp
- currentJobId (MES 수신)
- currentProductId (MES 수신)
- currentLotId (MES 수신)
- currentRecipeId (MES 수신)

### 2.1 MES 작업지시 동기화
Edge는 MES로부터 jobId, productId, lotId를 수신한다.

설비가 SETUP 또는 IDLE 상태일 때,
해당 작업지시 정보는 In-Memory State Store에 반영되며,
이후 발생하는 이벤트에 포함된다.

설비 제어 정책에 따라,
Edge는 해당 작업 정보를 PLC에 Write 하거나,
설비가 Edge로부터 작업 정보를 조회(Pull)할 수 있다.

---

## 3. 이벤트 생성 규칙

### STATE_TRANSITION
currentState != lastState 일 경우
→ 상태 전이 이벤트를 생성한다.
→ 이전 상태 유지 시간(durationSec)을 계산하여 포함한다.

### MODE_TRANSITION
currentMode != lastMode 일 경우
→ 모드 전이 이벤트를 생성한다.

### ALARM_ON / OFF
AlarmCode 변화 감지 시
→ 알람 이벤트를 생성한다.

### PRODUCTION_COMPLETE
TotalCount가 이전 값보다 증가할 경우
→ 증가분(deltaTotal, deltaGood, deltaReject)을 계산하여
→ 생산 완료 이벤트를 생성한다.

## 4. 설계 의도
Raw 데이터를 직접 전송하지 않고,  
의미 기반 이벤트 구조를 채택하여 Kafka 트래픽을 최소화하고  
OEE 계산 및 데이터 분석에 적합한 구조를 제공한다.