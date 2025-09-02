import json
from django.core.management.base import BaseCommand 
from core.models import StateData,  SocialUseData


class Command(BaseCommand):
    help = "Seed dataset for social use of energy"

    def handle(self, *args, **kwargs):
        with open('data/social_use.json') as f:
            data = json.load(f)

        for item in data:
            state_name = item.pop('state')
            state = StateData.objects.get(name=state_name)
            SocialUseData.objects.update_or_create(
                state=state,
                year=item['year'],
                defaults=item
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded social use data'))

        

