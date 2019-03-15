from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO

from fastai import *
from fastai.vision import *

# export_file_url = 'https://www.dropbox.com/s/v6cuuvddq73d1e0/export.pkl?raw=1'
export_file_url_PC = 'https://www.dropbox.com/s/ruml512u0dgq6i2/Fertigstellungsgrad.pkl?dl=1'
export_file_name_PC = 'Fertigstellungsgrad.pkl'
export_file_url_Ampel = 'https://www.dropbox.com/s/pnln6w67dlgdsb3/Ampel.pkl?dl=1'
export_file_name = 'Ampel.pkl'

classes = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
classes_Ampel = ['Gelb', 'Grün', 'Rot']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner_PC():
    await download_file(export_file_url_PC, path/export_file_name_PC)
    try:
        learn_PC = load_learner(path, export_file_name_PC)
        return learn_PC
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise
async def setup_learner_Ampel():
    await download_file(export_file_url_Ampel, path/export_file_name_Ampel)
    try:
        learn_Ampel = load_learner(path, export_file_name_Ampel)
        return learn_Ampel
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    return HTMLResponse(html.open().read())

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    data = await request.form()
    title = await (data['title'].read())
    statustext = await (data['statustext'].read())
    text = titel + ' ' + statustext
    prediction_Ampel = learn_Ampel.predict(text)
    prediction_PC = learn_PC.predict(text)
    return JSONResponse({'result_Ampel': str(prediction_Ampel)}, {'result_PC': str(prediction_PC)})

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app=app, host='0.0.0.0', port=5042)
