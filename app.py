from flask import Flask, request, render_template
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and file.filename.endswith('.xml'):
        tree = ET.parse(file)
        root = tree.getroot()
        nome_fundo = root.findtext('.//NmFundo')
        cnpj = root.findtext('.//CNPJ')
        pl = root.findtext('.//VLPatrimLiq')

        return render_template('resultado.html', nome_fundo=nome_fundo, cnpj=cnpj, pl=pl)
    return 'Arquivo inválido'

if __name__ == '__main__':
    app.run(debug=True)