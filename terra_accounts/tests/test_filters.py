from rest_framework import generics
from rest_framework.settings import api_settings
from rest_framework.test import APIRequestFactory, APITestCase

from terra_accounts.models import TerraUser
from terra_accounts.serializers import TerraUserSerializer

factory = APIRequestFactory()


class JSONOrderingTestCase(APITestCase):
    def setUp(self):
        for idx in range(3):
            data = {
                'email': 'a' * (idx + 1),
                'properties': {
                    'key': idx,
                }
            }
            # using Layer model as fake tests models needs lot of development
            TerraUser.objects.create(**data)

    def test_json_ordering(self):
        class OrderingListView(generics.ListAPIView):
            permission_classes = ()
            queryset = TerraUser.objects.all().order_by('pk')
            serializer_class = TerraUserSerializer
            filter_backends = (JSONFieldOrderingFilter, )
            ordering_fields = ['properties', ]

        view = OrderingListView.as_view()

        # testing ascending
        request = factory.get('/',
                              {api_settings.ORDERING_PARAM: 'properties__key'})
        response = view(request)

        self.assertListEqual(
            [0, 1, 2],
            [i['properties']['key'] for i in response.data])

        # testing descending
        request = factory.get('/',
                              {api_settings.ORDERING_PARAM: '-properties__key'})
        response = view(request)

        self.assertListEqual(
            [2, 1, 0],
            [i['properties']['key'] for i in response.data])

        request = factory.get('/', {api_settings.ORDERING_PARAM: 'name'})
        response = view(request)

        # testing normal field
        self.assertListEqual(
            [0, 1, 2],
            [i['properties']['key'] for i in response.data])
