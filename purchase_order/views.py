# views.py

from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def perform_create(self, serializer):
        serializer.save()

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class PurchaseOrderModelViewSet(ModelViewSet):
    serializer_class=PurchaseOrderSerializer

from datetime import datetime
class PurchaseOrderAcknowledgeAPIView(generics.GenericAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def post(self, request, *args, **kwargs):
        instance:PurchaseOrder = self.get_object()
        #print(instance.po_number)
        #print(instance.acknowledgment_date)
        #instance.acknowledgment_date = datetime.today()
        
        #print(instance.acknowledgment_date)
        #instance.save()
        if not request.data.get('acknowledgment_date'):
            request.data['acknowledgment_date'] = datetime.today()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response(serializer.data)
