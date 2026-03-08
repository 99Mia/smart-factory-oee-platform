📦docs
 ┣ 📜architecture.png
 ┣ 📜edge_transition_design.md
 ┣ 📜feature_generation_logic.md
 ┣ 📜feature_topic_schema.md
 ┣ 📜plc_tag_definition.md
 ┣ 📜processed_topic_schema.md
 ┗ 📜raw_topic_schema.md
📦edge
 ┣ 📂avro_schemas
 ┃ ┣ 📜plc_processed_topic.avsc
 ┃ ┗ 📜plc_raw_topic.avsc
 ┣ 📂processed_topic_samples
 ┃ ┣ 📜plc_processed_cnc_toolchange_s01.json
 ┃ ┣ 📜plc_processed_cnc_tooldelay_s02.json
 ┃ ┗ 📜plc_processed_line_jam_s03.json
 ┗ 📂raw_topic_samples
 ┃ ┣ 📜plc_raw_cnc_toolchange_s01.jsonl
 ┃ ┣ 📜plc_raw_cnc_tooldelay_s02.jsonl
 ┃ ┗ 📜plc_raw_line_jam_s03.jsonl
📦kafka_streams
 ┣ 📂avro_schemas
 ┃ ┗ 📜plc_feature_topic.avsc
 ┗ 📂feature_topic_samples
 ┃ ┣ 📜feature_line_jam_s03.csv
 ┃ ┣ 📜feature_line_jam_s03.json
 ┃ ┣ 📜feature_toolchange_s01.csv
 ┃ ┣ 📜feature_toolchange_s01.json
 ┃ ┣ 📜feature_tooldelay_s02.csv
 ┃ ┗ 📜feature_tooldelay_s02.json
 📦mes
 ┣ 📂master_tables
 ┃ ┣ 📜alarm_code_mapping.csv
 ┃ ┗ 📜ideal_cycle_time.csv
 ┗ 📂oee
 ┃ ┣ 📜downtime_cnc.py
 ┃ ┗ 📜production_count.py
 📦notebooks
 ┣ 📂analytics
 ┃ ┣ 📜state_timeline_s01.ipynb
 ┃ ┣ 📜state_timeline_s02.ipynb
 ┃ ┗ 📜state_timeline_s03.ipynb
 ┣ 📂feature_topic
 ┃ ┣ 📜feature_topic_line_jam_s03.ipynb
 ┃ ┣ 📜feature_topic_toolchange_s01.ipynb
 ┃ ┗ 📜feature_topic_tooldelay_s02.ipynb
 ┣ 📜anomaly_detection_line_jam_s03.ipynb
 ┣ 📜anomaly_detection_toolchange_s01.ipynb
 ┗ 📜anomaly_detection_tooldely_s02.ipynb
 📦plc_tag_samples
 ┣ 📜plc_tag_cases.csv
 ┗ 📜plc_tag_cases.json