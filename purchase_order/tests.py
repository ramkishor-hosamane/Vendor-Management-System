from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from vendor_management.models import Vendor
from .models import PurchaseOrder
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PurchaseOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a vendor for testing
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="1234567890", address="Test Address", vendor_code="V001")

    def test_create_purchase_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('purchase-order-list-create')
        data = {
            'po_number': 'PO001',
            'vendor': self.vendor.id,  # Use vendor ID created in setUp
            'order_date': datetime(2024, 5, 7, 10, 0, 0),
            'delivery_date': datetime(2024, 5, 10, 10, 0, 0),
            'items': {'item1': 'description1'},
            'quantity': 10,
            'status': 'pending',
            'quality_rating': None,
            'issue_date': datetime(2024, 5, 7, 10, 0, 0),
            'acknowledgment_date': None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)



    def test_delete_purchase_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        purchase_order = PurchaseOrder.objects.create(po_number='PO004', vendor=self.vendor, order_date=datetime(2024, 5, 7, 10, 0, 0),
                                                       delivery_date=datetime(2024, 5, 10, 10, 0, 0), items={'item1': 'description1'},
                                                       quantity=10, status='pending', issue_date=datetime(2024, 5, 7, 10, 0, 0))
        url = reverse('purchase-order-update-destroy', kwargs={'pk': purchase_order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_update_purchase_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        purchase_order = PurchaseOrder.objects.create(po_number='PO002', vendor=self.vendor, order_date=datetime(2024, 5, 7, 10, 0, 0),
                                                       delivery_date=datetime(2024, 5, 10, 10, 0, 0), items={'item1': 'description1'},
                                                       quantity=10, status='pending', issue_date=datetime(2024, 5, 7, 10, 0, 0))
        url = reverse('purchase-order-update-destroy', kwargs={'pk': purchase_order.pk})
        data = {'status': 'completed'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        purchase_order.refresh_from_db()
        self.assertEqual(purchase_order.status, 'completed')

        # Test on-time delivery rate
        completed_orders = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed')
        on_time_delivered = completed_orders.filter(delivery_date__lte=datetime.now()).count()
        on_time_delivery_rate = on_time_delivered / completed_orders.count()
        self.assertEqual(self.vendor.on_time_delivery_rate, on_time_delivery_rate)

    def test_acknowledge_purchase_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        purchase_order = PurchaseOrder.objects.create(po_number='PO003', vendor=self.vendor, order_date=datetime(2024, 5, 7, 10, 0, 0),
                                                       delivery_date=datetime(2024, 5, 10, 10, 0, 0), items={'item1': 'description1'},
                                                       quantity=10, status='pending', issue_date=datetime(2024, 5, 7, 10, 0, 0))
        url = reverse('purchase-order-acknowledge', kwargs={'pk': purchase_order.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        purchase_order.refresh_from_db()
        self.assertIsNotNone(purchase_order.acknowledgment_date)

        # Test average response time
        response_time = purchase_order.acknowledgment_date - purchase_order.issue_date
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.average_response_time, response_time.total_seconds()/36000)

    def test_quality_rating_average(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        purchase_order1 = PurchaseOrder.objects.create(po_number='PO004', vendor=self.vendor, order_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        delivery_date=datetime(2024, 5, 10, 10, 0, 0), items={'item1': 'description1'},
                                                        quantity=10, status='pending', issue_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        acknowledgment_date=datetime(2024, 5, 8, 10, 0, 0), quality_rating=4.0)
        
        purchase_order2 = PurchaseOrder.objects.create(po_number='PO005', vendor=self.vendor, order_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        delivery_date=datetime(2024, 5, 10, 10, 0, 0), items={'item1': 'description1'},
                                                        quantity=10, status='pending', issue_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        acknowledgment_date=datetime(2024, 5, 8, 10, 0, 0), quality_rating=5.0)
        purchase_order1.status  ='completed'
        purchase_order1.save()
        purchase_order2.status  ='completed'
        purchase_order2.save()
        average_quality_rating = (purchase_order1.quality_rating + purchase_order2.quality_rating) / 2
        self.assertEqual(self.vendor.quality_rating_avg, average_quality_rating)


    def test_fulfillment_rate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        purchase_order1 = PurchaseOrder.objects.create(po_number='PO006', vendor=self.vendor, order_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        delivery_date=datetime(2024, 5, 10, 10, 0, 0), items={'item1': 'description1'},
                                                        quantity=10, status='pending', issue_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        acknowledgment_date=datetime(2024, 5, 8, 10, 0, 0), quality_rating=4)
        purchase_order1.status  ='completed'
        purchase_order1.save()
        purchase_order2 = PurchaseOrder.objects.create(po_number='PO007', vendor=self.vendor, order_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        delivery_date=datetime(2024, 5, 10, 10, 0, 0), items={'item1': 'description1'},
                                                        quantity=10, status='pending', issue_date=datetime(2024, 5, 7, 10, 0, 0))
        purchase_order2.status  ='canceled'
        purchase_order2.save()
        
        fulfillment_rate = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed').count() / PurchaseOrder.objects.filter(vendor=self.vendor).count()
        self.assertEqual(self.vendor.fulfillment_rate, fulfillment_rate)