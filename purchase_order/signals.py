from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from vendor_management.performance_metrics import insert_vendor_historical_performance_instance, get_on_time_delivery_rate,get_avg_response_time,get_fulfillment_rate,get_quality_rating_average
from purchase_order.models import po_status_changed
@receiver(po_status_changed, sender=PurchaseOrder)
def handle_po_status_change(sender, instance:PurchaseOrder,old_status, **kwargs):
    # Check if the purchase order is being updated and its status is changing to 'completed'
    #print("Working boom boom")
    #print(kwargs)
    try:
        vendor_instance = instance.vendor
        old_instance = PurchaseOrder.objects.get(pk=instance.pk)

        ##Querysets for metrics caluculation
        total_pos_for_vendor_queryset =  PurchaseOrder.objects.filter(vendor=vendor_instance)
        completed_pos_for_vendor_queryset = total_pos_for_vendor_queryset.filter(status='completed')

        
        # Update fulfillment rate if status changes
        if  old_status != instance.status:
            total_pos_for_vendor_queryset =  PurchaseOrder.objects.filter(vendor=vendor_instance)
            completed_pos_for_vendor_queryset = total_pos_for_vendor_queryset.filter(status='completed')
            vendor_instance.fulfillment_rate = get_fulfillment_rate(total_pos_for_vendor_queryset)

            if instance.status == 'completed':
                vendor_instance.on_time_delivery_rate = get_on_time_delivery_rate(completed_pos_for_vendor_queryset)
                vendor_instance.quality_rating_avg = get_quality_rating_average(completed_pos_for_vendor_queryset)


        # Calculate average response time upon acknowledgment
        vendor_instance.save()

    except PurchaseOrder.DoesNotExist:
        pass  # Ignore if the old instance doesn't exist (e.g., new instance)


@receiver(post_save, sender=PurchaseOrder)
def handle_average_response_time_change(sender, instance:PurchaseOrder,created, **kwargs):
    vendor_instance = instance.vendor
    total_pos_for_vendor_queryset = PurchaseOrder.objects.filter(vendor=vendor_instance)

    if instance.acknowledgment_date:
        vendor_instance.average_response_time = get_avg_response_time(total_pos_for_vendor_queryset)
            