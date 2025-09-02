import json 
from django.core.management.base import BaseCommand 

from core.models import StateData, DemographicsData

class Command(BaseCommand):
    help = "Seed demographic data of Nigerian states"

    def handle(self, *args, **kwargs):
        with open('data/demographics.json') as f:
            data = json.load(f)

        for item in data:
            state_name = item.pop('state')
            state, _ = StateData.objects.get_or_create(name=state_name, defaults={'population': 0})

            DemographicsData.objects.update_or_create(
                    state=state,
                    year=item['year'],
                    defaults=item     
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded demographic data.'))