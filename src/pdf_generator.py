from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime

class DeliveryChallanPDFGenerator:
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin = 30
        
    def generate_challan_pdf(self, data, filename):
        c = canvas.Canvas(filename, pagesize=A4)
        self.draw_header(c, data)
        self.draw_company_info(c, data)
        self.draw_customer_info(c, data)
        self.draw_delivery_details(c, data)
        self.draw_items_table(c, data)
        self.draw_footer(c, data)
        c.save()
    
    def draw_header(self, c, data):
        logo_x = self.margin
        logo_y = self.page_height - 50
        logo_size = 40
        c.setStrokeColor(colors.black)
        c.setFillColor(colors.lightgrey)
        c.rect(logo_x, logo_y - logo_size, logo_size, logo_size, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(logo_x + logo_size/2, logo_y - logo_size/2, "LOGO")
        title_x = self.page_width / 2
        title_y = self.page_height - 40
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(title_x, title_y, "DELIVERY CHALLAN")
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.line(self.margin, self.page_height - 70, self.page_width - self.margin, self.page_height - 70)
    
    def draw_company_info(self, c, data):
        start_y = self.page_height - 100
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.margin, start_y, data['company']['name'])
        gstin_text = f"GSTIN : {data['company']['gstin']}"
        c.setFont("Helvetica", 10)
        c.drawString(self.margin, start_y - 20, gstin_text)
        c.setFont("Helvetica", 10)
        address_lines = data['company']['address'].split('\n')
        y_pos = start_y - 35
        for line in address_lines:
            c.drawString(self.margin, y_pos, line)
            y_pos -= 12
        phone_text = f"Phone : {data['company']['phone']}"
        c.drawString(self.margin, y_pos, phone_text)
    
    def draw_customer_info(self, c, data):
        start_y = self.page_height - 220
        c.setFont("Helvetica-Bold", 11)
        c.drawString(self.margin, start_y, "To,")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.margin, start_y - 20, data['customer']['name'])
        c.setFont("Helvetica", 10)
        address_lines = data['customer']['address'].split('\n') if data['customer']['address'] else []
        y_pos = start_y - 35
        for line in address_lines:
            if line.strip():
                c.drawString(self.margin, y_pos, line)
                y_pos -= 12
        right_x = self.page_width - 250
        box_width = 220
        box_height = 15
        details = [
            ("Challan No.", data['delivery']['challan_no']),
            ("Date", data['delivery']['date']),
            ("Transporter", data['delivery']['transporter']),
            ("LR No.", data['delivery']['lr_no']),
            ("Date", data['delivery']['lr_date']),
            ("Vehicle No.", data['delivery']['vehicle_no'])
        ]
        y_pos = start_y
        for i, (label, value) in enumerate(details):
            c.setStrokeColor(colors.black)
            c.setFillColor(colors.white)
            c.rect(right_x, y_pos - box_height, box_width, box_height, fill=1)
            c.setFont("Helvetica", 9)
            c.drawString(right_x + 2, y_pos - 12, f"{label}")
            c.setFont("Helvetica-Bold", 9)
            value_x = right_x + 80
            c.drawString(value_x, y_pos - 12, f"{value}")
            y_pos -= box_height
    
    def draw_delivery_details(self, c, data):
        start_y = self.page_height - 330
        c.setStrokeColor(colors.black)
        c.setFillColor(colors.white)
        c.rect(self.margin, start_y - 20, self.page_width - 2*self.margin, 20, fill=1)
        order_text = f"Please received the undermentioned goods as per YOUR Order No. {data['delivery']['order_no']} Date {data['delivery']['order_date']}"
        c.setFont("Helvetica", 10)
        c.drawString(self.margin + 5, start_y - 12, order_text)
        signature_text = "In good condition and sign, the duplicate for having received the same."
        c.drawString(self.margin + 5, start_y - 32, signature_text)
    
    def draw_items_table(self, c, data):
        start_y = self.page_height - 380
        headers = ["S.No.", "DESCRIPTION", "Qty.", "Remarks"]
        col_widths = [50, 300, 60, 120]
        c.setFillColor(colors.lightgrey)
        c.setStrokeColor(colors.black)
        c.rect(self.margin, start_y - 20, sum(col_widths), 20, fill=1)
        c.setFont("Helvetica-Bold", 10)
        x_pos = self.margin
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            c.drawCentredString(x_pos + width/2, start_y - 12, header)
            if i > 0:
                c.line(x_pos, start_y, x_pos, start_y - 20)
            x_pos += width
        c.setFillColor(colors.white)
        row_height = 25
        y_pos = start_y - 20
        for i, item in enumerate(data['items']):
            c.rect(self.margin, y_pos - row_height, sum(col_widths), row_height, fill=1)
            c.setFont("Helvetica", 10)
            x_pos = self.margin
            c.drawCentredString(x_pos + col_widths[0]/2, y_pos - 15, str(item['s_no']))
            c.line(x_pos + col_widths[0], y_pos, x_pos + col_widths[0], y_pos - row_height)
            x_pos += col_widths[0]
            c.drawString(x_pos + 5, y_pos - 15, item['description'][:40])
            c.line(x_pos + col_widths[1], y_pos, x_pos + col_widths[1], y_pos - row_height)
            x_pos += col_widths[1]
            c.drawCentredString(x_pos + col_widths[2]/2, y_pos - 15, str(item['qty']))
            c.line(x_pos + col_widths[2], y_pos, x_pos + col_widths[2], y_pos - row_height)
            x_pos += col_widths[2]
            c.drawString(x_pos + 5, y_pos - 15, item['remarks'][:20])
            c.line(self.margin, y_pos, self.margin + sum(col_widths), y_pos)
            y_pos -= row_height
        remaining_rows = max(0, min(10, int((y_pos - 200) / row_height)))
        for i in range(remaining_rows):
            c.rect(self.margin, y_pos - row_height, sum(col_widths), row_height, fill=1)
            x_pos = self.margin
            for width in col_widths[:-1]:
                x_pos += width
                c.line(x_pos, y_pos, x_pos, y_pos - row_height)
            c.line(self.margin, y_pos, self.margin + sum(col_widths), y_pos)
            y_pos -= row_height
        c.line(self.margin, y_pos, self.margin + sum(col_widths), y_pos)
        c.line(self.margin, start_y, self.margin, y_pos)
        c.line(self.margin + sum(col_widths), start_y, self.margin + sum(col_widths), y_pos)
    
    def draw_footer(self, c, data):
        footer_y = 150
        c.setFont("Helvetica", 8)
        terms_text = ("N.B. Claim for Shortage in quantity of damage is to be notified immediately on receipt of the goods "
                     "otherwise the claim will not be entertained. Every efforts will be made to execute the above order within "
                     "the time stated. Subject to Strikes, Electric failure, Rain or any other act of god over which we have no control.")
        lines = []
        words = terms_text.split()
        current_line = ""
        max_width = self.page_width - 2 * self.margin - 20
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if c.stringWidth(test_line, "Helvetica", 8) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        y_pos = footer_y
        for line in lines:
            c.drawString(self.margin, y_pos, line)
            y_pos -= 10
        signature_y = 80
        c.setFont("Helvetica", 10)
        c.drawString(self.margin, signature_y, "Receiver's Signature")
        c.line(self.margin, signature_y - 5, self.margin + 150, signature_y - 5)
        company_sig_x = self.page_width - 200
        c.drawString(company_sig_x, signature_y, f"For : {data['company']['name']}")
        c.line(company_sig_x, signature_y - 5, company_sig_x + 150, signature_y - 5)
        date_text = f"Date: {datetime.now().strftime('%d/%m/%Y')}"
        c.drawString(company_sig_x, signature_y - 25, date_text)
