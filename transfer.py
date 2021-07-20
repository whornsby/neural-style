from types import ClassMethodDescriptorType
import drive

# transfer job (class?)
#   - data
#     - inputs
#     - output location
#   - params
#   - Run()
#     - execute command
#     - upload output
#     -* display

# Upload output to 
#   - output dir
#   - content img dir
#   - style img(s) dir

# input (class?)
#   - name
#   - image
#   - drive file (id)
#   - drive output folder


class ImageInput:
  # TODO: this
  def __init__(self, id):
      self.gid = id
      self.image = None
      self.name

class ImageIndex:
  def __init__(self) -> None:
    pass

def new_entry(file,path):
    id = file['id']
    filename = file['title']
    name = filename.split('.')[0]
    return (id, filename, name, path)

def build_index():
  parents = ['root']
  while parents:
    pid = parents.pop()
    listed = drive.ListFile({'q': f"'{pid}' in parents and trashed=false"}).GetList()
    for file in listed:
      if file['mimeType'] == 'application/vnd.google-apps.folder':
          parents.append(file['id'])
      else:
        im_input = new_input_from_id(file['id'], file['title'])


def new_input_from_id(id):
  drive.CreateFile({'id': id})


class TransferJob:
  def __init__(self, content_file, style_file, output_name) -> None:
    self.content = content_file
    self.style = style_file
    self.base_name = output_name
    self.param_str = ""
    self.cmd = None
    self.flags = []

  def with_flag(self, fname, val=""):
    f = f"--{fname} {val}"
    self.flags.append(f)

  def file_param(self, base, value=""):
    s = '-' if value else ''
    self.param_str += f"_({base}{s}{value})"


  def width(self, w):
    self.with_flag("width", w)

  def iterations(self, n):
    self.with_flag("iterations", n)
    self.file_param("n", n)

  def preserve_colors(self):
    self.with_flag("preserve-colors")
    self.file_param("pColor")

  def pooling(self, val):
    if val is 'max': 
      return
    self.set_flag("pooling",val)
    self.file_param("pool",val)

  def overwrite(self):
    self.with_flag("overwrite")

# TODO: content weight
# TODO: style weight
# TODO: learning rate
# TODO: style abstractness
# TODO: content abstractness
# TODO: overwrite

  def Cmd(self, output=None):
    if output is None:
      output = self.Output_name()
    script = "python neural-style/neural-style/neural_style.py"
    cmd_arr = [script] + self.flags
    return ' '.join(cmd_arr)

  def Output_name(self):
   outname = self.base_name + self.param_str + ".jpg"
   if self.outname is None:
     self.with_flag("output", outname)
   self.outname = outname
   return outname
