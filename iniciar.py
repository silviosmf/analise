import csv
import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import sys
sys.path.insert(0,'./')
from config import Variaveis
from flask import Flask, jsonify, json
from flask import render_template

#-----------------------
#Cria e insere valores em uma tabela no MongoDB
#-----------------------
'''
db = client.MongoDBTeste

data = datetime.now()

insercao = []
insercao.append({"fonte":"Valor Econômico","titulo":"Título 5"})
insercao.append({"fonte":"Valor Econômico","titulo":"Título 6"})


db.tbl_teste.insert_many (
    [
        {"id":1,"nome":"Silvio Silva Miranda Filho"},
        {"id":2,"nome":"Alline Ferreira Agapito Miranda"},
        {"id":3,"nome":"Bernardo de Agapito Miranda"},
        {"id":4,"nome":"Beatriz de Agapito Miranda"}
    ]
)


print(insercao)
db.tbl_noticias.insert_many (insercao)
'''

#-----------------------
#Consulta ao Banco
#-----------------------

'''
db = client["MongoDBTeste"]
tbl_noticias = db["tbl_noticias"]

consulta = {"titulo":"Título 3"}

retorno = tbl_noticias.find_one(consulta)

print (retorno["fonte"])
data = retorno["data"]
print (data.year)
print (data.month)
print (data.day)
print (data.hour)
print (retorno)
'''

#-----------------------
#Remover campo no Banco
#-----------------------

def removerNoticia():
    client = MongoClient("localhost",27017)
    db = client["GCF"]
    tbl_noticias = db["tbl_noticias"]

    #remover = {"fonte":"Reuters"}
    remover = {"fonte":"Valor Econômico"}

    retorno = tbl_noticias.remove(remover)


def inserirPacoteCambio():
    client = MongoClient(Variaveis.caminhodb,Variaveis.portadb)
    db = client["GCF"]    

    pacotes = []
    for pacote in pacotesTeste:           
        cambios = []
        for cambio in pacote._listaCambio:
            cambios.append({"sigla":cambio._sigla, "porcentagem":cambio._porcentagem})
        pacotes.append({"dia":pacote._dia,"hora":pacote._hora, "listaCambio":cambios})
    print(pacotes)
    db.tbl_pacoteCambio.insert_many(pacotes)
    '''
    db.tbl_teste.insert_many (
        [
            {"id":1,"nome":"Silvio Silva Miranda Filho"},
            {"id":2,"nome":"Alline Ferreira Agapito Miranda"},
            {"id":3,"nome":"Bernardo de Agapito Miranda"},
            {"id":4,"nome":"Beatriz de Agapito Miranda"}
        ]
    )
    print(insercao)
    
    '''
#-----------------------
#Consulta ao Banco
#-----------------------

def consultaPacoteCambio():
    client = MongoClient(Variaveis.caminhodb,Variaveis.portadb)
    db = client["GCF"]
    colecao = db["tbl_pacoteCambio"]  
    consulta = {"dia":"24-11-2019", "hora":{"$regex": u"20"}}
    print(consulta)    
    retorno = colecao.find(consulta).count()
    print(retorno)


#consultaPacoteCambio()
#inserirPacoteCambio()

def testeOpenCSV():
    caminho = os.path.abspath("teste/info.csv")
    print(caminho)
    
    with open(caminho, "r") as f:
        reader = csv.reader(f)
        for linha in reader:
            #print(linha)
            for coluna in linha:
                print(coluna)
            
def openAnalistaCSV():
    #busca os caminhos dos arquivos que serão coletados dentro da pasta passado no parâmetro
    arquivos = listarArquivos('dados')
    for caminhoArquivo in arquivos:
        data = caminhoArquivo[-12:-10]+"/"+caminhoArquivo[-10:-8]+"/"+caminhoArquivo[-8:-4]
        ficheiro = open(caminhoArquivo, 'r')
        reader = csv.reader(ficheiro)
        colecao = []
        for linha in reader:
            linhas = str(linha).split(";")
            if((linhas[0][2:] == "Usuário") or (linhas[0][2:] == "Total")):
                continue
            colecao.append({"USUARIO":linhas[0][2:], "DATA":data, "EXIGENCIA":linhas[1], "DEFERIDO":linhas[2], "INDEFERIDO":linhas[3]})

        for dado in colecao:
            print(dado)    

def listarArquivos(caminho):
    lista = []
    for p, _, files in os.walk(os.path.abspath(caminho)):
        for arq in files:
            lista.append(os.path.join(p, arq))
            print(os.path.join(p, arq))
    return lista

#listarArquivos('teste/analistas')
#openAnalistaCSV()
#testeOpenCSV()    

iniciar = Flask(__name__, static_url_path='/')

#Analistas
@iniciar.route('/')
def analista():                        
    try:
        openAnalistaCSV()
        return render_template('analista.html')
    except Exception as e:
        return(str(e))     

if __name__ == '__main__':
        iniciar.run(host="localhost", debug=True)
