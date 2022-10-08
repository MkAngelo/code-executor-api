from typing import Union

from fastapi import FastAPI
import subprocess   
from os import remove

import os
import sys

from fastapi.logger import logger
from pydantic import BaseSettings
from pyngrok import ngrok

from fastapi.middleware.cors import CORSMiddleware

class Settings(BaseSettings):
    # ... The rest of our FastAPI settings

    BASE_URL = "http://localhost:3400"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"

settings = Settings()


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    settings.BASE_URL = public_url
    init_webhooks(public_url)

# ... Initialize routers and the rest of our app

@app.post(path="/")
def runner(source: str, lang: str) -> str:
    if source and lang:
        #source = source.encode("Latin-1").decode("utf-8")
        # Create a route
        name = "code." + lang
        route = "./temp/"+ name

        # Create a new file
        temp = open(route, "w")
        temp.write(source)
        temp.close()

        ans='' # Save the process

        # Execute
        if(lang == 'py'): 
            ans=subprocess.run(["python3", route], capture_output=True, text=True)
        elif(lang == 'java'): 
            ans=subprocess.run(["java", route], capture_output=True, text=True)
        elif(lang == 'c'): 
            compiler=subprocess.run(["gcc", route], capture_output=True, text=True)
            ans = subprocess.run(["./a.out"], capture_output=True, text=True)
        elif(lang == 'cpp'): 
            compiler=subprocess.run(["g++", route], capture_output=True, text=True)
            ans = subprocess.run(["./a.out"], capture_output=True, text=True)
        
        if ans.stderr:
            ans = "Upps... something was wrong"
        else:
            ans = ans.stdout
        
        context = {'ans': ans, 'text':source}  
        remove(route)
        return context
    