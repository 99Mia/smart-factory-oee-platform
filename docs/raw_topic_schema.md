# PLC Raw Topic Schema — PLC → Edge → Kafka (JSON 기준)

> 이 문서는 Edge에서 PLC Tag를 읽어 Kafka Raw Topic으로 보내는 JSON 데이터 구조를 정의합니다.  
> 한 이벤트에는 한 시점 장비 상태 전체가 포함되며, 확장 가능한 구조로 설계되어 있습니다.

---

## 1. Topic 정보

- **Topic 이름:** `plc_raw_topic`  
- **Description:** Edge에서 수집한 PLC Tag 이벤트를 시계열로 전송  
- **Partition Key:** `equipmentId` (같은 장비 이벤트 순서 보장)  
- **Retention:** 프로젝트 요구에 따라 설정 (예: 7일, 30일)  
- **Serialization Format:** Avro
- **Schema Management:** Schema Registry 기반 버전 관리

---

## 2. Schema

| Field        | Type      | Description |
|-------------|-----------|-------------|
| timestamp   | ISO8601 문자열 / DATETIME | Edge가 PLC Tag를 읽은 시각 |
| equipmentId | STRING    | PLC 장비 식별자 (예: CNC_01, Conveyor_01, Line_01) |
| tags        | OBJECT    | 한 시점 장비 상태 전체를 담은 객체 (Tag Name: Value) |

- **tags 객체 예시 (CNC_01)**:
```json
{
  "OperationState": 1,
  "Mode": 1,
  "PowerState": 1,
  "ErrorCode": 0,
  "AlarmCode": 0,
  "Estop": 0
}