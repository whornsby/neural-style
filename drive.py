from collections import defaultdict, namedtuple

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

import matplotlib.pyplot as plt
from util import *

ROOT_DIR_GDID = '13kelXjrToB3IpbHNj0WmRtP0yRNHcNUg'
CONTENT_DIR_GDID = '11_SKmzv0UqQhxb-rgcLYVsF5sdfUlu6A'
STYLE_DIR_GDID = '1ExIrZyGT2u4brgBIqVzQQk6-j63XP1xu'
OUTPUT_DIR_GDID = '190RRdQlpmipXHztkyK1tF_6WTeA5Ulmo'

IGNORED_TYPES = ["application/octet-stream"]
FOLDER_TYPE = "application/vnd.google-apps.folder"
IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif"]

tree = lambda: defaultdict(tree)
fdata = namedtuple("fdata","title id mimeType")

class Drive:
  def __init__(self) -> None:
    auth.authenticate_user()
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials.get_application_default()
    self.drive = GoogleDrive(gauth)
    self.image_index = defaultdict(lambda:None)
    self.dir_index = defaultdict(list)
    self.local_files = defaultdict(lambda:None)
    # self.path_tree = tree()

  def Create_index(self):
    queue = [CONTENT_DIR_GDID, STYLE_DIR_GDID]
    while queue:
      dir_id = queue.pop()
      listed = self.drive.ListFile({'q': f"'{dir_id}' in parents"}).GetList()
      for file in listed:
        title, mimeType, id = file['title'], file['mimeType'], file['id']
        if mimeType in IGNORED_TYPES:
          continue
        elif mimeType == FOLDER_TYPE:
          queue.append(id)
        elif mimeType in IMAGE_TYPES:
          im_name = title.split('.')[0]
          self.image_index[im_name] = fdata(title, id, mimeType)
        else:
          print("Unrecognized:", title, mimeType)
        # print(file['title'],file['mimeType'],file['id'])
    
    output_dirs = [(OUTPUT_DIR_GDID,"")]
    while output_dirs:
      dir_id, path = output_dirs.pop()
      listed = self.drive.ListFile({'q': f"'{dir_id}' in parents"}).GetList()
      for file in listed:
        title, mimeType, id = file['title'], file['mimeType'], file['id']
        if mimeType in IGNORED_TYPES:
          continue
        elif mimeType == FOLDER_TYPE:
          path += f"{title}/"
          self.dir_index[path] = id
          output_dirs.append((id,path))

  def List(self):
    for im in sorted(self.image_index):
      print(im)

  def contains(self, img_name):
    return self.image_index[img_name] is not None

  def img_data(self, img_name): 
    return self.image_index[img_name]

  def Retrieve(self, img_name):
    local_path = self.local_files[img_name]
    if local_path is None:
      img_data = self.image_index[img_name]
      if img_data is not None:
        img_file = self.drive.CreateFile({'id': img_data.id})
        img_file.GetContentFile(img_data.title, img_data.mimeType)
        local_path = img_data.title
        self.local_files[img_name] = local_path 
    
    return local_path

  # def Store_image(self, image_file, paths=["common/"], create=True):
  #   parents = []
  #   # Get parent ids for each of the paths passed in
  #   for path in paths:
  #     parent_id = self.dir_index[path]
  #     if parent_id is None:
  #       if create:
  #         path_dirs = path.split('/')
  #         path, dir = path_dirs[:-1], path_dirs[-1]
  #         parent_id = self.create_dir(path, dir) # TODO: implement create_dir
  #       else: 
  #         raise AttributeError(f"Path {path} does not exist and the create flag is {create}")
  #     parents.append[parent_id]
    
  #   upload_file = self.drive.CreateFile({'title': image_file,'parents': [{'id': pid} for pid in parents]})
  #   upload_file.SetContentFile(image_file)
  #   upload_file.Upload() 