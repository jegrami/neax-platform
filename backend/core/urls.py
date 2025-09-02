from django.urls import path

from  .views import (
    StateDataListView, 
    StateDataDatailView, 
    StateDemographicsDataListView,
    SocialUseDataListView,
    ResourceDataListView,
    InfrastructureDataListView,

    StateFullProfileView,
    StateDemographicsView,
    StateInfrastructureView,
    StateResourcesView,
    StateSocialUsesView,

     StateComparisionView,
     DemographicsComparisonView,
     SocialUseComparisonView,
     ResourceComparisonView,
     InfrastructureComparisonView
    )


urlpatterns = [

    # This set is for viewin individual state details
    path('api/states/', StateDataListView.as_view()),
    path('api/states/<int:pk>/', StateDataDatailView.as_view()),
    path('api/states/<int:state_id>/demographics/', StateDemographicsDataListView.as_view(), name="state-demographics"),
    path('api/states/<int:state_id>/social/', SocialUseDataListView.as_view(), name="social-use"),
    path('api/states/<int:state_id>/resources/', ResourceDataListView.as_view(), name="resources"),
    path('api/states/<int:state_id>/infrastructure/', InfrastructureDataListView.as_view(), name="infrastructure"),

    # This is for
    path('api/states/<int:state_id>/full/', StateFullProfileView.as_view(), name="state-full-profile"),
    path('api/states/<int:state_id>/demographics/', StateDemographicsView.as_view(), name="state-demographics"),
    path('api/states/<int:state_id>/social/', StateSocialUsesView.as_view(), name="state-social"),
    path('api/states/<int:state_id>/resources/', StateResourcesView.as_view(), name="state-resources"),
    path('api/states/<int:state_id>/infrastructure/', StateInfrastructureView.as_view(), name="state-infrastructure"),

    
    # This is for comparing two states
    path('api/states/compare/', StateComparisionView.as_view(), name="compare-states"),
    path('api/states/compare/demographics/', DemographicsComparisonView.as_view(), name="compare-demographics"),
    path('api/states/compare/social/', SocialUseComparisonView.as_view(), name="compare-social-use"),
    path('api/states/compare/resources/', ResourceComparisonView.as_view(), name="compare-resources"),
    path('api/states/compare/infrastructure/', InfrastructureComparisonView.as_view(), name="compare-infra"),
   
]

