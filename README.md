# Smart Factory OEE & Event-Driven Anomaly Detection

Detect anomalies before production loss.

---

## Problem

Production loss is not caused by anomalies themselves,  
but by **late detection**.

- Raw PLC data does not show system behavior directly  
- Early signals exist but are hidden in event data  

---

## What This Project Does

Builds an **event-driven manufacturing pipeline** that:

- transforms raw PLC signals into structured production events  
- reconstructs production flow from event sequences  
- derives OEE from actual system behavior  
- generates feature-level signals from production dynamics  
- detects anomalies before they impact production outcomes   

---

## System Flow

```
PLC → Edge → Kafka → MES → Feature → Detection → Visualization
```
![architecture](docs/architecture.png)

This pipeline transforms raw PLC signals into structured production behavior and detection signals.

---

## Challenge

### PLC Data Limitation

PLC systems provide discrete event signals, not continuous system behavior.

- Only state change events are recorded
- System state exists only implicitly between events
- Production flow cannot be directly observed from raw data

→ System behavior must be reconstructed from event sequences

---

### Detection Limitation

Detecting anomalies in manufacturing is not just about identifying abnormal conditions.

The real challenge is:

> Detecting them early enough to prevent production impact

- Rule-based detection identifies clear failures, but only after the system has degraded
- Statistical detection captures subtle changes, but is often unstable in noisy event data
- Neither approach alone can reliably detect early-stage anomalies

→ Effective detection requires capturing both early signals and reliable conditions

---

## Solution

### 1. Behavior Reconstruction
Transform event logs into production flow

- Connect state transitions over time  
- Derive production intervals and durations  
- Reconstruct continuous system behavior  

---

### 2. Feature Transformation
Convert events into measurable signals:

- production interval (speed change)  
- reject rate / streak (quality degradation)  
- alarm frequency (system instability)  
- hold / idle ratios (flow disruption)  

---

### 3. Hybrid Detection
Detection combines domain rules and statistical signals.

```python
rule_alert = (
    (reject_streak >= 2) or
    (cycle_time_avg > baseline * 1.1) or
    (hold_rate > threshold)
)

stat_alert = abs(z_score) > 2

combined_alert = rule_alert or stat_alert
```

- Rule-based → captures confirmed failure patterns  
- Statistical → captures early deviations  
- Combined → enables early and reliable detection  


---

## Scenarios (Interactive)

Timely Response
https://99Mia.github.io/smart-factory-oee-platform/docs/toolchange_s01_timeline.html  

Delayed Response  
https://99Mia.github.io/smart-factory-oee-platform/docs/tooldelay_s02_timeline.html  

Line Jam  
https://99Mia.github.io/smart-factory-oee-platform/docs/cnc_line_jam_timeline_03.html  
https://99Mia.github.io/smart-factory-oee-platform/docs/conveyor_line_jam_03_timeline.html  

---

## Key Insight

> Production loss is determined by **timing, not anomalies**

---

## Tech Stack

Kafka · Python · Pandas · Plotly · PLC / MES  

---

## Docs

https://github.com/99Mia/smart-factory-oee-platform/tree/master/docs
