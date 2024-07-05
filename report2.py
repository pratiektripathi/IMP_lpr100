import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch


def create_report(cdata):
    # Group the data by
    today = datetime.datetime.today()
    xdate = today.strftime("%d-%m-%y")
    sno = 1
    party_data = {}
    for row in cdata:
        party = row[4]
        variety = row[5]
        if party not in party_data:
            party_data[party] = {}
        if variety not in party_data[party]:
            party_data[party][variety] = {'total_gross_wt': 0, 'total_tare_wt': 0, 'total_core_wt': 0, 'total_net_wt': 0, 'data': []}
            sno=1

        gross_wt, tare_wt, core_wt, net_wt = float(row[6]), float(row[7]), float(row[8]), float(row[9])
        party_data[party][variety]['total_gross_wt'] += gross_wt
        party_data[party][variety]['total_tare_wt'] += tare_wt
        party_data[party][variety]['total_core_wt'] += core_wt
        party_data[party][variety]['total_net_wt'] += net_wt

        del row[10:]
        del row[1:3]
        del row[2:4]
        
        

        row[0] = sno
        sno += 1
        party_data[party][variety]['data'].append(row)

    # Define the style sheet
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_table_header = styles["Heading3"]
    style_table_data = styles["Normal"]

    # Define the document
    doc = SimpleDocTemplate("packing_list.pdf", pagesize=A4)

    # Define the story
    story = []

    # Add the title
    story.append(Paragraph("ADITYA FLEXIPACK PVT LTD", style_title))
    story.append(Paragraph(xdate, style_table_data))

    # Loop over each party and create a separate table
    for party, party_data in party_data.items():
        # Add the party header
        party_header = Paragraph("Party : " + party, style_table_header)
        story.append(party_header)

        for variety, variety_data in party_data.items():
            # Add the variety header
            variety_header = Paragraph("Job Name : " + variety, style_table_header)
            story.append(variety_header)

            # Add the table
            head = [["SNo.", "Roll No.", "Gross Wt.", "Tare Wt.", "Core Wt.", "Net Wt."]]
            table_data = head + variety_data['data']

            # Add the total row for this party and variety
            total_row = ['', 'Total', round(variety_data['total_gross_wt'], 2), round(variety_data['total_tare_wt'], 2),
                         round(variety_data['total_core_wt'], 2), round(variety_data['total_net_wt'], 2)]
            table_data.append(total_row)

            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            story.append(table)

    # Build the document
    doc.build(story, onFirstPage=lambda canvas, doc: canvas.drawString(inch, 10 * inch, ""),
               onLaterPages=lambda canvas, doc: canvas.drawString(inch, 10 * inch, ""))
