
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from purchase_order.models import  PurchaseOrder
from vendor_management.models import Vendor
from datetime import timedelta
class Command(BaseCommand):
    help = 'Generate purchase orders with real-life item names'

    def handle(self, *args, **options):
        real_items = [
            'Laptop', 'Smartphone', 'Desk', 'Chair', 'Printer', 'Monitor', 'Keyboard', 'Mouse', 'Headphones', 'Tablet',
            'Backpack', 'Camera', 'Sunglasses', 'Watch', 'Wallet', 'Book', 'Pen', 'Notebook', 'Calendar', 'Water Bottle',
            'Coffee Mug', 'Umbrella', 'Towel', 'Sunscreen', 'Hat', 'Scarf', 'Gloves', 'Socks', 'Shoes', 'T-shirt',
            'Jeans', 'Dress', 'Skirt', 'Jacket', 'Sweater', 'Coat', 'Suit', 'Tie', 'Belt', 'Pajamas',
            'Toothbrush', 'Toothpaste', 'Shampoo', 'Conditioner', 'Soap', 'Razor', 'Shaving Cream', 'Deodorant', 'Perfume', 'Hairbrush',
            'Hairdryer', 'Curling Iron', 'Straightener', 'Makeup Bag', 'Foundation', 'Concealer', 'Blush', 'Eyeshadow', 'Eyeliner', 'Mascara',
            'Lipstick', 'Nail Polish', 'Sunblock', 'Lotion', 'Tissues', 'Medicine', 'Bandages', 'First Aid Kit', 'Thermometer', 'Cotton Swabs',
            'Laundry Detergent', 'Fabric Softener', 'Bleach', 'Stain Remover', 'Dish Soap', 'Sponge', 'Dish Towel', 'Trash Bags', 'Ziploc Bags',
            'Aluminum Foil', 'Plastic Wrap', 'Paper Towels', 'Cleaning Spray', 'Vacuum Cleaner', 'Broom', 'Dustpan', 'Mop', 'Bucket',
            'Flashlight', 'Batteries', 'Candles', 'Matches', 'Lighter', 'Fire Extinguisher', 'Smoke Detector', 'Carbon Monoxide Detector', 'Emergency Kit'
        ]

        vendors = Vendor.objects.all()

        for i in range(2000):
            vendor = random.choice(vendors)
            order_date = timezone.now()
            delivery_date = order_date + timedelta(days=random.randint(1, 30))  # Random delivery date after order_date
            issue_date = order_date + timedelta(days=random.randint(1, 10))  # Random issue date after order_date
          
            purchase_order = PurchaseOrder.objects.create(
                po_number=f'PO{i+1:05}',
                vendor=vendor,
                order_date=order_date,
                delivery_date=delivery_date,
                items={'item': random.choice(real_items)},
                quantity=random.randint(1, 30),
                status=random.choice(['pending']),
                quality_rating=None,
                issue_date=issue_date,
                acknowledgment_date=None
            )
            purchase_order.save()

        self.stdout.write(self.style.SUCCESS('Purchase orders created successfully.'))
