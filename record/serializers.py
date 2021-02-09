from rest_framework import serializers
from record.models import TAIFAIMeasure


class RecordSerial(serializers.ModelSerializer):
    class Meta:
        model = TAIFAIMeasure
        fields = ('applicableCategory3LightLevel',
                  'taiMeasurePeriod',
                  'taiLane1NumberOfVehicles',
                  'taiLane2NumberOfVehicles',
                  'measureTimestamp')
