from django.http.response import JsonResponse
import math

from record.models import TAIFAIMeasure
from record.serializers import RecordSerial
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def record_list(request):
    if request.method == 'GET':
        records = TAIFAIMeasure.objects.all()
        print(records)
        record_serializer = RecordSerial(records)
        return JsonResponse(record_serializer.data)


def record_detail(request, start, finish, group_time, format=None):
    #start = 0
    #finish = 161387292400
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
