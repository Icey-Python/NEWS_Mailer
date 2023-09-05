import sys
from PDFNetPython3 import PDFDoc, Optimizer

def compress_pdf(input_pdf, output_pdf):
    try:
        PDFDoc.Initialize()
        
        # Open the input PDF
        pdf_doc = PDFDoc(input_pdf)
        
        # Create a PDF optimizer
        optimizer = Optimizer()
        
        # Set optimization options (e.g., image quality, DPI, etc.)
        optimizer.SetColorImageSettings(Optimizer.e_jpeg, 10)  # Adjust image quality (0-100)
        optimizer.SetImageDPI(150)  # Set image DPI
        
        # Optimize the PDF
        optimizer.Optimize(pdf_doc)
        
        # Save the compressed PDF to the output file
        pdf_doc.Save(output_pdf, SDFDoc.e_linearized)
        
        print(f"Compression complete. Compressed PDF saved as {output_pdf}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    
  # Specify the input and output PDF file names
  input_pdf = "multi_column_with_long_paragraphs.pdf"
  output_pdf = "multi_column_with_long_paragraphs.pdf"

    compress_pdf(input_pdf, output_pdf)





