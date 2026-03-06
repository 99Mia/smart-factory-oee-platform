import json
import pandas as pd
from datetime import datetime
import os
import re

# ============================================
# 1. JSONL 읽기
# ============================================

current_dir = os.path.dirname(__file__)
file_path = os.path.join(
    current_dir,
    "../../../edge/processed_topic_samples/plc_processed_cnc_toolchange_s01.jsonl"
)

data = []
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

matches = re.findall(r'\{.*?\}(?=\s*\{|\s*$)', content, flags=re.DOTALL)

for match in matches:
    obj = json.loads(match)
    obj["timestamp"] = datetime.fromisoformat(
        obj["timestamp"].replace("Z", "+00:00")
    )
    data.append(obj)

df = pd.DataFrame(data)
df.sort_values("timestamp", inplace=True)
df.reset_index(drop=True, inplace=True)


# ============================================
# 2. 라인 전체 알람 타임라인 생성
# ============================================

df_alarms = df[df["eventType"].isin(["ALARM_ON", "ALARM_OFF"])][
    ["timestamp", "equipmentId", "alarmCode", "eventType"]
].copy()

df_alarms.sort_values("timestamp", inplace=True)

active_alarms = []
alarm_timeline = []

for _, row in df_alarms.iterrows():

    if row["eventType"] == "ALARM_ON":
        active_alarms.append({
            "equipmentId": row["equipmentId"],
            "alarmCode": row["alarmCode"]
        })

    elif row["eventType"] == "ALARM_OFF":
        active_alarms = [
            a for a in active_alarms
            if not (
                a["equipmentId"] == row["equipmentId"]
                and a["alarmCode"] == row["alarmCode"]
            )
        ]

    alarm_timeline.append({
        "timestamp": row["timestamp"],
        "activeAlarms": active_alarms.copy()
    })

df_alarm_timeline = pd.DataFrame(alarm_timeline)


# ============================================
# 3. 특정 시점의 활성 알람 조회 함수
# ============================================

def get_active_alarms(ts):

    rows = df_alarm_timeline[
        df_alarm_timeline["timestamp"] <= ts
    ]

    if rows.empty:
        return []

    return rows.iloc[-1]["activeAlarms"]


# ============================================
# 4. CNC 이벤트만 추출
# ============================================

df_cnc = df[df["equipmentId"] == "CNC_01"].copy()
df_cnc.sort_values("timestamp", inplace=True)
df_cnc.reset_index(drop=True, inplace=True)


# ============================================
# 5. 상태 / 모드 누적 갱신 (이벤트 기반)
# ============================================

current_state = None
current_mode = None

filled_states = []
filled_modes = []

for _, row in df_cnc.iterrows():

    if row["eventType"] == "STATE_TRANSITION":
        current_state = row["currentState"]

    if row["eventType"] == "MODE_TRANSITION":
        current_mode = row["currentMode"]

    filled_states.append(current_state)
    filled_modes.append(current_mode)

df_cnc["state_filled"] = filled_states
df_cnc["mode_filled"] = filled_modes


# ============================================
# 6. 다음 이벤트까지 시간 계산
# ============================================

df_cnc["next_timestamp"] = df_cnc["timestamp"].shift(-1)
df_cnc["durationSec"] = (
    df_cnc["next_timestamp"] - df_cnc["timestamp"]
).dt.total_seconds()


# ============================================
# 7. 다운타임 / 생산시간 계산
# ============================================

downtime_records = []
production_time = 0
downtime_time = 0

for _, row in df_cnc.iterrows():

    if pd.isna(row["durationSec"]):
        continue

    state = row["state_filled"]
    mode = row["mode_filled"]
    duration = row["durationSec"]

    active_alarm_list = get_active_alarms(row["timestamp"])
    active_alarm_codes = [
        a["alarmCode"] for a in active_alarm_list
    ]

    # 생산 조건 (AUTO + RUN/COMPLETE)
    is_production = (
        state in ["RUN", "COMPLETE"]
        and mode == "AUTO"
    )

    if is_production:
        production_time += duration
    else:
        downtime_time += duration

        downtime_records.append({
            "start": row["timestamp"],
            "end": row["next_timestamp"],
            "durationSec": duration,
            "state": state,
            "mode": mode,
            "alarmCodes": active_alarm_codes
        })


# ============================================
# 8. 결과 정리
# ============================================

df_downtime = pd.DataFrame(downtime_records)

planned_production_time = production_time + downtime_time

availability = (
    production_time / planned_production_time
    if planned_production_time > 0 else 0
)

print("\n===== CNC Downtime Detail =====")
print(df_downtime)

print("\n===== CNC OEE Availability =====")
print(f"Production Time         : {production_time:.1f} sec")
print(f"Downtime                : {downtime_time:.1f} sec")
print(f"Planned Production Time : {planned_production_time:.1f} sec")
print(f"Availability            : {availability:.4f}")