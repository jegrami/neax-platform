from rest_framework import serializers
from .models import (
    StateData, 
    DemographicsData, 
    SocialUseData, 
    ResourceData,
    InfrastructureData,
    )

'''
Notice how I listed all the model field names instead of just using the shortcut '__all__'?
That was because i hoped the json data returned when calling the API would be sorted  in the 
order listed here. It didn't work as I expected, but i am going to leave it like this for now.
'''

class StateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateData
        fields = ['id', 'name', 'population', 'boundary', 'year', 'data_source']


class DemographicsDataSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField() # Shows the state name instead of ID
    class Meta:
        model = DemographicsData 
        fields = ["state", "poverty_rate", "mobile_ownership", "radio_ownership", 
                  "iron_sheet_roofing", "livestock_ownership", "household_electrification",
                    "year", "data_source"]


class SocialUseDataSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    class Meta:
        model = SocialUseData
        fields = ["state", "education_facilities", "health_facilities", 
                  "agricultural_zones", "mines_quarries", "commercial_activities", 
                  "public_institutions", "nighttime_lights", "year", "data_source"]
        

class ResourceDataSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = ResourceData
        fields = ["state", "solar_potential", "wind_potential", 
                  "biomass_potential", "hydro_potential", "year", "data_source"]


class InfrastructureDataSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = InfrastructureData
        fields = ["state", "transmission_lines_km", "substations_count", 
                  "mini_grids_count", "off_grid_solutions", "power_plants_count", 
                  "accessibility_to_cities", "year", "data_source"
                  ]
        