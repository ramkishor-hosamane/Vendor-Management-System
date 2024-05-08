from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from vendor_management.models import HistoricalPerformance
from vendor_management.performance_metrics import insert_vendor_historical_performance_instance, get_on_time_delivery_rate,get_avg_response_time,get_fulfillment_rate,get_quality_rating_average
from purchase_order.models import po_status_changed
@receiver(po_status_changed, sender=PurchaseOrder)
def handle_po_status_change(sender, instance:PurchaseOrder,old_status, **kwargs):
    vendor_instance = instance.vendor    
    if  old_status != instance.status:
        ##Querysets for metrics caluculation
        total_pos_for_vendor_queryset =  PurchaseOrder.objects.filter(vendor=vendor_instance)
        completed_pos_for_vendor_queryset = total_pos_for_vendor_queryset.filter(status='completed')

        # Update fulfillment rate if status changes
        vendor_instance.fulfillment_rate = get_fulfillment_rate(total_pos_for_vendor_queryset)

        if instance.status == 'completed':
            # Update on_time_delivery_rate and quality_rating_avg if status changes to completed
            vendor_instance.on_time_delivery_rate = get_on_time_delivery_rate(completed_pos_for_vendor_queryset)
            vendor_instance.quality_rating_avg = get_quality_rating_average(completed_pos_for_vendor_queryset)


        vendor_instance.save()
        HistoricalPerformance.objects.create(vendor=vendor_instance,on_time_delivery_rate = vendor_instance.on_time_delivery_rate,quality_rating_avg = vendor_instance.quality_rating_avg,average_response_time = vendor_instance.average_response_time,fulfillment_rate = vendor_instance.fulfillment_rate)


@receiver(post_save, sender=PurchaseOrder)
def handle_average_response_time_change(sender, instance:PurchaseOrder,created, **kwargs):
    vendor_instance = instance.vendor
    
    # Calculate average response time upon acknowledgment
    if instance.acknowledgment_date:
        total_pos_for_vendor_queryset = PurchaseOrder.objects.filter(vendor=vendor_instance)
        vendor_instance.average_response_time = get_avg_response_time(total_pos_for_vendor_queryset)
        vendor_instance.save()
        HistoricalPerformance.objects.create(vendor=vendor_instance,on_time_delivery_rate = vendor_instance.on_time_delivery_rate,quality_rating_avg = vendor_instance.quality_rating_avg,average_response_time = vendor_instance.average_response_time,fulfillment_rate = vendor_instance.fulfillment_rate)


    