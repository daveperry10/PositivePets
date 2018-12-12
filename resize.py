"""
resize.py:

what it does:
  shrink the image files in the media/ directory to 400 x 400 size(px)

how to run:
  run at command line from project root directory
  "python resize.py"

"""

from PIL import Image
import os
import glob

os.chdir('media')
file_list = glob.glob('*.jpg') + glob.glob('*.png') + glob.glob('*.jpeg')

for file in file_list:
    try:
        img = Image.open(file)
        img.thumbnail((400,400))
        img.save(file, img.format)
        print("success: ", file, img.format, img.size)
    except:
        print("failure shrinking " + file)
        pass
