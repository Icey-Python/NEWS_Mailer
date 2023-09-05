from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, PageTemplate, NextPageTemplate,Image,Spacer,PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import requests

# Create a PDF document
def compile_news():
  doc = SimpleDocTemplate("multi_column_with_long_paragraphs.pdf", pagesize=letter)
  
  
  
  # Define a two-column page template
  page_template = PageTemplate(
      id="two_column",
      frames=[
          Frame(36, 36, 250, 750, id="left_frame"),
          Frame(336, 36, 250, 750, id="right_frame"),
      ],
  )
  
  
  
  large_style = ParagraphStyle(name='Large', fontSize=14) 
  summary_style = ParagraphStyle(name="gray",textColor = "#808080")
  # Add the page template to the document
  doc.addPageTemplates(page_template)
  
  # Define styles for text
  styles = getSampleStyleSheet()
  style = styles["Normal"]
  
  # Content for first page 
  first_page_content = []
  first_page_content.append(Paragraph("Title", styles["Heading1"]))
  first_page_content.append(Paragraph("Subtitle", styles["Heading2"]))
  
  
  
  style.textColor = colors.black
  style.leading = 12  # Adjust line spacing as needed
  
  # Create a list of longer paragraphs
  with open("scrapped_news.json","r") as file:
    import json
    data = json.load(file)
  
  #banner template
  banner_info=[]
  # Create a story for the content
  story = []
  
  for no,paragraph in enumerate(data[0:30]):
      if paragraph['image'] == "https:":
        pass
      else:
        response = requests.get(paragraph['image'])
        print(response.status_code)
        image_data = response.content
        photo_curr =f"images/photo_{no}.jpg"
        with open(photo_curr,"wb") as photo:
          photo.write(image_data)
        #Add image to PDF
        import PIL 
        im= PIL.Image.open(photo_curr,"r")
        w,h =im.size
        image = Image(photo_curr,width = 200,height = ((h/w)*200)) 
        print("height",(h/w)*200)
        
      title = Paragraph(f"<br/><b>{paragraph['title']}</b><br/><br/>",large_style)
      summary = Paragraph(f"<em><i>{paragraph['summary']}</i></em><br/><br/>", summary_style)
      p = Paragraph(paragraph['content'], style)
      story.append(title)
      try:
        story.append(image)
      except LayoutError(ident):
        continue
      story.append(summary)
      story.append(p)
      story.append(NextPageTemplate('two_column'))
  
  # Build the PDF with the content
  doc.build(story)

compile_news()