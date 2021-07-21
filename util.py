import re
import numpy as np
from PIL import Image
import scipy.misc

# default argument
CONTENT_WEIGHT = 5e0
CONTENT_WEIGHT_BLEND = 1
STYLE_WEIGHT = 5e2
TV_WEIGHT = 1e2
STYLE_LAYER_WEIGHT_EXP = 1
LEARNING_RATE = 1e1
BETA1 = 0.9
BETA2 = 0.999
EPSILON = 1e-08
STYLE_SCALE = 1.0
ITERATIONS = 1000
VGG_PATH = 'imagenet-vgg-verydeep-19.mat'
POOLING = 'max'
INITIAL_NOISEBLEED =  1.0

'''Display a single image'''
def imgfig(img_file, title, size=10):
  fig = plt.figure(figsize=(size, size))
  img = plt.imread(img_file)
  plt.axis('off')
  plt.title(title)
  plt.imshow(img)

def ishow(image, titls, size=10):
  fig = plt.figure(figsize=(size, size))
  plt.axis('off')
  plt.title(title)
  plt.imshow(image)

'''Display a list of images vertically'''
def imgshow(img_file, *img_files): 
  n = len(img_files) + 1
  fig, ax = plt.subplots(n,1,figsize=(8, 8*n))

  if n == 1:
    ax.axis('off')
    ax.set_title(img_file)
    im = plt.imread(img_file)
    ax.imshow(im)
  else:
    imgs = (img_file,) + img_files
    for i, imfile in enumerate(imgs):
      ax[i].axis('off')
      ax[i].set_title(imfile)
      im = plt.imread(imfile)
      ax[i].imshow(im)

  plt.show()


'''Display a list of images horizontally'''
def imgshow_h(img_file, *img_files): 
  n = len(img_files) + 1
  fig, ax = plt.subplots(1,n,figsize=(8, 8*n))

  if n == 1:
    ax.axis('off')
    ax.set_title(img_file)
    im = plt.imread(img_file)
    ax.imshow(im)
  else:
    imgs = (img_file,) + img_files
    for i, imfile in enumerate(imgs):
      ax[i].axis('off')
      ax[i].set_title(imfile)
      im = plt.imread(imfile)
      ax[i].imshow(im)

  plt.show()

def imread(path):
    img = scipy.misc.imread(path).astype(np.float)
    if len(img.shape) == 2:
        # grayscale
        img = np.dstack((img,img,img))
    elif img.shape[2] == 4:
        # PNG with alpha channel
        img = img[:,:,:3]
    return img


def imsave(path, img):
    img = np.clip(img, 0, 255).astype(np.uint8)
    Image.fromarray(img).save(path, quality=95)

def fmt_imsave(fmt, iteration):
    if re.match(r'^.*\{.*\}.*$', fmt):
        return fmt.format(iteration)
    elif '%' in fmt:
        return fmt % iteration
    else:
        raise ValueError("illegal format string '{}'".format(fmt))