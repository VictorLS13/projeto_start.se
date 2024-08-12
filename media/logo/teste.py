import pytesseract
import cv2
import aspose.words as aw 
import re
from datetime import datetime


def ler_boleto(caminho_pdf: str, caminho_png: str) -> str:
    pdf = aw.Document(caminho_pdf)
    pdf.save(caminho_png)
    imagem = cv2.imread(caminho_png)

    caminho = r'C:\Program Files\Tesseract-OCR'
    pytesseract.pytesseract.tesseract_cmd = caminho + r'\tesseract.exe'

    texto = pytesseract.image_to_string(imagem)

    padrao_cnpj = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
    resultado_cnpj = re.search(padrao_cnpj, texto)
    cnpj = resultado_cnpj.group(0) if resultado_cnpj else None

    padrao_data = r'\d{2}/\d{2}/\d{4}'
    datas = re.findall(padrao_data, texto)
    
    datas_validas = []
    for data in datas:
        try:
            datas_validas.append(datetime.strptime(data, '%d/%m/%Y'))
        except ValueError:
            continue

    if datas_validas:
        data_mais_recente = max(datas_validas).strftime('%d/%m/%Y')
    else:
        data_mais_recente = None

    return data_mais_recente, cnpj

print(ler_boleto('2F CAMINHOES - VCTO 05-08-2.pdf', 'teste2.jpg'))
