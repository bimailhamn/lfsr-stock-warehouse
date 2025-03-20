from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer

class ItemListCreateView(APIView):
    # GET /items/
    def get(self, request, *args, **kwargs):
        items = Item.objects.filter(is_deleted=False)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    # POST /items/
    def post(self, request, *args, **kwargs):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailView(APIView):
    def get_object(self, code):
        try:
            return Item.objects.get(code=code, is_deleted=False)
        except Item.DoesNotExist:
            return None

    # GET /items/{code}/
    def get(self, request, code, *args, **kwargs):
        item = self.get_object(code)
        if item:
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    # PUT /items/{code}/
    def put(self, request, code, *args, **kwargs):
        item = self.get_object(code)
        if item:
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    # DELETE /items/{code}/
    def delete(self, request, code, *args, **kwargs):
        item = self.get_object(code)
        if item:
            item.is_deleted = True  # Soft delete
            item.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
