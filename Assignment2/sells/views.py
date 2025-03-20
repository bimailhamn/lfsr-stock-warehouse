from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SellHeader, SellDetail
from .serializers import SellHeaderSerializer, SellDetailSerializer

class SellHeaderView(APIView):
    # GET /sell/
    def get(self, request):
        sells = SellHeader.objects.filter(is_deleted=False)
        serializer = SellHeaderSerializer(sells, many=True)
        return Response(serializer.data)

    # POST /sell/
    def post(self, request):
        serializer = SellHeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SellHeaderDetailView(APIView):
    def get_object(self, code):
        try:
            return SellHeader.objects.get(code=code, is_deleted=False)
        except SellHeader.DoesNotExist:
            return None

    # GET /sell/{code}/
    def get(self, request, code):
        sell = self.get_object(code)
        if sell:
            serializer = SellHeaderSerializer(sell)
            return Response(serializer.data)
        return Response({"detail": "Sell not found"}, status=status.HTTP_404_NOT_FOUND)

    # PUT /sell/{code}/
    def put(self, request, code):
        sell = self.get_object(code)
        if sell:
            serializer = SellHeaderSerializer(sell, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Sell not found"}, status=status.HTTP_404_NOT_FOUND)

    # DELETE /sell/{code}/
    def delete(self, request, code):
        sell = self.get_object(code)
        if sell:
            sell.is_deleted = True  # Soft delete
            sell.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Sell not found"}, status=status.HTTP_404_NOT_FOUND)


class SellDetailView(APIView):
    def get_queryset(self, header_code):
        return SellDetail.objects.filter(header__code=header_code)

    # GET /sell/{header_code}/details/
    def get(self, request, header_code):
        details = self.get_queryset(header_code)
        serializer = SellDetailSerializer(details, many=True)
        return Response(serializer.data)

    # POST /sell/{header_code}/details/
    def post(self, request, header_code):
        try:
            header = SellHeader.objects.get(code=header_code)
        except SellHeader.DoesNotExist:
            return Response({"detail": "Sell header not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SellDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(header_code=header)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)