# myapp/management/commands/create_vendors.py

import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from vendor_management.models import Vendor

class Command(BaseCommand):
    help = 'Create vendors with real names and contact details'

    def handle(self, *args, **options):
        real_names = ['John Smith', 'Emma Johnson', 'Michael Brown', 'Emily Davis', 'Daniel Wilson', 'Olivia Martinez', 'David Anderson', 'Sophia Taylor', 'James Garcia', 'Isabella Hernandez']
        real_contact_details = ['123 Main St, City, Country', '456 Elm St, City, Country', '789 Oak St, City, Country', '321 Pine St, City, Country', '654 Maple St, City, Country']

        vendors = []
        for name, contact_details in zip(real_names, real_contact_details):
            vendor = Vendor.objects.create(
                name=name,
                contact_details=contact_details,
                address='Address of Vendor',
                vendor_code=f'V{len(vendors)+1:03}',
                on_time_delivery_rate=0.0,
                quality_rating_avg=0.0,
                average_response_time=0.0,
                fulfillment_rate=0.0
            )
            vendors.append(vendor)

        self.stdout.write(self.style.SUCCESS('Vendors created successfully.'))
