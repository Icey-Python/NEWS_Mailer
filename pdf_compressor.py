import PyPDF2
import os


def compress_pdf(input_pdf, output_pdf):
  # Open the PDF files
  file_size_bytes = os.path.getsize(input_pdf)
  # Convert to megabytes (MB)
  file_size_mb = file_size_bytes / 1024 / 1024
  print("before", file_size_mb)
  import subprocess

  # Specify the input and output PDF file paths

  # Run Ghostscript to compress the PDF
  subprocess.run([
      "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
      "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dBATCH",
      f"-sOutputFile={output_pdf}", input_pdf
  ])

  file_size_bytes = os.path.getsize(output_pdf)
  # Convert to megabytes (MB)
  file_size_mb = file_size_bytes / 1024 / 1024
  print("after", file_size_mb)


# Specify the input and output PDF file names
input_pdf = "multi_column_with_long_paragraphs.pdf"
output_pdf = "multi_column_with_long_paragraphs.pdf"


