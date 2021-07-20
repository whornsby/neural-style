from PIL import Image
import matplotlib.pyplot as plt
import os 




# def process_upload(img_data, content=False, style=False):
#   filename = list(img_data)[0]
#   temp_fn = filename.strip().replace(" ", "_")

#   if filename != temp_fn:
#     os.rename(filename, temp_fn)
#     filename = temp_fn
  
#   if content and style:
#     raise AttributeError("Image must be either content or style, not both")
#   if content:
#     CONTENT_IMAGE_FN = filename
#     print("Content image filename:", filename)
#     imgfig(filename, "Content image")
#   elif style:
#     STYLE_IMAGE_FN = filename
#     print("Style image filename:", filename)
#     imgfig(filename, "Style image")
#   else:
#     print("Image saved with filename:", filename)
#     imgshow(filename)