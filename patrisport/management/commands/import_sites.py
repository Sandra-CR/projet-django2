import json
from decimal import Decimal

from django.core.management.base import BaseCommand

from patrisport.models import (
    DateReference,
    Denomination,
    SiteOlympique,
    SportSite,
    Typologie,
)


class Command(BaseCommand):
    help = "Importe les sites sportifs depuis le fichier JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default="clean.json",
            help="Chemin vers le fichier JSON (par defaut: clean.json)",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            typologies = item.pop("typologie", [])
            denominations = item.pop("denomination", [])
            dates_ref = item.pop("date_s_de_reference", [])
            site_olympique_label = item.pop("site_olympique", None)
            geo = item.pop("geo", None)

            informations_acces_transport = (
                item.pop("informations_d_acces_en_transport_en_commun", "") or ""
            )

            site_olympique = None
            if site_olympique_label:
                site_olympique, _ = SiteOlympique.objects.get_or_create(
                    label=site_olympique_label
                )

            longitude = (
                Decimal(str(item.get("longitude"))) if item.get("longitude") else None
            )
            latitude = (
                Decimal(str(item.get("latitude"))) if item.get("latitude") else None
            )
            geo_lon = Decimal(str(geo.get("lon"))) if geo and geo.get("lon") else None
            geo_lat = Decimal(str(geo.get("lat"))) if geo and geo.get("lat") else None

            site, created = SportSite.objects.update_or_create(
                appellation=item.get("appellation"),
                commune=item.get("commune"),
                defaults={
                    "departement": item.get("departement"),
                    "adresse": item.get("adresse"),
                    "code_postal": item.get("code_postal"),
                    "longitude": longitude,
                    "latitude": latitude,
                    "geo_lon": geo_lon,
                    "geo_lat": geo_lat,
                    "informations_acces_transport": informations_acces_transport,
                    "datation": item.get("datation", ""),
                    "periode_de_construction": item.get("periode_de_construction", ""),
                    "historique_et_description": item.get(
                        "historique_et_description", ""
                    ),
                    "credits": item.get("credits", ""),
                    "url_image": item.get("url_image", ""),
                    "adresse_com": item.get("adresse_com", ""),
                    "site_olympique": site_olympique,
                },
            )

            for t in typologies:
                site.typologie.add(Typologie.objects.get_or_create(name=t)[0])
            for d in denominations:
                site.denomination.add(Denomination.objects.get_or_create(name=d)[0])
            for dt in dates_ref:
                site.dates_reference.add(
                    DateReference.objects.get_or_create(value=dt)[0]
                )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Cree : {site.appellation}"))
            else:
                self.stdout.write(self.style.WARNING(f"Mis a jour : {site.appellation}"))
