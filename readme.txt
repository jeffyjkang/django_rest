serializer:
format json, yaml, xml
product model -> serialized to json -> served through rest api

./mange.py shell
>>> from store.models import Product
>>> product = Product.objects.all()[0]
>>> from store.serializers import ProductSerializer
>>> serializer = ProductSerializer()
>>> data = serializer.to_representation(product)
>>> from rest_framework.renderers import JSONRenderer
>>> renderer = JSONRenderer()
>>> print(renderer.render(data))

product serializer -> list api view -> products list returned from our api

django rest framework generic views:
list apiview, createapiview, destroyapiview, retrieveupdatedestroyapiview
most cases:
use django rest framework's generic api views and mixins.
rare cases:
use base apiview to build up the api from the ground up.

rest_framework search filter:
default partial match
exact match: =<val>
regex

pagination:
page number pagination: use a page number to paginate res
limitOffset pagination: use a limit anf offset fields to more finely paginate res
cursor pagination: use db cursor to paginate res

simple curl commands:
curl -X POST http://localhost:8000/api/v1/products/new -d price=1.00 -d name='My Product' -d description='Hello World'
curl -X DELETE http://localhost:8000/api/v1/products/5/destroy

serializer field configuration:
read_only: whether or not the field can be written to through the serializer
source: where the data for the serializer field will be populated from
  eg: product_name = serializer.CharField(source='name')
write_only: (True) means a field can be written to but will not appear in any API response

serializer method field:
default get_ is the prefix to the field name for the method that is called.

serializer for one or many instances:
many=True: creates a list of serialized model instances
many=False: (default) will serialize only one model instance

eg for cart in the django shell:
>>> import json
>>> from store.models import *
>>> from store.serializers import *
>>> product = Product.objects.all().first()
>>> cart = ShoppingCart()
>>> cart.save()
>>> item = ShoppingCartItem(shopping_cart=cart,product=product,quantity=5)
>>> item.save()
>>> serializer = ProductSerializer(product)
>>> print(json.dumps(serializer.data,indent=2))

serializer's validated_data:
data that has already passed through serializer and model validation process, used to create or update a model.

api test case:
all test case classes implement the same interface as Django's TestCase class
remember to use the JSON format when testing API client requests: self.client.post(url, data, format='json')
