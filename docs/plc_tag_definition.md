# PLC Tag Definition — OEE Monitoring

## 📑 목차
- [1. 장비 상태 (Equipment Status)](#1-장비-상태-equipment-status)
- [2. 생산 성과 (Production Performance)](#2-생산-성과-production-performance)
- [3. 고장 정보 (Fault Information)](#3-고장-정보-fault-information)
- [4. 물류 / 흐름 문제 (Material Flow Issues)](#4-물류--흐름-문제-material-flow-issues)
- [5. 안전 (Safety)](#5-안전-safety)

---

## 1. 장비 상태 (Equipment Status)

### CNC_01.OperationState / Conveyor_01.OperationState
설명: 설비의 실제 동작 상태  
데이터 타입: INT

| 값 | 상태 | 설명 |
|-----|--------|---------------------------|
| 0 | UNKNOWN | 상태 미확인 (통신 이상 가능) |
| 1 | RUN | 정상 가동 중 |
| 2 | IDLE | 대기 중 |
| 3 | HOLD | 일시 정지 |
| 4 | COMPLETE | 사이클 종료 |
| 5 | FAULT | 고장 정지 |

---

### CNC_01.Mode / Conveyor_01.Mode
설명: 설비 운전 모드  
데이터 타입: INT

| 값 | 상태 | 설명 |
|-----|--------|---------------------------|
| 0 | UNKNOWN | 모드 미확인 |
| 1 | AUTO | 자동 운전 |
| 2 | MANUAL | 수동 운전 |
| 3 | SETUP | 셋업 모드 |
| 4 | MAINTENANCE | 작업 모드 |

---

### CNC_01.PowerState / Conveyor_01.PowerState
설명: 설비 전원 상태  
데이터 타입: INT

| 값 | 상태 | 설명 |
|-----|--------|---------------------------|
| 0 | OFF | 전원 꺼짐 |
| 1 | ON | 전원 켜짐 |

---

## 2. 생산 성과 (Production Performance)

### Line_01.TotalCount
설명: 총 생산 수량 (누적)  
데이터 타입: DINT  

---

### Line_01.GoodCount
설명: 양품 수량  
데이터 타입: DINT  

---

### Line_01.RejectCount
설명: 불량 수량  
데이터 타입: DINT  

---

## 3. 고장 정보 (Fault Information)

### CNC_01.ErrorCode
설명: CNC 설비 오류 코드 (Vendor-specific)  
데이터 타입: INT

> ⚠️ ErrorCode는 장비 제조사별 Vendor-specific 코드이며, 본 문서의 값은 공통 예시입니다.

| 코드 | 의미 |
|-------|---------------------------|
| 0 | No Error |
| 100 | Servo Fault |
| 101 | Overload |
| 102 | Overheat |
| 103 | Spindle Fault |
| 104 | Axis Error |
| 999 | Unknown Error |

---

### Conveyor_01.ErrorCode
설명: 컨베이어 오류 코드  
데이터 타입: INT

> ⚠️ ErrorCode는 장비 제조사별 Vendor-specific 코드이며, 본 문서의 값은 공통 예시입니다.

| 코드 | 의미 |
|-------|---------------------------|
| 0 | No Error |
| 200 | Motor Fault |
| 201 | Overcurrent |
| 202 | Sensor Failure |
| 203 | Drive Fault |
| 999 | Unknown Error |

---

### CNC_01.AlarmCode
설명: CNC 경고/알람 코드  
데이터 타입: INT

> ⚠️ AlarmCode는 장비 제조사별 Vendor-specific 코드이며, 본 문서의 값은 공통 예시입니다.

| 코드 | 의미 |
|-------|---------------------------|
| 0 | No Alarm |
| 10 | Maintenance Required |
| 11 | Tool Change Required |
| 12 | Coolant Low |
| 13 | Door Open |
| 99 | Other Alarm |

---

### Conveyor_01.AlarmCode
설명: 컨베이어 경고 코드  
데이터 타입: INT

> ⚠️ AlarmCode는 장비 제조사별 Vendor-specific 코드이며, 본 문서의 값은 공통 예시입니다.

| 코드 | 의미 |
|-------|---------------------------|
| 0 | No Alarm |
| 20 | Minor Delay / Micro Stop |
| 21 | Jam Warning |
| 22 | Jam Stop |
| 99 | Other Alarm |

---

## 4. 물류 / 흐름 문제 (Material Flow Issues)

### Conveyor_01.JamDetected
설명: 컨베이어 막힘 감지  
데이터 타입: INT

| 값 | 상태 | 설명 |
|-----|--------|---------------------------|
| 0 | Normal | 막힘 없음 |
| 1 | Jam | 물류 막힘 발생 |

---

## 5. 안전 (Safety)

### CNC_01.Estop / Conveyor_01.Estop
설명: 비상 정지 상태  
데이터 타입: INT

| 값 | 상태 | 설명 |
|-----|--------|---------------------------|
| 0 | Normal | 비상정지 해제 |
| 1 | ESTOP | 비상정지 작동 |

---

## 6. 확장 가능성 (Extensibility)

> ⚡ **확장 가능성:**  
> 현재 PLC Tag 구조는 `장비명_데이터유형` 규칙으로 통일되어 있어,  
> 향후 센서 데이터(예: 온도, 진동, 전류) 추가 및 Predictive Maintenance 기반 이상징후 예측 AI로 확장 가능합니다.  
> 기존 Edge Event, Kafka Topic, MES/AI Feature 파이프라인 구조는 그대로 활용 가능하며,  
> 새로운 Tag 추가 시 기존 로직 변경 최소화가 가능합니다.