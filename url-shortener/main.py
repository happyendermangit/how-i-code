from flask import Flask,request,redirect,render_template
from lightdb import LightDB
import secrets
import urllib.parse

db = LightDB('./db.json')
app = Flask('URLshorten')

def generate_code():
    return secrets.token_urlsafe(8)


def check_url(url:str):
    if url.startswith('https://') or url.startswith('http://'):
        return True 
    else:
        return False 
    

@app.route('/')
async def home():
    return render_template("index.html")

@app.route('/api/v1/short',methods=['POST'])
async def short():
    data = request.json
    if check_url(data.get('url')):
        if data.get('custom_code'):
            if not data.get('custom_code') in db.keys():
                db.set(urllib.parse.quote(data.get('custom_code')),data.get('url'))
                return {"code":urllib.parse.quote(data.get('custom_code'))}
            else:
                return {"error":"Vanity already taken.","code":400},400
        else:
            c = generate_code()
            db.set(c,data.get('url'))
            return {"code":c}
    else:
        return {"error":"Invalid URL.","code":400},400

@app.route('/redirect/<code>')
def red(code):
    if urllib.parse.quote(code) in db.keys():
        return redirect(db.get(urllib.parse.quote(code)))
    else:
        return render_template('error.html',error="This shorten link doesn't exist!")

# Run the app if its not used as a module

if __name__ == "__main__":
    app.run(port=80,debug=True)