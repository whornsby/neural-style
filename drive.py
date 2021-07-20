from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

ROOT_DIR_GDID = '13kelXjrToB3IpbHNj0WmRtP0yRNHcNUg'
CONTENT_DIR_GDID = '11_SKmzv0UqQhxb-rgcLYVsF5sdfUlu6A'
STYLE_DIR_GDID = '1ExIrZyGT2u4brgBIqVzQQk6-j63XP1xu'
OUTPUT_DIR_GDID = '190RRdQlpmipXHztkyK1tF_6WTeA5Ulmo'

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

'''Recursively search through Drive to find the file with a given name''' 
def get_file_from_name(name, start_id='root'):
  parents = [start_id]
  while parents:
    pid = parents.pop()
    listed = drive.ListFile({'q': f"'{pid}' in parents"}).GetList()
    for file in listed:
      if file['title'] == name:
        pass 
      # return file
      elif file['mimeType'] == 'application/vnd.google-apps.folder':
          parents.append(file['id'])

def get_file_by_id(id,name):
  file = drive.CreateFile({'id': id})
  file.GetContentFile('tmp/' + name)

def upload_image(im_file, parent_folder, title=None):
  if title is None:
    title = im_file.split('/')[-1]

  upload_file = drive.CreateFile({'title': title, 'parents': [{'id': parent_folder}]})
  upload_file.SetContentFile(im_file)
  upload_file.Upload()


def download_image(filename, parent_id):
  file_list = drive.ListFile({'q': f'{parent_id} in parents and trashed=false'})
