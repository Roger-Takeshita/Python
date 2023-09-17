from fpdf import FPDF
from fpdf.enums import XPos, YPos

title = "20,000 Leagues Under the Sea"


class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        title_width = self.get_string_width(title) + 6
        document_width = self.w
        self.set_x((document_width - title_width) / 2)
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        self.set_line_width(1)
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
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(169, 169, 169)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="c")

    def chapter_title(self, chp_number, chp_title, link):
        # Set link location
        self.set_link(link)
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

    def chapter(self, chp_number, chp_title, filename, link):
        self.add_page()
        self.chapter_title(chp_number, chp_title, link)
        self.chapter_body(filename)


pdf = PDF(orientation="P", unit="mm", format="Letter")

# Metadata
pdf.set_title(title)
pdf.set_author("Roger Takeshita")

# Config
pdf.set_auto_page_break(auto=True, margin=15)

# First page
pdf.add_page()
pdf.image("background_image.png", x=-0.5, w=pdf.w + 1)

# Variables
website_link = "http://www.gutenberg.org/cache/epub/164/pg164.txt"
ch1_link = pdf.add_link()
ch2_link = pdf.add_link()

# Attach links
pdf.cell(0, 10, "Text Source", link=website_link)
pdf.ln()
pdf.cell(0, 10, "Chapter 1", link=ch1_link)
pdf.ln()
pdf.cell(0, 10, "Chapter 2", link=ch2_link)

pdf.chapter(1, "A RUNAWAY REEF", "chp1.txt", ch1_link)
pdf.chapter(2, "THE PROS AND CONS", "chp2.txt", ch2_link)

pdf.output("fpdf2_part_4.pdf")
