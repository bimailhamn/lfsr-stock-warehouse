from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from items.models import Item
from purchases.models import PurchaseDetail
from sells.models import SellDetail
from datetime import datetime
import os
from django.conf import settings
from django.http import FileResponse
from .pdf_utils import generate_pdf


class ReportView(APIView):
    def get(self, request, item_code):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Konversi string tanggal ke objek datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Ambil item berdasarkan item_code
        item = get_object_or_404(Item, code=item_code)
        # Ambil data pembelian dan penjualan dalam rentang tanggal
        purchases = PurchaseDetail.objects.filter(
            item_code=item,
            header_code__date__range=(start_date, end_date)
        )
        sells = SellDetail.objects.filter(
            item_code=item,
            header_code__date__range=(start_date, end_date)
        )
        # Format data untuk laporan
        report_data = {
            "item_code": item.code,
            "item_name": item.name,
            "unit": item.unit,
            "description": item.description,
            "start_date": start_date,
            "end_date": end_date,
            "purchases": [],
            "sells": [],
            "initial_stock": item.stock,
            "initial_balance": item.balance,
        }

        for purchase in purchases:
            report_data["purchases"].append({
                "date": purchase.header_code.date,
                "code": purchase.header_code,
                "qty": purchase.quantity,
                "price": purchase.unit_price,
                "total": purchase.quantity * purchase.unit_price,
            })

        for sell in sells:
            report_data["sells"].append({
                "date": sell.header_code.date,
                "code": sell.header_code,
                "qty": sell.quantity,
                "price": sell.unit_price,
                "total": sell.quantity * sell.unit_price,
            })

        # Generate PDF
        pdf_filename = f"report_{item_code}_{start_date}_{end_date}.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
        generate_pdf(report_data, pdf_path)

        # Return PDF sebagai response
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')