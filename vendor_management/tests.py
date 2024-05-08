
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendor, HistoricalPerformance
from .serializers import VendorSerializer, VendorHistoricalPerformanceSerializer
from datetime import datetime, timedelta
from purchase_order.models import PurchaseOrder
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class VendorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


        self.vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='Contact details 1', address='Address 1', vendor_code='V001')
        self.vendor2 = Vendor.objects.create(name='Vendor 2', contact_details='Contact details 2', address='Address 2', vendor_code='V002')

    def test_vendor_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('vendor-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_vendor_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vendor = Vendor.objects.get(pk=self.vendor1.pk)
        serializer = VendorSerializer(vendor)
        self.assertEqual(response.data, serializer.data)

    def test_vendor_performance(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        purchase_order1 = PurchaseOrder.objects.create(po_number='PO004', vendor=self.vendor1, order_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        delivery_date=datetime(2024, 5, 10, 10, 0, 0), items={'item1': 'description1'},
                                                        quantity=10, status='pending', issue_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        acknowledgment_date=datetime(2024, 5, 8, 10, 0, 0), quality_rating=4.0)
        
        purchase_order2 = PurchaseOrder.objects.create(po_number='PO005', vendor=self.vendor1, order_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        delivery_date=datetime(2024, 5, 10, 10, 0, 0), items={'item1': 'description1'},
                                                        quantity=10, status='pending', issue_date=datetime(2024, 5, 7, 10, 0, 0),
                                                        acknowledgment_date=datetime(2024, 5, 8, 10, 0, 0), quality_rating=5.0)
        purchase_order1.status  ='completed'
        purchase_order1.save()
        purchase_order2.status  ='completed'
        purchase_order2.save()


        url = reverse('vendor-performance', args=[self.vendor1.pk])
        response = self.client.get(url)
        performance_objs = HistoricalPerformance.objects.filter(vendor=self.vendor1)
        serializer = VendorHistoricalPerformanceSerializer(performance_objs,many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_vendor(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('vendor-list-create')
        data = {
            'name': 'New Vendor',
            'contact_details': 'New Contact Details',
            'address': 'New Address',
            'vendor_code': 'V003'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in response.data)
        self.assertTrue(Vendor.objects.filter(name='New Vendor').exists())

    def test_update_vendor(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor1.pk])
        data = {'name': 'Updated Vendor Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.get(pk=self.vendor1.pk).name, 'Updated Vendor Name')

    def test_delete_vendor(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vendor.objects.filter(pk=self.vendor1.pk).exists())



    def test_vendor_invalid_retrieve(self):
        # Test retrieving a non-existing vendor
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('vendor-retrieve-update-destroy', args=[999])  # Non-existing vendor pk
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vendor_invalid_update(self):
        # Test updating a non-existing vendor
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('vendor-retrieve-update-destroy', args=[999])  # Non-existing vendor pk
        data = {'name': 'Updated Vendor Name'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vendor_performance_empty(self):
        # Test retrieving performance for a vendor with no historical performance data
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('vendor-performance', args=[self.vendor2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_vendor_performance_future_date(self):
        # Test retrieving performance for a future date
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        future_date = timezone.now() + timedelta(days=7)
        try:
            HistoricalPerformance.objects.create(vendor=self.vendor2, on_time_delivery_rate=0.8, quality_rating_avg=4.5, average_response_time=2.5, fulfillment_rate=0.9, date=future_date)
        except:
            pass    
        url = reverse('vendor-performance', args=[self.vendor2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])  