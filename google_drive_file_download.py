'''
Guide for usage:
In your terminal, run the command:

Reguired commands to Install:
python3.6 -m pip install requests 
python3.6 -m pip install tqdm

python3.6 google_drive_file_download.py --googleFID=Google_File_ID --destination_path=/home/download/file.type

Setps to Get Google file ID & URL:

1. Go to google drive and select file 
2. Right click on the file and get url once given  the permission.
3. link is in encode format we need to  decode with below reference  link
4. reference link: https://sites.google.com/site/gdocs2direct/
5. "https://drive.google.com/uc?export=download" and google file ID.

author: Naga Manoj Kumar Chittipalla
'''

import requests

from tqdm import tqdm

class download_google_drive_file():
    def __init__(self,google_id, destination):
        self.id = google_id
        self.destination = destination
        self.URL = "https://drive.google.com/uc?export=download"

    def copy_to_destination(self, response, destination):
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
             with tqdm(unit='B', unit_scale=True, unit_divisor=1024) as bar:
                 for chunk in response.iter_content(CHUNK_SIZE):
                     if chunk:
                         f.write(chunk)
                         bar.update(CHUNK_SIZE)   
    def run(self):
        session = requests.Session()
        response = session.get(self.URL, params = { 'id' : self.id }, stream = True)
        if "404" in str(response):
            print(" Please provide valid google file ID.")
            exit()
        self.copy_to_destination(response, self.destination)
         

if __name__ == "__main__":
    import sys, os
    import argparse
    parser = argparse.ArgumentParser(description='Download The Files From Google Drive.')
    required = parser.add_argument_group('required arguments')
    required.add_argument('--googleFID',
                          help='<google file id from the URL>',
                          required=True,
                          metavar='1sMWXoi4l4bhwoLYXlKlgCCNvT0QrkzLm1')
    required.add_argument('--destination_path',
                           help='<provide destination path along with file type>',
                           metavar='/home/download/file.type')
    args = parser.parse_args()
    file_name = args.destination_path.split("/")[-1]
    if not os.path.isdir(args.destination_path.replace(file_name,"")) or "."  not in file_name:
        print('provide destination path along with file type.')
        exit()
    obj=download_google_drive_file(args.googleFID, args.destination_path)
    obj.run()
