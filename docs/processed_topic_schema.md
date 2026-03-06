# Processed Topic Schema — Edge → Kafka (JSON 기준)

> 이 문서는 Edge에서 PLC Raw 데이터를 가공하여 Kafka Processed Topic으로 보내는 JSON 데이터 구조를 정의합니다.  
> 한 이벤트는 상태 전이, 알람, 생산 완료 등 의미 기반 이벤트 단위로 구성되며, OEE 계산 및 AI Feature 생성을 고려하여 설계되었습니다.

---

## 1. Topic 정보

- **Topic 이름:** `processed_topic`
- **Description:** Edge에서 Raw 데이터를 가공하여 상태 변화 및 생산 이벤트 단위로 전송
- **Partition Key:** `equipmentId` (같은 장비 이벤트 순서 보장)
- **Retention:** 프로젝트 요구에 따라 설정 (예: 30일, 90일)
- **Serialization Format:** Avro
- **Schema Management:** Schema Registry 기반 버전 관리


---

## 2. Schema

| Field | Type | Description |
|-------|------|-------------|
| timestamp | ISO8601 문자열 / DATETIME | 이벤트 발생 시각 |
| edgeId | STRING | Edge 식별자 |
| equipmentId | STRING | 설비 식별자 (예: CNC_01, Conveyor_01, Line_01) |
| jobId | STRING | 작업 지시 ID |
| productId | STRING | 제품 ID |
| lotId | STRING | LOT ID |
| eventType | STRING | 이벤트 유형 |
| previousState | STRING | 이전 상태 |
| currentState | STRING | 현재 상태 |
| previousMode | STRING | 이전 모드 |
| currentMode | STRING | 현재 모드 |
| durationSec | INT | 이전 상태 유지 시간 (초) |
| alarmCode | INT | 알람 코드 |
| deltaTotal | INT | 총 생산 수량 증가 |
| deltaGood | INT | 양품 수량 증가 |
| deltaReject | INT | 불량 수량 증가 |

> 이벤트 유형에 따라 일부 필드는 NULL 값을 가질 수 있음.
> durationSec는 상태 전이 발생 시 이전 상태가 유지된 시간을 Edge에서 계산하여 포함한다.

---

## 3. eventType 정의

- `STATE_TRANSITION`
- `MODE_TRANSITION`
- `ALARM_ON`
- `ALARM_OFF`
- `PRODUCTION_COMPLETE`

---

## 4. 상태(State) 값 정의

> 상태 값 정의는 "PLC Tag Definition — OEE Monitoring" 문서를 따른다.

---

## 5. 모드(Mode) 값 정의

> 모드 값 정의는 "PLC Tag Definition — OEE Monitoring" 문서를 따른다.

---

## 6. 이벤트 예시 (STATE_TRANSITION)

```json
{
  "timestamp": "2026-03-03T08:00:00Z",
  "edgeId": "EDGE_01",
  "equipmentId": "CNC_01",
  "jobId": "JOB_001",
  "productId": "BRAKEROTOR_A",
  "lotId": "LOT_01",
  "eventType": "STATE_TRANSITION",
  "previousState": "IDLE",
  "currentState": "RUN",
  "previousMode": null,
  "currentMode": null,
  "durationSec": 120,
  "alarmCode": null,
  "deltaTotal": null,
  "deltaGood": null,
  "deltaReject": null
}
```
