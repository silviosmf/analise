import csv
import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import sys
sys.path.insert(0,'./controles')
import controleAnalistas
from config import Variaveis
from flask import Flask, jsonify, json
from flask import render_template
from pandas import DataFrame


def testeOpenCSV():
    caminho = os.path.abspath("teste/info.csv")
    print(caminho)
    
    with open(caminho, "r") as f:
        reader = csv.reader(f)
        for linha in reader:
            print(linha)
            for coluna in linha:
                print(coluna)
            
def coletarAnalistaCSV():
    colecao = []
    #busca os caminhos dos arquivos que serão coletados dentro da pasta passado no parâmetro
    arquivos = listarArquivos('persistencia/dados')
    for caminhoArquivo in arquivos:
        data = caminhoArquivo[-12:-10]+"/"+caminhoArquivo[-10:-8]+"/"+caminhoArquivo[-8:-4]
        ficheiro = open(caminhoArquivo, 'r')
        reader = csv.reader(ficheiro)
        
        for linha in reader:
            linhas = str(linha).split(";")
            if((linhas[0][2:] == "Usuário") or (linhas[0][2:] == "Total")):
                continue
            d = datetime.strptime(data, "%d/%m/%Y")
            colecao.append({"DATA":d, "NOME":linhas[0][2:], "EXIGENCIA":int(linhas[1]), "DEFERIDO":int(linhas[2]), "INDEFERIDO":int(linhas[3])})

        #for dado in colecao:
            #print(dado)    
    return colecao

def listarArquivos(caminho):
    lista = []
    for p, _, files in os.walk(os.path.abspath(caminho)):
        for arq in files:
            lista.append(os.path.join(p, arq))
            #rint(os.path.join(p, arq))
    return lista

def montarLista():
    colecao = coletarAnalistaCSV()
    df = DataFrame(colecao)
    return df
 
iniciar = Flask(__name__, static_url_path='/static')

#Analistas
@iniciar.route('/')
def analista(): 
    return controleAnalistas.carregarAnalistas()

@iniciar.route('/analise')
def analise():                        
    return controleAnalistas.carregarAnalistaSelecionado()

@iniciar.route('/analistas')
def analistas():                        
    return controleAnalistas.carregarAnalistaTodos()

@iniciar.route('/selecionarAnalista', methods=['GET','POST'])
def selecionarAnalista():
    
    print("Executou........")
    return jsonify(valor="novo valor")    

if __name__ == '__main__':
        iniciar.run(host="localhost", debug=True)


