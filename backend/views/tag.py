import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Tag
from backend.serializers import TagSerializer

logger = logging.getLogger(__name__)


class TagView(APIView):

    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def put(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        serializer = TagSerializer(tag, request.data)
        if serializer.is_valid():
            tag = serializer.save()
            logger.debug(f"{tag.id} updated")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        data = {
            "id": tag.id,
            "address": tag.address.id
        }
        tag.delete()
        logger.debug(f"tag id: {data['id']} related to {data['address']} deleted")
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagListView(APIView):

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            logger.debug(f"{tag.id} created by {tag.creator_user_id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
