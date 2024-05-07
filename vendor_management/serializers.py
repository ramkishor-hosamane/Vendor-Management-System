# vendor_management/serializers.py

from rest_framework import serializers
from .models import Vendor,HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class VendorHistoricalPerformanceSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
