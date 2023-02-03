from flask import Flask, redirect, render_template, request, session,url_for
import qrcode
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)

app.secret_key = 'secret_key'

@app.route('/')
def index():
    
    link = session.get('link', '')
    session.pop('link', None)
    base64_img = session.get('base64_img', '')
    session.pop('base64_img', None)
    return render_template('index.html', link=link, base64_img = base64_img)

@app.route('/', methods=['POST'])
def generator():
    memory = BytesIO()
    link = request.form.get('qr_link')
    session['link'] = link

    img = qrcode.make(link)
    img.save(memory)
    memory.seek(0)
    base64_img = "data:image/png;base64," + \
        b64encode(memory.getvalue()).decode('ascii')
    session['base64_img'] = base64_img
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)