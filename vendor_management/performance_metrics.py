from vendor_management.models import HistoricalPerformance,Vendor
from purchase_order.models import PurchaseOrder
from django.utils import timezone
from django.db.models import Avg, ExpressionWrapper, F, fields
from django.db.models.functions import Coalesce
from datetime import timedelta
def insert_vendor_historical_performance_instance(vendor_instance:Vendor):
    HistoricalPerformance.objects.create(
        vendor=vendor_instance,
        on_time_delivery_rate=vendor_instance.on_time_delivery_rate,
        quality_rating_avg=vendor_instance.quality_rating_avg,
        average_response_time=vendor_instance.average_response_time,
        fulfillment_rate=vendor_instance.fulfillment_rate
    )

def get_on_time_delivery_rate(completed_pos_for_vendor_queryset):
    total_completed_pos = completed_pos_for_vendor_queryset.count()
    if total_completed_pos == 0:
        on_time_delivery_rate = 0
    else:
        completed_pos_on_time = completed_pos_for_vendor_queryset.filter(delivery_date__lte=timezone.now()).count()
        on_time_delivery_rate = completed_pos_on_time / total_completed_pos
    return float(on_time_delivery_rate)


def get_quality_rating_average(completed_pos_for_vendor_queryset):

    res =  completed_pos_for_vendor_queryset.filter(quality_rating__isnull=False).aggregate(
    quality_rating_avg=Coalesce(Avg(F('quality_rating')),0.0))['quality_rating_avg']
    return res


def get_avg_response_time(total_pos_for_vendor_queryset):
    
    response_time_expr = ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=fields.DurationField()
        )
        
    # Aggregate and compute the average response time
    avg_response_time:timedelta = total_pos_for_vendor_queryset.annotate(
        response_time=response_time_expr
    ).aggregate(
        avg_response_time=Avg('response_time', output_field=fields.DurationField())
    )['avg_response_time']
    
    return float(avg_response_time.total_seconds()/36000) if avg_response_time else 0.0


def get_fulfillment_rate(total_pos_for_vendor_queryset):

    # Count the total number of POs issued to the vendor
    total_count = total_pos_for_vendor_queryset.count()

    # Count the number of successfully fulfilled POs (status 'completed' without issues)
    fulfilled_count = total_pos_for_vendor_queryset.filter(
        status='completed',
        issue_date__isnull=False,  # Assuming issue_date is set when PO is issued
        acknowledgment_date__isnull=False  # Assuming acknowledgment_date is set when PO is acknowledged
    ).count()
    
    
    # Calculate fulfillment rate
    if total_count > 0:
        fulfillment_rate = fulfilled_count / total_count
    else:
        fulfillment_rate = 0.0  # Default to 0 if there are no POs
    
    return float(fulfillment_rate)