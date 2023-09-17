from fpdf import FPDF
from fpdf.enums import XPos, YPos

title = "20,000 Leagues Under the Sea"


class PDF(FPDF):
    def header(self):
        # Font
        self.set_font("helvetica", "B", 15)
        # Center text dynamically
        title_width = self.get_string_width(title) + 6
        document_width = self.w
        self.set_x((document_width - title_width) / 2)
        # Color of frame, background, and text
        self.set_draw_color(0, 80, 180)  # Border
        self.set_fill_color(230, 230, 0)  # Background
        self.set_text_color(220, 50, 50)  # Text
        # Thickness of frame (border)
        self.set_line_width(1)
        # Title
        self.cell(
            title_width,
            10,
            title,
            border=True,
            new_x=XPos.RIGHT,
            new_y=YPos.NEXT,
            align="C",
            fill=True,
        )
        self.ln(10)

    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # Set font
        self.set_font("helvetica", "I", 8)
        # Set font color
        self.set_text_color(169, 169, 169)
        # Page number
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="c")

    def chapter_title(self, chp_number, chp_title):
        self.set_font("helvetica", "", 12)
        self.set_fill_color(200, 220, 255)
        chapter_title = f"Chapter {chp_number} : {chp_title}"
        self.cell(0, 5, chapter_title, new_x=XPos.RIGHT, new_y=YPos.NEXT, fill=True)
        self.ln()

    def chapter_body(self, filename):
        with open(filename, "rb") as fh:
            txt = fh.read().decode("latin-1")
        self.set_font("times", "", 12)
        self.multi_cell(0, 5, txt)
        self.ln()
        self.set_font("times", "I", 12)
        self.cell(0, 5, "END OF CHAPTER")

    def chapter(self, chp_number, chp_title, filename):
        self.add_page()
        self.chapter_title(chp_number, chp_title)
        self.chapter_body(filename)


pdf = PDF(orientation="P", unit="mm", format="Letter")

# Set auto page break
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.chapter(1, "A RUNAWAY REEF", "assets/chp1.txt")
pdf.chapter(2, "THE PROS AND CONS", "assets/chp2.txt")

# Export pdf
pdf.output("pdfs/fpdf2_part_3.pdf")
