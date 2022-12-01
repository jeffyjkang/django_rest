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