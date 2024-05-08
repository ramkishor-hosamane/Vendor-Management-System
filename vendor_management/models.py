
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)
    def clean(self):
        # Ensure on_time_delivery_rate is between 0 and 100
        if not 0 <= self.on_time_delivery_rate <= 100:
            raise ValidationError("On-time delivery rate must be between 0 and 100.")

        # Ensure average_response_time is greater than or equal to 0
        if self.average_response_time < 0:
            raise ValidationError("Average response time cannot be negative.")

        # Ensure fulfillment_rate is between 0 and 100
        if not 0 <= self.fulfillment_rate <= 100:
            raise ValidationError("Fulfillment rate must be between 0 and 100.")
        return super().clean()
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"
    
    def clean(self):
        # Ensure date is not in the future
        if  self.date and self.date > timezone.now():
            raise ValidationError("Date cannot be in the future.")

        # Ensure on_time_delivery_rate is between 0 and 100
        if not 0 <= self.on_time_delivery_rate <= 100:
            raise ValidationError("On-time delivery rate must be between 0 and 100.")

        # Ensure average_response_time is greater than or equal to 0
        if self.average_response_time < 0:
            raise ValidationError("Average response time cannot be negative.")

        # Ensure fulfillment_rate is between 0 and 100
        if not 0 <= self.fulfillment_rate <= 100:
            raise ValidationError("Fulfillment rate must be between 0 and 100.")
    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)