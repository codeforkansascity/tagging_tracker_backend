from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Address
from backend.serializers import AddressSerializer


class AddressView(APIView):

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        address = self.get_object(pk)
        return Response(AddressSerializer(address).data)

    def delete(self, request, pk):
        print("HERE")
        address = self.get_object(pk)
        address.delete()
        return Response()
