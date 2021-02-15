from django.http.response import JsonResponse, HttpResponse
import math

from record.models import TAIFAIMeasure
from record.serializers import RecordSerial
from rest_framework.decorators import api_view
from influxdb_client import InfluxDBClient
@api_view(['GET', 'POST', 'DELETE'])

def INFLUX_API():
    username = ''
    password = ''
    database = 'telegraf'
    retention_policy = 'autogen'
    bucket = f'{database}/{retention_policy}'
    client = InfluxDBClient(url='http://localhost:8086', token=f'{username}:{password}', org='-')
    query_api = client.query_api()
    query = f'from(bucket: "'+bucket+'")\
    |> range(start: -24h)\
    |> filter(fn: (r) => r._measurement == "mqtt_consumer" \
                    and (   r._field == "measure_taiLane1NumberOfVehicles" or \
                            r._field == "measure_taiLane2NumberOfVehicles" or \
                            r._field == "measure_taiMeasurePeriod" or\
                            r._field == "measure_applicableCategory1LightLevel" or\
                            r._field == "measure_applicableCategory2LightLevel" or\
                            r._field == "measure_applicableCategory3LightLevel" or\
                            r._field == "measure_applicableCategory4LightLevel" or\
                            r._field == "measure_applicableCategory5LightLevel" or\
                            r._field == "measure_applicableCategory6LightLevel" or\
                            r._field == "measure_applicableCategory7LightLevel" or\
                            r._field == "measure_timestamp"))\
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")\
        |> window(every: 1h)\
        |> group(columns: ["host", "_measurement"], mode:"by")'
    tables = query_api.query(query)
    client.close()
    return tables
def record_database_timescale(request, start, finish, group_time):
    group_time = group_time.replace("_", " ")
    query = ('SELECT extract(epoch from (time_bucket(\'%s\', time at time zone \'utc\' at time zone \'cet\'))) AS five_min,'
                    '1 as id,'
                    'ROUND(avg("measure_taiMeasurePeriod")::numeric,0) as "taiMeasurePeriod",'
                    'ROUND(avg("measure_taiLane1NumberOfVehicles")::numeric,0) as "taiLane1NumberOfVehicles",'
                    'ROUND(avg("measure_taiLane2NumberOfVehicles")::numeric,0) as "taiLane2NumberOfVehicles",'
                    'ROUND(avg("measure_applicableCategory1LightLevel")::numeric,0) as "applicableCategory1LightLevel",'
                    'ROUND(avg("measure_applicableCategory2LightLevel")::numeric,0) as "applicableCategory2LightLevel",'
                    'ROUND(avg("measure_applicableCategory3LightLevel")::numeric,0) as "applicableCategory3LightLevel",'
                    'ROUND(avg("measure_applicableCategory4LightLevel")::numeric,0) as "applicableCategory4LightLevel",'
                    'ROUND(avg("measure_applicableCategory5LightLevel")::numeric,0) as "applicableCategory5LightLevel",'
                    'ROUND(avg("measure_applicableCategory6LightLevel")::numeric,0) as "applicableCategory6LightLevel",'
                    'ROUND(avg("measure_applicableCategory7LightLevel")::numeric,0) as "applicableCategory7LightLevel"'
                    'FROM mqtt_consumer '
                    'where measure_timestamp > %s and measure_timestamp < %s'
                    " GROUP BY five_min "
                    " ORDER BY five_min ") % (group_time, start, finish)
    records = TAIFAIMeasure.objects.raw(query)
    for record in records:
        record.measure_timestamp = record.five_min * 1000
    record_serializer = RecordSerial(records, many=True)
    return JsonResponse(record_serializer.data, safe=False)

def record_database_influx(request):
    tables = INFLUX_API()
    toSend = []
    for record in tables[0].records:
        obj = TAIFAIMeasure()
        obj.taiLane1NumberOfVehicles = record.values.get("measure_taiLane1NumberOfVehicles")
        obj.taiLane2NumberOfVehicles = record.values.get("measure_taiLane2NumberOfVehicles")
        obj.applicableCategory1LightLevel = record.values.get("measure_applicableCategory1LightLevel")
        obj.applicableCategory2LightLevel = record.values.get("measure_applicableCategory2LightLevel")
        obj.applicableCategory3LightLevel = record.values.get("measure_applicableCategory3LightLevel")
        obj.applicableCategory4LightLevel = record.values.get("measure_applicableCategory4LightLevel")
        obj.applicableCategory5LightLevel = record.values.get("measure_applicableCategory5LightLevel")
        obj.applicableCategory6LightLevel = record.values.get("measure_applicableCategory6LightLevel")
        obj.applicableCategory7LightLevel = record.values.get("measure_applicableCategory7LightLevel")
        obj.taiMeasurePeriod = record.values.get("measure_taiMeasurePeriod")
        obj.measure_timestamp = record.values.get("measure_timestamp")
        print(f'test: {obj.measure_timestamp}')
        toSend.append(obj)
    print(len(toSend))
    record_serializer = RecordSerial(toSend, many=True)
    return JsonResponse(record_serializer.data, safe=False)



