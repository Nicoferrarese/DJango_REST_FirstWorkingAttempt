"""
B0otxArSLpTsQOkPqKOfzcy7sHCnpEwz4XXmuaAyBTvPNzvZvFT0mO6A9rcpmzaHJonGPSbKY24sivaospzoHg==
B0otxArSLpTsQOkPqKOfzcy7sHCnpEwz4XXmuaAyBTvPNzvZvFT0mO6A9rcpmzaHJonGPSbKY24sivaospzoHg==
"""
from influxdb_client import InfluxDBClient, Point

username = ''
password = ''

database = 'telegraf'
retention_policy = 'autogen'

bucket = f'{database}/{retention_policy}'

client = InfluxDBClient(url='http://localhost:8086', token=f'{username}:{password}', org='-')
"""
print('*** Write Points ***')

write_api = client.write_api()

point = Point("mem").tag("host", "host1").field("used_percent", 25.43234543)
print(point.to_line_protocol())

write_api.write(bucket=bucket, record=point)
write_api.__del__()
"""
print('*** Query Points ***')

query_api = client.query_api()
query = f'from(bucket: "telegraf/autogen")\
  |> range(start: -1h)\
  |> filter(fn: (r) => r._measurement == "mqtt_consumer" and (r._field == "measure_applicableCategory3LightLevel"))'
tables = query_api.query(query)
for record in tables[0].records:
    print(f'#{record.get_time()} #{record.get_measurement()}: #{record.get_field()} #{record.get_value()}')

client.close()
