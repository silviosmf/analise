import csv
import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import sys
sys.path.insert(0,'./')
from config import Variaveis
from flask import Flask, jsonify, json
from flask import render_template
from pandas import DataFrame


#-----------------------
#Consulta ao Banco
#-----------------------

def consultarAnalistas():
    client = MongoClient(Variaveis.caminhodb,Variaveis.portadb)
    db = client["GCF"]
    colecao = db["tbl_analista"]  
    #consulta = {"dia":"24-11-2019", "hora":{"$regex": u"20"}}
    #print(consulta)    
    #retorno = colecao.find(consulta).count()
    retorno = colecao.find()
    return retorno


#consultaPacoteCambio()
#inserirPacoteCambio()

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
    arquivos = listarArquivos('dados')
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

def salvarDadosMongoDB():
    colecao = coletarAnalistaCSV()
    client = MongoClient(Variaveis.caminhodb,Variaveis.portadb)
    db = client["GCF"]    
    db.tbl_analista.insert_many(colecao)

#salvarDadosMongoDB()


