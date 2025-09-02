import json
from django.core.management.base import BaseCommand 
from core.models import StateData 

class Command(BaseCommand):
    help = "Seed all 36 states + capital (alphabetically)"

    def handle(self, *args, **kwargs):
        with open('data/states.json') as f:
            states = json.load(f)

            # firt, warehouse cleaning
            StateData.objects.all().delete()

            # then, seed the states
            for state in states:
                StateData.objects.create(name=state['name'], population=0)
            self.stdout.write(self.style.SUCCESS("Successfully seeded states data."))