from collections import defaultdict
from neural_style import ITERATIONS
import os
import math
import copy

import numpy as np
import scipy.misc

from stylize import stylize
from util import *


ITERATIONS = 1000
DEFAULTS = {
  "network": VGG_PATH,
  "initial_noiseblend": INITIAL_NOISEBLEED,
  
  "iterations": ITERATIONS,

  "content_weight": CONTENT_WEIGHT,
  "style_weight": STYLE_WEIGHT,
  "learning_rate": LEARNING_RATE,
  "tv_weight": TV_WEIGHT,
  "content_weight_blend": CONTENT_WEIGHT_BLEND,
  "style_layer_weight_exp": STYLE_LAYER_WEIGHT_EXP,
  "style_scale": STYLE_SCALE, 

  "beta1": BETA1,
  "beta2": BETA2,
  "epsilon": EPSILON,

  "pooling": POOLING,
  "preserve_colors": False,
  "verbose": False
}

SUPPORTED_FEATURES = "content, styles, width, iterations, preserve_colors, pooling, initial, overwrite, output" # width?
class TransferJob:
  def __init__(self, content_file, style_file, output_name, width=None) -> None:
    args = defaultdict(None)
    for k,v in DEFAULTS.items():
      args[k] = v
    
    content_im = imread(content_file)
    style_im = imread(style_file)
    # Resize images
    if width is not None:
      new_shape = (int(math.floor(float(content_im.shape[0]) /
              content_im.shape[1] * width)), width)
      content_im = scipy.misc.imresize(content_im, new_shape)
    target_shape = content_im.shape
    style_im = scipy.misc.imresize(style_im, target_shape[1] / style_im.shape[1])

    args['content'] = content_im
    args['styles'] = [style_im]
    args['initial'] = content_im
    
    self.args = args
    self.base_name = output_name
    self.param_str = ""
    self.outname = None

  def file_param(self, base, value=""):
    s = '-' if value else ''
    self.param_str += f"_({base}{s}{value})"

  def iterations(self, n):
    if n is not ITERATIONS:
      self.args['iterations'] = n
      self.file_param("n", n)

  def preserve_colors(self):
    self.args['preserve_colors'] = True
    self.file_param("pColor")

  def pooling(self, val):
    if val is 'max': 
      return
    self.args['pooling'] = val
    self.file_param("pool",val)

  def content_weight(self, weight_scale):
    weight = CONTENT_WEIGHT * weight_scale
    self.args['content_weight'] = weight
    self.file_param('contentWgt', weight_scale)

  def style_weight(self, weight_scale):
    weight = STYLE_WEIGHT * weight_scale
    self.args['style_weight'] = weight
    self.file_param('styleWgt', weight_scale)

  def style_abstractness(self, style_layer_weight_xp):
    self.args['style_layer_weight_xp'] = style_layer_weight_xp
    self.file_param('styleAbs', style_layer_weight_xp)


  def content_abstractness(self, content_weight_blend):
    self.args['content_weight_blend'] = content_weight_blend
    self.file_param('contentAbs', content_weight_blend)

  def overwrite(self):
    self.args['overwrite'] = True

  def verbose(self):
    self.args['verbose'] = True

# TODO: content weight
# TODO: style weight
# TODO: learning rate
# TODO: style abstractness
# TODO: content abstractness
# TODO: overwrite

  def Execute(self):
    print("Executing style transfer job for", self.base_name)
    self.output = self.Output_name()

    for iteration, image, loss_vals in stylize(
      content=self.args['content'],
      styles=self.args['styles'],
      initial=self.args['initial'],
      iterations=self.args['iterations'],
      preserve_colors=self.args['preserve_colors'],
      pooling=self.args['pooling']
    ):
      pass
    if image is not None:
      imsave(self.output, image)

  def Output_name(self):
   outname = self.base_name + self.param_str + ".jpg"
   return outname



def prepare_inputs(args):
  if not os.path.isfile(args.network):
        raise IOError("Network %s does not exist. (Did you forget to "
                     "download it?)" % args.network)
  if os.path.isfile(args.output) and not args.overwrite:
      raise IOError("%s already exists, will not replace it without "
                    "the '--overwrite' flag" % args.output)
  try:
      imsave(args.output, np.zeros((500, 500, 3)))
  except:
      raise IOError('%s is not writable or does not have a valid file '
                    'extension for an image file' % args.output)


