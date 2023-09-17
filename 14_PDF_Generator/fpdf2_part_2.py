from fpdf import FPDF
from fpdf.enums import XPos, YPos


class PDF(FPDF):
    def header(self):
        # Logo
        #                            x, y, width, height
        self.image("blue-jays.jpg", 10, 8, 25)
        # Font
        self.set_font("helvetica", "B", 20)
        # Padding
        self.cell(80)
        # Title
        self.cell(
            30, 10, "Title", border=True, new_x=XPos.RIGHT, new_y=YPos.NEXT, align="C"
        )
        self.ln(20)

    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # Set font
        self.set_font("helvetica", "I", 10)
        # Page number
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="c")


pdf = PDF(orientation="P", unit="mm", format="Letter")

# Set auto page break
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("times", "", 12)

for i in range(1, 41):
    pdf.cell(0, 10, f"This is line {i}", new_x=XPos.LEFT, new_y=YPos.NEXT)

# Export pdf
pdf.output("fpdf2_part_2.pdf")
