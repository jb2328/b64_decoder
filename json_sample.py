import json

f='{ "app_id": "cambridge-sensor-network","dev_id": "elsys-ems-048f2b","hardware_serial": "A81758FFFE048F2B","port": 5,"counter": 10393,"payload_raw": "AQDqAh4DAj70Bw4oCwAAAOkNAA8AEgA=","payload_fields": {"accMotion": 0, "device": "elsys", "digital": 0} }'
sample_file=json.loads(f)
