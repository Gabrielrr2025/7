from flask import Flask, render_template, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['xml_file']
    tree = ET.parse(file)
    root = tree.getroot()

    try:
        nome_fundo = root.findtext('.//NomeFundo')
        cota = root.findtext('.//GrupoCota/Cota')
        pl = root.findtext('.//GrupoCota/PL')
        data_cota = root.findtext('.//GrupoCota/DataCota')

        ativos = []
        for ativo in root.findall('.//GrupoCarteira/GrupoCarteiras/GrupoCarteira'):
            nome = ativo.findtext('Ativo')
            tipo = ativo.findtext('TipoAtivo')
            quantidade = ativo.findtext('Quantidade')
            valor_mercado = ativo.findtext('ValorMercado')
            percentual_pl = ativo.findtext('PercentualPL')

            ativos.append({
                'nome': nome,
                'tipo': tipo,
                'quantidade': quantidade,
                'valor_mercado': valor_mercado,
                'percentual_pl': percentual_pl
            })

        return render_template('resultado.html', nome_fundo=nome_fundo, cota=cota, pl=pl,
                               data_cota=data_cota, ativos=ativos)
    except Exception as e:
        return f"Erro ao processar XML: {e}"

if __name__ == '__main__':
    app.run(debug=True)
