from django.db import models

class TAIFAIMeasure(models.Model):
    applicableCategory3LightLevel = models.IntegerField(blank=False, default=0)           # LSC = Luminanza / Illuminamento da impostare
    applicableCategory3CategoryLightLevel = models.IntegerField(blank=False, default=0)    # Light level della categoria collegata
    taiMeasurePeriod = models.IntegerField(blank=False, default=10)            # TPM = TAI Periodo misura (min)
    taiLane1NumberOfVehicles = models.IntegerField(blank=False, default=0)     #TVA = TAI Numero veicoli corsia 1 nel periodo TAI considerato
    taiLane2NumberOfVehicles = models.IntegerField(blank=False, default=0)     #TVB = TAI Numero veicoli corsia 2 nel periodo TAI considerato
    measureTimestamp = models.CharField(max_length=30, blank=False, default=0)
