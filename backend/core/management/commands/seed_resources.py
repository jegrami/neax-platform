import json
from django.core.management.base import BaseCommand
from core.models import StateData, ResourceData

class Command(BaseCommand):
    help = "Seed resource data for each state"

    def handle(self, *args, **kwargs):
        with open('data/resources.json') as f:
            data = json.load(f)

            for item in data:
                state_name = item.pop('state')
                state = StateData.objects.get(name=state_name)
                ResourceData.objects.update_or_create(
                    state=state,
                    year=item['year'],
                    defaults=item
                )

            self.stdout.write(self.style.SUCCESS('Successfully seeded resource data'))
