from typing import Union

from fastapi import FastAPI
import subprocess   
from os import remove

app = FastAPI()

@app.post(path="/")
def runner(source: str, lang: str) -> str:
    if source and lang:

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
    