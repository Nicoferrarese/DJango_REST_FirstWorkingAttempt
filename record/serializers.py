from rest_framework import serializers
from record.models import TAIFAIMeasure


class RecordSerial(serializers.ModelSerializer):
    class Meta:
        model = TAIFAIMeasure
        fields = ('applicableCategory3LightLevel',
                  'applicableCategory3CategoryLightLevel',
                  'taiMeasurePeriod',
                  'taiLane1NumberOfVehicles',
                  'taiLane2NumberOfVehicles',
                  'measureTimestamp')
