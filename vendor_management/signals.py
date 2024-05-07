from django.db.models.signals import pre_save
from django.dispatch import receiver
from vendor_management.models import Vendor
from purchase_order.models import PurchaseOrder
from django.db.models import Count
from django.db.models import F
from datetime import datetime

# @receiver(pre_save, sender=Vendor)
# def handle_on_time_delivery_rate(sender , instance:Vendor, **kwargs):
#     total_completed_pos = PurchaseOrder.objects.filter(vendor=instance, status='completed').count()
#     if total_completed_pos == 0:
#         instance.on_time_delivery_rate = 0
#         return

#     completed_pos_on_time = PurchaseOrder.objects.filter(vendor=instance, status='completed', delivery_date__lte=timezone.now()).count()
#     on_time_delivery_rate = completed_pos_on_time / total_completed_pos
#     instance.on_time_delivery_rate = on_time_delivery_rate