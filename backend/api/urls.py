from django.urls import path
from .views import status, SocialMediaAgentView

urlpatterns = [
    path('status/', status),
    path('agent/', SocialMediaAgentView.as_view())
]