def record_detail(request, start, finish, group_time, format=None):
    start = 0
    finish = 161387292400
    queryset = TAIFAIMeasure.objects.filter(measureTimestamp__gte=start,
                                            measureTimestamp__lte=finish).order_by('measureTimestamp')
    #print("Record-Detail_request")
    for x in queryset:
        #print('timestamp: {d}'.format(d=x.measureTimestamp))
        group_time = int(group_time)
        x.taiLane1NumberOfVehicles = math.trunc(x.taiLane1NumberOfVehicles * (60 / x.taiMeasurePeriod))
        x.taiLane2NumberOfVehicles = math.trunc(x.taiLane2NumberOfVehicles * (60 / x.taiMeasurePeriod))
        #print('vehicles per hour: {d}'.format(d=x.taiLane1NumberOfVehicles))

    result = result_normalizer(queryset, group_time)
    # print("sending:")
    # for x in result:
        # x.measureTimestamp = 1606376204040
        # print('-->timestamp: {d}'.format(d=x.measureTimestamp))
        # print('-->vehicles per hour: {d}'.format(d=x.taiLane1NumberOfVehicles))
    record_serializer = RecordSerial(result, many=True)
    return JsonResponse(record_serializer.data, safe=False)


def result_normalizer(queryset, minutes_to_group):
    input_length = len(queryset) - 1
    last_element_index = input_length
    index = input_length
    result = []
    while index > 0:
        item_in_this_section = 0
        to_push = TAIFAIMeasure()
        while queryset[last_element_index].measureTimestamp < (
                queryset[index].measureTimestamp + (minutes_to_group * 60000)):
            to_push = adder(to_push, queryset[index])
            index -= 1
            item_in_this_section += 1
            if index < 0:
                index = 0
                break
        divider(to_push, item_in_this_section)
        to_push.measureTimestamp = queryset[index].measureTimestamp + math.trunc(
            (queryset[last_element_index].measureTimestamp
             - queryset[index].measureTimestamp) / 2)
        last_element_index = index
        result.insert(0, to_push)
    return result


def adder(record: TAIFAIMeasure, value: TAIFAIMeasure):
    record.taiLane1NumberOfVehicles += value.taiLane1NumberOfVehicles
    record.taiLane2NumberOfVehicles += value.taiLane2NumberOfVehicles
    record.applicableCategory1LightLevel += value.applicableCategory1LightLevel
    record.applicableCategory2LightLevel += value.applicableCategory2LightLevel
    record.applicableCategory3LightLevel += value.applicableCategory3LightLevel
    record.applicableCategory4LightLevel += value.applicableCategory4LightLevel
    record.applicableCategory5LightLevel += value.applicableCategory5LightLevel
    record.applicableCategory6LightLevel += value.applicableCategory6LightLevel
    record.applicableCategory7LightLevel += value.applicableCategory7LightLevel
    return record


def divider(to_push, n_items):
    to_push.taiLane1NumberOfVehicles = math.trunc(to_push.taiLane1NumberOfVehicles / n_items)
    to_push.taiLane2NumberOfVehicles = math.trunc(to_push.taiLane2NumberOfVehicles / n_items)
    to_push.applicableCategory1LightLevel = math.trunc(to_push.applicableCategory1LightLevel / n_items)
    to_push.applicableCategory2LightLevel = math.trunc(to_push.applicableCategory2LightLevel / n_items)
    to_push.applicableCategory3LightLevel = math.trunc(to_push.applicableCategory3LightLevel / n_items)
    to_push.applicableCategory4LightLevel = math.trunc(to_push.applicableCategory4LightLevel / n_items)
    to_push.applicableCategory5LightLevel = math.trunc(to_push.applicableCategory5LightLevel / n_items)
    to_push.applicableCategory6LightLevel = math.trunc(to_push.applicableCategory6LightLevel / n_items)
    to_push.applicableCategory7LightLevel = math.trunc(to_push.applicableCategory7LightLevel / n_items)
