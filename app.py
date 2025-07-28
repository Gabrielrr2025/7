from flask import Flask, render_template, request
import os
import xml.etree.ElementTree as ET
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["file"]
        if not file or not file.filename.endswith(".xml"):
            return "Arquivo inválido. Envie um arquivo .xml", 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        tree = ET.parse(filepath)
        root = tree.getroot()

        # Busca os dados principais
        info_fundo = root.find(".//Informe")
        if info_fundo is None:
            return "Não foi possível encontrar o elemento 'Informe' no XML."

        cnpj = info_fundo.findtext("CNPJ", default="Não encontrado")
        nome_fundo = info_fundo.findtext("NomeFundo", default="Não encontrado")
        dt_comptc = info_fundo.findtext("DtComptc", default="Não encontrado")
        pl_fundo = info_fundo.findtext("VLPatrimLiq", default="Não encontrado")

        # Busca os ativos
        ativos = []
        for item in root.findall(".//InformeDetalhe"):
            ativo = {
                "Código ISIN": item.findtext("CdIsin", default=""),
                "Tipo Ativo": item.findtext("TpAtivo", default=""),
                "Descrição": item.findtext("DenomSocial", default=""),
                "Quantidade": item.findtext("QtdAtivo", default="0"),
                "Valor Mercado": item.findtext("VlrMercado", default="0"),
                "Percentual da Carteira": item.findtext("PctPapelao", default="0")
            }
            ativos.append(ativo)

        df = pd.DataFrame(ativos)

        return render_template(
            "resultado.html",
            cnpj=cnpj,
            nome_fundo=nome_fundo,
            dt_comptc=dt_comptc,
            pl_fundo=pl_fundo,
            tables=[df.to_html(classes="table table-striped", index=False)],
            titles=df.columns.values
        )

    except Exception as e:
        return f"Erro ao processar o XML: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
