from django.db import models
from vendor_management.models import Vendor
from django.utils import timezone
from django.dispatch import Signal

# Define a custom signal
po_status_changed = Signal()



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,related_name='purchase_orders')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50,choices=(('pending','pending'),('completed','completed') ,('canceled','canceled')))
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
    def acknowledge(self):
        self.acknowledgment_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        # Fetch the initial values of the instance from the database
        old_instance = type(self)._base_manager.get(pk=self.pk) if self.pk else None

        # Call the original save method
        super().save(*args, **kwargs)

        # Emit the custom signal po_status_changed
        if old_instance and old_instance.status != self.status:
            po_status_changed.send(sender=self.__class__, instance=self, old_status=old_instance.status)
    def __str__(self):
        return self.po_number


