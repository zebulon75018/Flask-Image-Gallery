
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
import os
import glob
import sys
import binascii
import argparse

NB_IMAGES_PER_REQUEST = 5000

app = Flask("Flask Image Gallery")
app.config['IMAGE_EXTS'] = [".png", ".jpg", ".jpeg", ".gif", ".tiff"]

parser = argparse.ArgumentParser('Usage: %prog [options]')
parser.add_argument('root_dir', help='Gallery root directory path')
parser.add_argument('-l', '--listen', dest='host', default='127.0.0.1', \
                                    help='address to listen on [127.0.0.1]')
parser.add_argument('-p', '--port', metavar='PORT', dest='port', type=int, \
                                default=5000, help='port to listen on [5000]')
args = parser.parse_args()
app.config['ROOT_DIR'] = args.root_dir


def encode(x):
    return binascii.hexlify(x.encode('utf-8')).decode()

def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()

image_paths = []
for root,dirs,files in os.walk(app.config['ROOT_DIR']):
     for file in files:
        if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
             image_paths.append(encode(os.path.join(root,file)))
 
@app.route('/')
def home():
    if request.args.get('step') is None:
         step = 0
    else: 
         step = int(request.args.get('step'))
    print(image_paths[step*NB_IMAGES_PER_REQUEST:NB_IMAGES_PER_REQUEST])
    return render_template('index.html', paths=image_paths[step*NB_IMAGES_PER_REQUEST:NB_IMAGES_PER_REQUEST*(step+1)], ntotal=len(image_paths),step=step)


@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir,filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)


if __name__=="__main__":
        app.run(host=args.host, port=args.port, debug=True)
