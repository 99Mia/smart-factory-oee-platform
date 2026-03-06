import json
import pandas as pd
from datetime import datetime
import os
import re

# 1. JSONL 파일 읽기
current_dir = os.path.dirname(__file__)
file_path = os.path.join(
    current_dir,
    "../../../edge/processed_topic_samples/plc_processed_line_jam_s03.jsonl"
)

data = []
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 2. 각 JSON 객체 추출 (멀티라인 지원)
matches = re.findall(r'\{.*?\}(?=\s*\{|\s*$)', content, flags=re.DOTALL)
for match in matches:
    obj = json.loads(match)
    obj["timestamp"] = datetime.fromisoformat(obj["timestamp"].replace("Z", "+00:00"))
    data.append(obj)

# 3. DataFrame 변환
df = pd.DataFrame(data)

# 4. CNC 이벤트와 Line 이벤트 분리
df_cnc = df[df["equipmentId"] == "CNC_01"].copy()
df_line = df[df["equipmentId"] == "Line_01"].copy()

df_cnc.sort_values("timestamp", inplace=True)
df_cnc.reset_index(drop=True, inplace=True)

# 5. CNC 상태 추적 (MODE / ALARM)
alarm_active = False
current_mode = 'AUTO'
cnc_states = []

for idx, row in df_cnc.iterrows():
    # MODE_TRANSITION 반영
    if row['eventType'] == 'MODE_TRANSITION' and row['currentMode'] in ['MANUAL','AUTO']:
        current_mode = row['currentMode']
    # ALARM_ON / ALARM_OFF
    if row['eventType'] == 'ALARM_ON':
        alarm_active = True
    if row['eventType'] == 'ALARM_OFF':
        alarm_active = False
    cnc_states.append({
        'timestamp': row['timestamp'],
        'current_mode': current_mode,
        'alarm_active': alarm_active
    })

df_cnc_state = pd.DataFrame(cnc_states)

# 6. Line 이벤트별 status 판단
statuses = []
for idx, line_row in df_line.iterrows():
    cnc_before = df_cnc_state[df_cnc_state['timestamp'] <= line_row['timestamp']]
    if not cnc_before.empty:
        last_state = cnc_before.iloc[-1]
        if last_state['alarm_active'] or last_state['current_mode'] == 'MANUAL':
            statuses.append('isolated')
        else:
            statuses.append('valid')
    else:
        statuses.append('valid')  # CNC 이벤트 없으면 기본 valid

df_line['status'] = statuses

# 7. NaN 처리
df_line['deltaTotal'] = df_line['deltaTotal'].fillna(0)
df_line['deltaGood'] = df_line['deltaGood'].fillna(0)
df_line['deltaReject'] = df_line['deltaReject'].fillna(0)

# 8. valid / isolated 누적 계산
valid_events = df_line[df_line['status'] == 'valid'].copy()
isolated_events = df_line[df_line['status'] == 'isolated'].copy()

valid_events['cum_total'] = valid_events['deltaTotal'].cumsum()
valid_events['cum_good'] = valid_events['deltaGood'].cumsum()
valid_events['cum_reject'] = valid_events['deltaReject'].cumsum()

isolated_events['cum_total'] = isolated_events['deltaTotal'].cumsum()
isolated_events['cum_good'] = isolated_events['deltaGood'].cumsum()
isolated_events['cum_reject'] = isolated_events['deltaReject'].cumsum()

# 9. 최종 결과 출력
print("=== Valid Production ===")
if not valid_events.empty:
    print(valid_events[['cum_total','cum_good','cum_reject']].iloc[-1])
else:
    print("No valid production events.")

print("\n=== Isolated Production ===")
if not isolated_events.empty:
    print(isolated_events[['cum_total','cum_good','cum_reject']].iloc[-1])
else:
    print("No isolated production events.")