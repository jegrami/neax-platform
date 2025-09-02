'''
For the models, i try to mirror the Energy Access Explorer data structure, 
which divides their dataset into four categories: `Demographics`, `Social/Productive use`,
`Resources`, and `Infrastructure`, each one displays a specific set of data points.
'''

from django.db import models

# Create your models here.

class StateData(models.Model):
    """
    This represents the basic state data universal to all states
    """
    name = models.CharField(max_length=100, unique=True)
    population = models.BigIntegerField()
    boundary = models.JSONField(null=True, blank=True, help_text= "GoeJSON boundary of the state")
    year = models.IntegerField(null=True, blank=True)
    data_source = models.CharField(max_length=255, null=True, blank=True)



    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "State Data"
        verbose_name_plural = "States Data"



class DemographicsData(models.Model):
    """
    Holds the demographics data for a state. "Demographics" in the sense of 
    "Descriptive statics or characteristics" ... at least that's how i mean it. 
    """
    state = models.OneToOneField(StateData, on_delete=models.CASCADE, related_name="demographics")
    poverty_rate = models.FloatField(null=True, blank=True)
    mobile_ownership = models.FloatField(null=True, blank=True)
    radio_ownership = models.FloatField(null=True, blank=True)
    iron_sheet_roofing = models.FloatField(null=True, blank=True)
    livestock_ownership = models.FloatField(null=True, blank=True)
    household_electrification = models.FloatField(null=True, blank=True) 
    year = models.IntegerField()
    data_source = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.state.name} Demographics {self.year}"



class SocialUseData(models.Model):
    """
    How the state uses energy for social purposes.
    """
    state = models.OneToOneField(StateData, on_delete=models.CASCADE, related_name="social_uses")
    education_facilities = models.IntegerField(help_text="Number of education facilities", null=True, blank=True)
    health_facilities = models.IntegerField(help_text="Number of health facilities", null=True, blank=True)
    agricultural_zones = models.FloatField(help_text="Agricultural land area or index", null=True, blank=True)
    mines_quarries = models.IntegerField(help_text="Number of mines and quarries", null=True, blank=True)
    commercial_activities = models.IntegerField(help_text="Estimated number of SMEs/commercial activities", null=True, blank=True)
    public_institutions = models.IntegerField(help_text="Number of public institutions", null=True, blank=True)
    nighttime_lights = models.FloatField(help_text="Average nighttime light intensity", null=True, blank=True)
    year = models.IntegerField()
    data_source = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.state.name} Energy for Social use - {self.year}"
    

class ResourceData(models.Model):
    """
    Holds data about resources in the state that could be used for energy generation .
    """
    state = models.OneToOneField(StateData, on_delete=models.CASCADE, related_name="resources")
    solar_potential = models.FloatField(help_text="Average solar irradiation (kWh/m2/day)", null=True, blank=True)
    wind_potential = models.FloatField(help_text="Average wind speed (m/s)", null=True, blank=True)
    biomass_potential = models.FloatField(help_text="Biomass potential (tons/year or GWh)", null=True, blank=True)
    hydro_potential = models.FloatField(help_text="Small/medium hydro potential (MW)", null=True, blank=True)
    year = models.IntegerField()
    data_source = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.state.name} Resource Data - {self.year}"
    

class InfrastructureData(models.Model):
    """ 
    Holds data about the energy infrastructure in the state.
    """
    state = models.OneToOneField(StateData, on_delete=models.CASCADE, related_name="infrastructure")
    transmission_lines_km = models.FloatField(help_text="Length of transmission lines (km)", null=True, blank=True)
    substations_count = models.IntegerField(help_text="Number of substations", null=True, blank=True)
    mini_grids_count = models.IntegerField(help_text="Number of operational mini-grids", null=True, blank=True)
    off_grid_solutions = models.IntegerField(help_text="Number of off-grid installations (SHS, community systems)", null=True, blank=True)
    power_plants_count = models.IntegerField(help_text="Number of power plants", null=True, blank=True)
    accessibility_to_cities = models.FloatField(help_text="Average travel time to nearest city (minutes)", null=True, blank=True)
    year = models.IntegerField()
    data_source = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.state.name} Infrastructure Data - {self.year}"



