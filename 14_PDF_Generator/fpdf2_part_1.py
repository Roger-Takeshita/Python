from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Create FPDF object
#    Layout ('P', 'L') - portrait vs landscape
#    Unit ('mm', 'cm', 'in')
#    Format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))
pdf = FPDF("P", "mm", "Letter")

# Add a page
pdf.add_page()

# Font
#   Fonts ('times', 'courier', 'helvetica', 'symbol', 'zpfdingbats')
#   'B' (bold), 'U' (underline), 'I' (italic), '' (regular), combination ('BU')
pdf.set_font("helvetica", "", 16)  # font-family, normal, font-size

# Add text
#   w = width
#   h = height
#   text
#   new_y=YPos.NEXT = new line
#   new_x=XPos.LEFT = alignment
#   border=True
pdf.cell(120, 120, "Hello World", new_x=XPos.LEFT, new_y=YPos.NEXT, border=True)
pdf.set_font("times", "", 12)
pdf.cell(80, 10, "Good By World")

# Export pdf
pdf.output("pdfs/fpdf2_part_1.pdf")
