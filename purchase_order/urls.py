
from django.urls import path
from .views import PurchaseOrderListCreateAPIView,PurchaseOrderRetrieveUpdateDestroyAPIView,PurchaseOrderAcknowledgeAPIView,PurchaseOrderModelViewSet

urlpatterns = [
    path('', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('<int:pk>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-update-destroy'),
    #path('', PurchaseOrderModelViewSet.as_view({'get':'list','post':'create'}), name='purchase-order-list-create'),
    #path('<int:pk>/', PurchaseOrderModelViewSet.as_view({'get':'retrieve','post':'create'}), name='purchase-order-update-destroy'),

    path('<int:pk>/acknowledge/', PurchaseOrderAcknowledgeAPIView.as_view(), name='purchase-order-acknowledge'),
]
