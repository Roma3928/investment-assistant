from django.urls import path
from .views import *
from .models import *

urlpatterns = [
    path('', index, name='home'),
    path('tax', TaxView.as_view(), name='tax'),
    path('analytics', PromotionListView.as_view(), name='analytics'),
    path('companies/<str:symbol>/', CompanyDetailView.as_view(), name='company-detail'),
]
