# manufacturing Feature Topic Schema

본 토픽은 제조 설비에서 발생하는 이벤트 로그(processed topic)를 기반으로  
AI 이상 탐지를 위한 **Feature 데이터를 생성하여 저장하는 Kafka Topic**이다.

Feature는 생산 이벤트(`PRODUCTION_COMPLETE`)를 기준으로  
**최근 5개 생산 제품을 기준으로 한 Count Window 방식**으로 생성된다.

각 Feature Record는 최근 5개 생산 과정에서 발생한 설비 상태, 알람, 생산 속도 등의
통계적 특징을 포함한다.

이 데이터는 이후 **AI 기반 이상 탐지 모델의 입력 데이터로 사용된다.**

---

# Topic 이름

- manufacturing.feature.topic

---

# Window 정의

| 항목 | 내용 |
|---|---|
Window Type | Count Window |
Window Size | 5 Products |
Trigger Event | PRODUCTION_COMPLETE |
Aggregation Scope | equipmentId = Line_01 |

설명

- 생산 완료 이벤트(`PRODUCTION_COMPLETE`)가 발생할 때마다 Window가 갱신된다.
- 최근 **5개 제품 생산 이벤트**를 기준으로 Feature를 계산한다.
- Sliding Window 방식으로, 한 제품씩 이동하며 Feature를 업데이트한다.

---

# Feature Schema

## 1. 메타데이터

| 필드 | 타입 | 설명 |
|---|---|---|
timestamp | string | Feature 생성 시간 |
edgeId | string | Edge 장비 ID |
lineId | string | 생산 라인 ID |
jobId | string | 생산 작업 ID |
productId | string | 제품 ID |
lotId | string | 생산 Lot ID |
windowProductCount | int | Window에 포함된 제품 수 |

---

## 2. 생산 속도 Feature

| Feature | 타입 | 설명 |
|---|---|---|
production_interval_avg | float | 제품 간 평균 생산 간격 |
production_interval_std | float | 생산 간격 표준편차 |

설명

- `PRODUCTION_COMPLETE` 이벤트의 timestamp를 기준으로 계산

---

## 3. 설비 사이클 Feature

| Feature | 타입 | 설명 |
|---|---|---|
cycle_time_avg | float | 평균 설비 사이클 시간 |
cycle_time_std | float | 사이클 시간 변동성 |

설명

- `STATE_TRANSITION (RUN → COMPLETE)` 이벤트를 기반으로 계산

---

## 4. 알람 Feature

| Feature | 타입 | 설명 |
|---|---|---|
alarm_count | int | Window 내 발생한 알람 수 |
alarm_rate | float | 제품당 알람 발생 비율 |

설명

- `ALARM_ON` 이벤트 기반

---

## 5. 설비 상태 Feature

| Feature | 타입 | 설명 |
|---|---|---|
hold_count | int | HOLD 상태 발생 횟수 |
idle_count | int | IDLE 상태 발생 횟수 |

설명

- `STATE_TRANSITION` 이벤트 기반

---

## 6. 작업자 개입 Feature

| Feature | 타입 | 설명 |
|---|---|---|
manual_mode_count | int | AUTO → MANUAL 전환 횟수 |

설명

- `MODE_TRANSITION` 이벤트 기반

---

## 7. 품질 Feature

| Feature | 타입 | 설명 |
|---|---|---|
good_count | int | Window 내 정상 생산 수 |
reject_count | int | Window 내 불량 생산 수 |
reject_rate | float | 불량률 |
reject_streak | int | 연속 불량 발생 개수 |

설명

- `PRODUCTION_COMPLETE` 이벤트 기반

---

# Feature Record 예시

```json
{
  "timestamp": "2026-03-03T08:10:00Z",
  "edgeId": "EDGE_01",
  "lineId": "Line_01",
  "jobId": "JOB_001",
  "productId": "BRAKEROTER_A",
  "lotId": "LOT_01",
  "windowProductCount": 5,

  "production_interval_avg": 140,
  "production_interval_std": 15,

  "cycle_time_avg": 150,
  "cycle_time_std": 8,

  "alarm_count": 1,
  "alarm_rate": 0.2,

  "hold_count": 1,
  "idle_count": 2,

  "manual_mode_count": 1,

  "good_count" : 4,
  "reject_count" : 1,
  "reject_count" : 0.2,
  "reject_streak" : 1
}