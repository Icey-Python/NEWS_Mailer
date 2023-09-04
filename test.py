import json
import requests
from fpdf import FPDF
from datetime import datetime
import re
from PIL import Image
import math


# PDF config
class NewsPDF(FPDF):

  def header(self):
    self.set_text_color(150, 150, 150)
    self.set_font('Arial', 'B', 12)
    self.cell(
        0,
        10,
        f"Daily News Articles - {datetime.now().strftime('%A, %B %d, %Y')}",
        align='R',
        ln=1)

  def footer(self):
    self.set_text_color(150, 150, 150)
    self.set_xy(-15, -15)
    self.set_font('Arial', 'I', 12)
    self.cell(0, 10, f'{self.page_no()}', align='C')


pdf = NewsPDF()
pdf.set_margins(10, 10)
pdf.add_page()
img_width = pdf.w / 1.6

# Load news data
try:
  with open('scrapped_news.json', encoding='utf-8') as f:
    news_data = json.load(f)
  for data in news_data:
    content = []
    # Pattern to match unknown chars
    pattern = re.compile(r'[^\x00-\x7F]+')
    # Replace unknown chars with ''
    data['title'] = pattern.sub('', data['title'])
    data['summary'] = pattern.sub('', data['summary'])
    data['content'] = pattern.sub('', data['content'])
    #parsing content into smaller chunks to subdivide into columns
    if len(data['content']) > 1000:
      size = len(data['content']) // 1000
      for i in range(size):
        start = i * 1000
        end = (i + 1) * 1000
        w_str = (data['content'])[start:end]
        content.append(w_str)
    else:
      w_str = data['content']
      content.append(w_str)
      
    data['content'] = content
    
except FileNotFoundError:
  print("The 'news.json' file is not found.")
  exit(1)
except json.JSONDecodeError:
  print("Failed to parse 'news.json'. Check its format.")
  exit(1)


def go_to_next_column(prev_coord, cell_txt):
  pdf.set_xy(pdf.x + 100, prev_coord)
  pdf.multi_cell(90, 5, cell_txt, align='J')


# Define cell padding
cell_padding = 5
for item in news_data[0:10]:
  image_path = None
  # Download image
  image_url = item['image']
  w = h = pdf.get_y() + 10
  if image_url == 'https:':
    image_path = None
  else:
    try:
      response = requests.get(image_url)
      if response.status_code == 200:
        image_path = 'image.jpg'
        with open(image_path, 'wb') as f:
          f.write(response.content)
          im = Image.open(image_path)
          w, h = im.size
      else:
        image_path = None
    except requests.exceptions.RequestException as e:
      print(f"Failed to download image: {e}")
      image_path = None

  # get items
  title = item['title']
  summary = item['summary']
  content = item['content']
  
  # Add title
  pdf.set_font('Times', 'B', 20)
  pdf.multi_cell(0, 10, txt=title.upper(), align='L')

  # Add image
  if image_path:
    pdf.image(image_path,
              x=pdf.get_x(),
              y=pdf.get_y() + cell_padding,
              w=img_width)

  # Add summary
  pdf.set_font('Arial', 'I', 12)
  pdf.set_text_color(100, 100, 100)
  pdf.set_x(img_width + 20)
  pdf.multi_cell(0, 10, txt=(summary[11:]).strip(), align='L')

  #add content
  pdf.set_y(((h/w)*img_width)+20)
  pdf.set_text_color(50, 50, 50)
  for no, text in enumerate(content):
    coord = 0
    if no % 2 == 0:
      print(2,pdf.get_y() - coord)
      go_to_next_column(pdf.get_y() - coord, text)
      pdf.ln(10)
    else:
      coord = pdf.get_y()
      pdf.set_x(0)
      pdf.multi_cell(90, 5, text, align='J')
      coord = pdf.get_y()
  # Add spacing
  pdf.ln(10)

# Output PDF
pdf.output('news.pdf')
