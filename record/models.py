import datetime
import time

import pytz
from django.db import models
#from numpy.core import long


class TAIFAIMeasure(models.Model):
    # LSC = Luminanza / Illuminamento da impostare
    #taiMeasurePeriod = models.IntegerField(blank=False, default=10)            # TPM = TAI Periodo misura (min)
    taiLane1NumberOfVehicles = models.IntegerField(blank=False, default=10)     #TVA = TAI Numero veicoli corsia 1 nel periodo TAI considerato
    taiLane2NumberOfVehicles = models.IntegerField(blank=False, default=20)     #TVB = TAI Numero veicoli corsia 2 nel periodo TAI considerato
    taiMeasurePeriod = models.IntegerField(blank=False, default=10)
    measure_timestamp = models.BigIntegerField( blank=False, default=161287292402)
    applicableCategory1LightLevel = models.IntegerField(blank=False, default=0)
    applicableCategory2LightLevel = models.IntegerField(blank=False, default=0)
    applicableCategory3LightLevel = models.IntegerField(blank=False, default=0)
    applicableCategory4LightLevel = models.IntegerField(blank=False, default=0)
    applicableCategory5LightLevel = models.IntegerField(blank=False, default=0)
    applicableCategory6LightLevel = models.IntegerField(blank=False, default=0)
    applicableCategory7LightLevel = models.IntegerField(blank=False, default=0)
