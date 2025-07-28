# app.py
from flask import Flask, request, render_template, redirect, url_for
import os
import xml.etree.ElementTree as ET
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'xml'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    fundo = root.find('.//FundoInvestimento')
    carteira = root.find('.//ComposicaoCarteira')

    nome_fundo = fundo.findtext('Nome', default='Não encontrado')
    cnpj = fundo.findtext('CNPJ', default='Não encontrado')
    data = carteira.findtext('DataFim', default='Não encontrada')
    pl = carteira.findtext('PL', default='Não encontrado')
    cotas = carteira.findtext('QtdeCotas', default='Não encontrado')

    rent_mes = carteira.findtext('RentabMes', default='Não encontrada')
    rent_ano = carteira.findtext('RentabAno', default='Não encontrada')
    rent_12m = carteira.findtext('Rentab12Meses', default='Não encontrada')

    ativos = []
    for ativo in carteira.findall('.//ItemCarteira'):  # Lista de ativos
        nome = ativo.findtext('NomeAtivo', default='-')
        tipo = ativo.findtext('TipoAtivo', default='-')
        qtd = ativo.findtext('QuantidadeAtivo', default='0')
        val = ativo.findtext('ValorMercado', default='0')
        perc = ativo.findtext('PercPL', default='0')
        ativos.append((nome, tipo, qtd, val, perc))

    return {
        'nome_fundo': nome_fundo,
        'cnpj': cnpj,
        'data': data,
        'pl': pl,
        'cotas': cotas,
        'rent_mes': rent_mes,
        'rent_ano': rent_ano,
        'rent_12m': rent_12m,
        'ativos': ativos
    }

@app.route('/')
def index():
    return render_template('index.html', Ano=datetime.now().year)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    dados = parse_xml(filepath)
    return render_template('resultado.html', dados=dados)

if __name__ == '__main__':
    app.run(debug=True)
