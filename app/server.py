from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from fastai.basic_train import load_learner

import logging, sys, requests
from pathlib import Path

import config

def setup_application():
  app = Starlette()
  app.add_middleware(CORSMiddleware,
                     allow_origins = ['*'],
                     allow_headers = ['X-Requested-With', 'Content-Type'])
  app.mount('/static', StaticFiles(directory = 'app/static'))
  return app

def download_file(url, dest):
  if dest.exists():
    return
  logging.info('Starting download: ' + url)
  response = requests.get(url)
  with open(dest, 'wb') as open_file:
    open_file.write(response.content)
  logging.info('Download successful: ' + str(dest))

def setup_learner(url, file_name):
  download_file(url, path/file_name)
  try:
    learner = load_learner(path, file_name)
    return learner
  except RuntimeError:
    logging.exception('Error setting up learner')

path = Path(__file__).parent

app = setup_application()

learner_traffic_light = setup_learner(config.url_traffic_light,
                                      config.file_name_traffic_light)
learner_status = setup_learner(config.url_status,
                               config.file_name_status)

@app.route('/')
def index(request):
  html = path/'view'/'index.html'
  return HTMLResponse(html.open().read())

@app.route('/analyze', methods=['GET'])
def analyze(request):
  responses = {}
  try:
    input_text = request.query_params['text']
    logging.info('Input text: ' + input_text)
    status = learner_status.predict(input_text)[0]
    responses['status'] = str(status)
    trafficlight = learner_traffic_light.predict(input_text)[0]
    responses['trafficlight'] = str(trafficlight)
  except KeyError:
    logging.error('KeyError')
  logging.info('Response: ' + str(responses))
  return JSONResponse(responses)

if __name__ == '__main__':
  if 'serve' in sys.argv:
    uvicorn.run(app=app, host='0.0.0.0', port=5042)
