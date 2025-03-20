import copy

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(report_data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Judul Laporan
    title = Paragraph("Stock Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))  # Tambahkan spasi

    # Informasi Item
    item_info = [
        ["Item Code", report_data["item_code"]],
        ["Name", report_data["item_name"]],
        ["Unit", report_data["unit"]],
    ]
    item_table = Table(item_info, colWidths=[100, 300])
    item_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    elements.append(item_table)
    elements.append(Spacer(1, 12))

    # Data Tabel
    table_data = [
        ["No", "Date", "Description", "Code", "In (Qty)", "In (Price)", "Out (Qty)", "Out \n(Price)", "Stock", "Total"],
    ]
    counter = 1
    span = []
    p_total_purchase = 0
    q_total_purchase = 0
    for transaction in report_data["purchases"]:
        table_data.append([
            counter,
            transaction["date"],
            report_data["item_name"],
            transaction["code"],
            transaction["qty"],
            transaction["price"],
            0,
            0,
            transaction["qty"],
            transaction["total"]
        ])
        counter += 1
        p_total_purchase += transaction["total"]
        q_total_purchase += transaction['qty']
    table_data.append(["balance", "", "", "","","","","", q_total_purchase, p_total_purchase])
    span.append(counter)
    p_total_sell = 0
    q_total_sell = 0
    for transaction in report_data["sells"]:
        table_data.append([
            counter,
            transaction["date"],
            report_data["item_name"],
            transaction["code"],
            0,
            0,
            transaction["qty"],
            transaction["price"],
            transaction["qty"],
            transaction["total"]
        ])
        counter += 1
        p_total_sell += transaction["total"]
        q_total_sell += transaction['qty']
    table_data.append(["balance", "", "", "","","","","", q_total_sell, p_total_sell])
    span.append(counter)
    # Tambahkan Gaya Tabel
    style = [
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]
    injected = 0
    second_counter = copy.copy(counter)
    for i in span:
        style.append(('SPAN', (0,i+injected), (3,i+injected)))
        style.append(('SPAN', (4, i + injected), (7, i + injected)))
        injected += 1
        second_counter += 1
    print(report_data)
    if counter != second_counter:
        table_data.append(["summary", "", "", "", q_total_purchase, "", q_total_sell, "", report_data['initial_stock'], report_data['initial_balance']])
        style.append(('SPAN', (0, second_counter), (3, second_counter)))
        style.append(('SPAN', (4, second_counter), (5, second_counter)))
        style.append(('SPAN', (6, second_counter), (7, second_counter)))
    table = Table(table_data, colWidths=[30, 70, 100, 50, 50, 70, 50, 50, 50, 70], rowHeights=[40 for i in range(len(table_data))])
    table.setStyle(TableStyle(style))
    elements.append(table)

    # Build PDF
    doc.build(elements)
