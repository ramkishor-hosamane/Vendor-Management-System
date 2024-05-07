# vendor_management/urls.py

from django.urls import path
from .views import VendorListCreateAPIView, VendorRetrieveUpdateDestroyAPIView,VendorPerformanceAPIView

urlpatterns = [
    path('', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('<int:pk>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),
    path('<int:pk>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),

]
