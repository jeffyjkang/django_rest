import os.path
from django.conf import settings

from django.test import TestCase
from rest_framework.test import APITestCase
from store.models import Product

# Create your tests here.
class ProductCreateTestCase(APITestCase):
  def test_create_product(self):
    initial_product_count = Product.objects.count()
    product_attrs = {
      'name': 'New Product',
      'description': 'Awesome product',
      'price': '123.45',
    }
    res = self.client.post('/api/v1/products/new', product_attrs)
    if res.status_code != 201:
      print(res.data)
    self.assertEqual(
      Product.objects.count(),
      initial_product_count + 1,
    )
    for attr, expected_value in product_attrs.items():
      self.assertEqual(res.data[attr], expected_value)
    self.assertEqual(res.data['is_on_sale'], False)
    self.assertEqual(
      res.data['current_price'],
      float(product_attrs['price']),
    )

class ProductDestroyTestCase(APITestCase):
  def test_delete_product(self):
    initial_product_count = Product.objects.count()
    product_id = Product.objects.first().id
    self.client.delete('/api/v1/products/{}/'.format(product_id))
    self.assertEqual(
      Product.objects.count(),
      initial_product_count - 1
    )
    self.assertRaises(
      Product.DoesNotExist,
      Product.objects.get, id=product_id,
    )

class ProductListTestCase(APITestCase):
  def test_list_products(self):
    products_count = Product.objects.count()
    res = self.client.get('/api/v1/products/')
    self.assertIsNone(res.data['next'])
    self.assertIsNone(res.data['previous'])
    self.assertEqual(res.data['count'], products_count)
    self.assertEqual(len(res.data['results']), products_count)

class ProductUpdateTestCase(APITestCase):
  def test_update_product(self):
    product = Product.objects.first()
    res = self.client.patch(
      '/api/v1/products/{}/'.format(product.id),
      {
        'name': 'New Product',
        'description': 'Awesome product',
        'price': '123.45',
      },
      format='json',
    )
    updated = Product.objects.get(id=product.id)
    self.assertEqual(updated.name, 'New Product')
  def test_upload_product_photo(self):
    product = Product.objects.first()
    original_photo = product.photo
    photo_path = os.path.join(
      settings.MEDIA_ROOT, 'products', 'vitamin-iron.jpg',
    )
    with open(photo_path, 'rb') as photo_data:
      res = self.client.patch(
        '/api/v1/products/{}/'.format(product.id),
        { 'photo': photo_data },
        format='multipart',
      )
      self.assertEqual(res.status_code, 200)
      self.assertNotEqual(res.data['photo'], original_photo)
      try:
        updated = Product.objects.get(id=product.id)
        expected_photo = os.path.join(
          settings.MEDIA_ROOT, 'products', 'vitamin-iron',
        )
        self.assertTrue(
          updated.photo.path.startswith(expected_photo)
        )
      finally:
        os.remove(updated.photo.path)
