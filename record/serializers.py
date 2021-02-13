from rest_framework import serializers
from record.models import TAIFAIMeasure


class RecordSerial(serializers.ModelSerializer):
    class Meta:
        model = TAIFAIMeasure
        fields = ('applicableCategory1LightLevel',
                  'applicableCategory2LightLevel',
                  'applicableCategory3LightLevel',
                  'applicableCategory4LightLevel',
                  'applicableCategory5LightLevel',
                  'applicableCategory6LightLevel',
                  'applicableCategory7LightLevel',
                  'taiMeasurePeriod',
                  'taiLane1NumberOfVehicles',
                  'taiLane2NumberOfVehicles',
                  'measure_timestamp')
