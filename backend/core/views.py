
from rest_framework import generics
from rest_framework import status

from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import (
    StateData,
    DemographicsData,
    SocialUseData,
    ResourceData,
    InfrastructureData,
    )

from core.serializers import (
    StateDataSerializer,
    DemographicsDataSerializer,
    SocialUseDataSerializer,
    ResourceDataSerializer,
    InfrastructureDataSerializer,
    )


'''
The views are all fucked up. There may be some major redundancies. I'll 
come back it to it later
'''

# Lists all the states with their basic data (boundary, population)
class StateDataListView(generics.ListCreateAPIView):
    
    serializer_class = StateDataSerializer

    
    def get_queryset(self):
        queryset = StateData.objects.all()
        name = self.request.query_params.get('name')

        if name:
            queryset = queryset.filter(name__iexact=name)
        return queryset


class StateDataDatailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StateData.objects.all()
    serializer_class = StateDataSerializer


# Single state data accross all categories
class StateFullProfileView(APIView):
    def get(self, request, state_id):
        state = (
            StateData.objects
            .select_related("demographics", "social_uses", "resources", "infrastructure")
            .filter(id=state_id)
            .first()
        )
        if not state:
            return Response({"error": "State not found"}, status=status.HTTP_404_NOT_FOUND)

        profile = {
            "state": StateDataSerializer(state).data,
            "demographics": DemographicsDataSerializer(getattr(state, "demographics", None), allow_null=True).data or {},
            "social_uses": SocialUseDataSerializer(getattr(state, "social_uses", None), allow_null=True).data or {},
            "resources": ResourceDataSerializer(getattr(state, "resources", None), allow_null=True).data or {},
            "infrastructure": InfrastructureDataSerializer(getattr(state, "infrastructure", None), allow_null=True).data or {},
        }

        return Response(profile)

    

# For creating or viewing a single category
class StateDemographicsDataListView(generics.ListCreateAPIView):
    serializer_class = DemographicsDataSerializer

    def get_queryset(self):
        state_id = self.kwargs['state_id']
        
        get_object_or_404(StateData, id=state_id)
        return DemographicsData.objects.filter(state_id=state_id)

    def perform_create(self, serializer):
        
        state_id = self.kwargs['state_id']
        state = get_object_or_404(StateData, id=state_id)
        serializer.save(state=state)


class SocialUseDataListView(generics.ListCreateAPIView):
    serializer_class = SocialUseDataSerializer

    def get_queryset(self):
        state_id = self.kwargs['state_id']
        get_object_or_404(StateData, id=state_id)
        return SocialUseData.objects.filter(state_id=state_id)
    
    def perform_create(self, serializer):
        state_id = self.kwargs['state_id']
        state = get_object_or_404(StateData, id=state_id)
        serializer.save(state=state)

class ResourceDataListView(generics.ListCreateAPIView):
    serializer_class = ResourceDataSerializer

    def get_queryset(self):
        state = self.kwargs['state_id']
        get_object_or_404(StateData, id=state)
        return ResourceData.objects.filter(state_id=state)
    
    def perform_create(self, serializer):
        state_id = self.kwargs['state_id']
        state = get_object_or_404(StateData, id=state_id)
        serializer.save(state=state)
    

class InfrastructureDataListView(generics.ListCreateAPIView):
    serializer_class = InfrastructureDataSerializer

    def get_queryset(self):
        state_id = self.kwargs['state_id']
        get_object_or_404(StateData, id=state_id)
        return InfrastructureData.objects.filter(state_id=state_id)
    
    def perform_create(self, serializer):
        state_id = self.kwargs['state_id']
        state = get_object_or_404(StateData, id=state_id)
        serializer.save(state=state)




class StateCategoryView(APIView):
    model = None 
    serializer_class = None

    def get(self, request, state_id):
        state = get_object_or_404(StateData, id=state_id)
        obj = self.model.objects.filter(state=state).first()
        data = self.serializer_class(obj).data.first() if obj else {}
        return Response({"state": state.name, "data": data})


class StateDemographicsView(StateCategoryView):
    model = DemographicsData
    serializer_class = DemographicsDataSerializer

class StateSocialUsesView(StateCategoryView):
    model = SocialUseData
    serializer_class = SocialUseDataSerializer

class StateResourcesView(StateCategoryView):
    model = ResourceData
    serializer_class = ResourceDataSerializer

class StateInfrastructureView(StateCategoryView):
    model = InfrastructureData
    serializer_class = InfrastructureDataSerializer


# data comparison views
class StateComparisionView(APIView):
    def get(self, request):
        state_a = request.query_params.get('a')
        state_b = request.query_params.get('b')

        if not (state_a and state_b):
            return Response(
                {"error": "You need to provide two states for comparison"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch both states in one query, with all related data
        states = (
            StateData.objects
            .select_related("demographics", "social_uses", "resources", "infrastructure")
            .filter(Q(name__iexact=state_a.strip()) | Q(name__iexact=state_b.strip()))
        )

        if states.count() != 2:
            return Response(
                {"error": "One or both states not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        def get_full_profile(state):
            return {
                "state": StateDataSerializer(state).data,
                "demographics": DemographicsDataSerializer(
                    getattr(state, "demographics", None), allow_null=True
                ).data or {},
                "social_uses": SocialUseDataSerializer(
                    getattr(state, "social_uses", None), allow_null=True
                ).data or {},
                "resources": ResourceDataSerializer(
                    getattr(state, "resources", None), allow_null=True
                ).data or {},
                "infrastructure": InfrastructureDataSerializer(
                    getattr(state, "infrastructure", None), allow_null=True
                ).data or {},
            }

        profiles = [get_full_profile(state) for state in states]
        return Response(profiles, status=status.HTTP_200_OK)



class CategoryComparisonView(APIView):
    model = None
    serializer_class = None 

    def get(self, request):
        state_a = request.query_params.get('a')
        state_b = request.query_params.get('b')

        if not (state_a and state_b):
            return Response(
                {'error': "You need to provide two states for comparison"},
                status=status.HTTP_404_NOT_FOUND
            )
        states = StateData.objects.filter(Q(name__iexact=state_a) | Q(name__iexact=state_b))

        if states.count() != 2:
            return Response(
                {'error': 'One or both states not found. Please check the names and try again'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        data = []
        for state in states:
            obj = self.model.objects.filter(state=state).first()
            data.append({
                "state": state.name,
                "data": self.serializer_class(obj).data if obj else {}
            })
        
        return Response(data, status=status.HTTP_200_OK)
    

class DemographicsComparisonView(CategoryComparisonView):
    model = DemographicsData
    serializer_class = DemographicsDataSerializer

class SocialUseComparisonView(CategoryComparisonView):
    model = SocialUseData
    serializer_class = SocialUseDataSerializer

class ResourceComparisonView(CategoryComparisonView):
    model = ResourceData
    serializer_class = ResourceDataSerializer

class InfrastructureComparisonView(CategoryComparisonView):
    model = InfrastructureData
    serializer_class = InfrastructureDataSerializer
    