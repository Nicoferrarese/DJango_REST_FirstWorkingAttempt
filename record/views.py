
from django.http.response import JsonResponse
from record.models import TAIFAIMeasure
from record.serializers import RecordSerial
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def record_list(request):
    if request.method == 'GET':
        records = TAIFAIMeasure.objects.all()
        print(records)
        record_serializer = RecordSerial(records, many=True)
        return JsonResponse(record_serializer.data, safe=False)

