import fitz
import os
from utility_scripts.pdfscraper.utils import files as file_util
from pdf2image import convert_from_path

project_name = '_test_project'
input_dir = '../../input'

pdf_list = file_util.get_file_list(f'{input_dir}/{project_name}/pdf', file_extension='pdf')

image_data = 0
for pdf_name in pdf_list:
  file_source = os.path.abspath(f'{input_dir}/{project_name}/{pdf_name}')
  pdf_name = pdf_name.replace('\\', '/')
  pdf_name = pdf_name.split('/')[-1]
  print('generating images for: ---->', pdf_name)
  doc = fitz.open(file_source)
  mat = fitz.Matrix(300 / 72, 300 / 72)  # sets zoom factor for 300 dpi
  count = 0
  # Count variable is to get the number of pages in the pdf
  for p in doc:
    count += 1

  # for i in range(count):
  #   file_util.create_directory(f'{input_dir}/{project_name}/images/{pdf_name}/')
  #   val = f"{input_dir}/{project_name}/images/{pdf_name}/image_{i}.jpg"
  #   page = doc.load_page(i)
  #   pix = page.get_pixmap(matrix=mat)
  #   pix.save(val)
  # doc.close()

  ##print_for_ai_datasets
  for i in range(count):
    file_util.create_directory(f'{input_dir}/{project_name}/images/{pdf_name}/')
    val = f"../../ai/datasets/images/image2_{image_data}.jpg"
    page = doc.load_page(i)
    pix = page.get_pixmap(matrix=mat)
    pix.save(val)
    image_data += 1
  doc.close()
