from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO

from fastai import *
from fastai.text import *
from fastai.basic_train import *

import logging, sys, requests
from pathlib import Path

export_file_url_status = 'https://www.dropbox.com/s/ruml512u0dgq6i2/Fertigstellungsgrad.pkl?dl=1'
export_file_name_status = 'Fertigstellungsgrad.pkl'
export_file_url_traffic_light = 'https://www.dropbox.com/s/pnln6w67dlgdsb3/ampel.pkl?dl=1'
export_file_name_traffic_light = 'ampel.pkl'

# classes_status = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# classes_traffic_light = ['Gelb', 'Grün', 'Rot']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

def download_file(url, dest):
    if dest.exists(): return
    logging.info('Starting download: ' + url)
    response = requests.get(url)
    with open(dest, 'wb') as f:
        f.write(response.content)
    logging.info('Download successful: ' + str(dest))

def setup_learner_status():
   download_file(export_file_url_status, path/export_file_name_status)
   try:
       learn_status = load_learner(path, export_file_name_status)
       return learn_status
   except RuntimeError as e:
       if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
           print(e)
           message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
           raise RuntimeError(message)
       else:
           raise

def setup_learner_traffic_light():
   download_file(export_file_url_traffic_light, path/export_file_name_traffic_light)
   try:
       learn_traffic_light = load_learner(path, export_file_name_traffic_light)
       return learn_traffic_light
   except RuntimeError as e:
       if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
           print(e)
           message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
           raise RuntimeError(message)
       else:
           raise

learn_traffic_light = setup_learner_traffic_light()
learn_status = setup_learner_status()

@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    return HTMLResponse(html.open().read())

@app.route('/analyze', methods=['GET'])
def analyze(request):
    responses = {}
    try:
        input_text = request.query_params['text']
        logging.info('input text: ' + input_text)
        responses['computed_status'] = str(learn_status.predict(input_text)[0])
        responses['computed_trafficlight'] = str(learn_traffic_light.predict(input_text)[0])
    except KeyError:
        logging.error('KeyError')
    logging.info(responses)
    return JSONResponse(responses)

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app=app, host='0.0.0.0', port=5042)
