# vendor_management/views.py

from rest_framework import generics
from .models import Vendor,HistoricalPerformance
from .serializers import VendorSerializer,VendorHistoricalPerformanceSerializer
from rest_framework.response import Response

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = VendorHistoricalPerformanceSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)