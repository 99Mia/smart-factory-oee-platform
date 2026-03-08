# Manufacturing Feature Generation Logic

이 문서는 `manufacturing.feature.topic`에 Feature 데이터를 생성하는 **로직**과 **계산 방법**을 상세히 기술합니다.

---

## 1. 개요

* 입력: 생산 이벤트 로그 (`PRODUCTION_COMPLETE`, `STATE_TRANSITION`, `ALARM_ON`, `MODE_TRANSITION`)
* 출력: Feature Record (Kafka Topic `manufacturing.feature.topic`)
* Window: 최근 5개 제품 기준 Count Window
* Trigger: `PRODUCTION_COMPLETE` 이벤트 발생 시 Feature 계산

---

## 2. 이벤트 처리 순서

1. `PRODUCTION_COMPLETE` 이벤트 수신
2. 해당 제품을 Window에 추가
3. Window가 5개 제품 이상이면, 통계 Feature 계산
4. Feature Record 생성 후 Kafka Topic에 Publish

---

## 3. Window 관리

* Type: Count Window
* Size: 5 Products
* Scope: equipmentId = Line_01
* Sliding 방식: 한 제품씩 이동하며 Window 갱신

**Pseudo Code:**

```python
window = deque(maxlen=5)  # 최근 5개 제품

def on_production_complete(event):
    window.append(event)
    if len(window) >= 1:
        feature_record = calculate_features(window)
        publish_to_kafka(feature_record)
```

---

## 4. Feature 계산 로직

### 4.1 생산 속도 Feature

* **Input:** `PRODUCTION_COMPLETE` 이벤트 timestamp
* **Calculation:**

```python
intervals = [window[i].timestamp - window[i-1].timestamp for i in range(1, len(window))]
production_interval_avg = mean(intervals)
production_interval_std = std(intervals)
```

### 4.2 설비 사이클 Feature

* **Input:** `STATE_TRANSITION (RUN → COMPLETE)` 이벤트
* **Calculation:**

```python
cycle_times = [event.cycle_time for event in window]
cycle_time_avg = mean(cycle_times)
cycle_time_std = std(cycle_times)
```

### 4.3 알람 Feature

* **Input:** `ALARM_ON` 이벤트
* **Calculation:**

```python
alarm_count = sum(len(event.alarms) for event in window)
alarm_rate = alarm_count / len(window)
```

### 4.4 설비 상태 Feature

* **Input:** `STATE_TRANSITION` 이벤트
* **Calculation:**

```python
hold_count = sum(1 for event in window if event.state == 'HOLD')
idle_count = sum(1 for event in window if event.state == 'IDLE')
```

### 4.5 작업자 개입 Feature

* **Input:** `MODE_TRANSITION` 이벤트
* **Calculation:**

```python
manual_mode_count = sum(1 for event in window if event.mode_change == 'AUTO->MANUAL')
```

### 4.6 품질 Feature

* **Input:** `PRODUCTION_COMPLETE` 이벤트
* **Calculation:**

```python
good_count = sum(1 for event in window if event.quality == 'GOOD')
reject_count = sum(1 for event in window if event.quality == 'REJECT')
reject_rate = reject_count / len(window)

# 연속 불량 계산
reject_streak = 0
current_streak = 0
for event in window:
    if event.quality == 'REJECT':
        current_streak += 1
        reject_streak = max(reject_streak, current_streak)
    else:
        current_streak = 0
```

---

## 5. Kafka Publish Logic

```python
def publish_to_kafka(feature_record):
    producer.send('manufacturing.feature.topic', value=feature_record)
```

---

## 6. 참고

* 모든 Feature는 **최근 5개 제품 Window 기준**으로 계산
* Trigger Event가 발생할 때마다 Feature 업데이트
* AI 이상 탐지 모델 입력용 데이터로 사용
