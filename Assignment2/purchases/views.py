# purchases/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseHeader
from .serializers import PurchaseHeaderSerializer, PurchaseDetailSerializer, PurchaseDetail

class PurchaseHeaderView(APIView):
    # GET /purchase/
    def get(self, request):
        purchases = PurchaseHeader.objects.filter(is_deleted=False)
        serializer = PurchaseHeaderSerializer(purchases, many=True)
        return Response(serializer.data)

    # POST /purchase/
    def post(self, request):
        serializer = PurchaseHeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseHeaderDetailView(APIView):
    def get_object(self, code):
        try:
            return PurchaseHeader.objects.get(code=code, is_deleted=False)
        except PurchaseHeader.DoesNotExist:
            return None

    # GET /purchase/{code}/
    def get(self, request, code):
        purchase = self.get_object(code)
        if purchase:
            serializer = PurchaseHeaderSerializer(purchase)
            return Response(serializer.data)
        return Response({"detail": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)

    # PUT /purchase/{code}/
    def put(self, request, code):
        purchase = self.get_object(code)
        if purchase:
            serializer = PurchaseHeaderSerializer(purchase, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)

    # DELETE /purchase/{code}/
    def delete(self, request, code):
        purchase = self.get_object(code)
        if purchase:
            purchase.is_deleted = True  # Soft delete
            purchase.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)

class PurchaseDetailView(APIView):

    def get_queryset(self, header_code):
        return PurchaseDetail.objects.filter(header_code=header_code)

    def get(self, request, header_code):
        details = self.get_queryset(header_code)
        serializer = PurchaseDetailSerializer(details, many=True)
        return Response(serializer.data)

    # POST /purchase/{header_code}/details/
    def post(self, request, header_code):
        try:
            header = PurchaseHeader.objects.get(code=header_code)
        except PurchaseHeader.DoesNotExist:
            return Response({"detail": "Purchase header not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(header_code=header)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
