from django.db import models

# Create your models here.
from django.db import models

class SiteOlympique(models.Model):
    label = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Site olympique"
        verbose_name_plural = "Sites olympiques"

    def __str__(self):
        return self.label


class Typologie(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Typologie"
        verbose_name_plural = "Typologies"

    def __str__(self):
        return self.name


class Denomination(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Dénomination"
        verbose_name_plural = "Dénominations"

    def __str__(self):
        return self.name


class DateReference(models.Model):
    value = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Date de référence"
        verbose_name_plural = "Dates de référence"

    def __str__(self):
        return self.value


class SportSite(models.Model):
    departement = models.PositiveSmallIntegerField()
    commune = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=10)

    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    geo_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    geo_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    informations_acces_transport = models.TextField(blank=True)
    appellation = models.CharField(max_length=255)
    typologie = models.ManyToManyField(Typologie, blank=True, related_name="sites")
    denomination = models.ManyToManyField(Denomination, blank=True, related_name="sites")

    dates_reference = models.ManyToManyField(DateReference, blank=True, related_name="sites")
    datation = models.CharField(max_length=150, blank=True)
    periode_de_construction = models.CharField(max_length=150, blank=True)

    historique_et_description = models.TextField(blank=True)
    credits = models.CharField(max_length=255, blank=True)
    url_image = models.URLField(blank=True)
    adresse_com = models.CharField(max_length=255, blank=True)

    site_olympique = models.ForeignKey(
        SiteOlympique,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sites",
    )

    class Meta:
        verbose_name = "Site sportif"
        verbose_name_plural = "Sites sportifs"

    def __str__(self):
        return f"{self.appellation} ({self.commune})"
