import json
from django.core.management.base import BaseCommand
from core.models import StateData, InfrastructureData

class Command(BaseCommand):
    help = "Seeder for the infra data of each state"

    def handle(self, *args, **kwargs):
        with open('data/infra.json') as f:
            data = json.load(f)

            for item in data:
                state_name = item.pop('state')
                state = StateData.objects.get(name=state_name)
                InfrastructureData.objects.update_or_create(
                    state=state,
                    year=item['year'],
                    defaults=item
                )
            
            self.stdout.write(self.style.SUCCESS('Successfully seeded infrastructure data'))
        