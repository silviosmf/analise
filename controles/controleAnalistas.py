from flask import Flask, jsonify, json
from flask import render_template
from datetime import datetime, timedelta
import sys
sys.path.insert(0,'./persistencia')
import persistenciaAnalistas
from pandas import DataFrame

#print(df[(df.DATA > "26/11/2019") & (df.DATA < "28/11/2019")])
#print(df.NOME.unique()[0])

#for usuario in df.NOME.unique():
#    print(df[(df.NOME == usuario)])


#Retorna primeira letra maiuscula
# df["NOME"].str.title()
#Condições dentro do Frame
#df[df.DATA == "25/11/2019"]
#Retorna qtde de repetições do atributo
#df.NOME.value_counts()
#Retorna posição definida no index
#df.iloc[1:3]

def carregarAnalistaSelecionado():    
    colecao = []
    try:
        colecao = persistenciaAnalistas.consultarAnalistas()
    except Exception as e:
        print("Não conseguiu acessar o Banco de Dados")
        return(str(e))

    df = DataFrame(colecao)
    strDatas = []
    #Definir nome para consulta
    strNome = df.iloc[0].NOME 
    listDeferido = []
    # Pegar os deferimentos de nome definido anteriormente
    listd = df[(strNome == df.NOME)].DEFERIDO.values
    for item in listd:
        listDeferido.append(int(item))
    for data in df.DATA.unique():  
        splitData = str(data).split("-");             
        strDatas.append(splitData[2][0:2]+"/"+splitData[1]+"/"+splitData[0])

    print(strDatas)
    print(strNome)
    print(listDeferido)        
    datas = json.dumps(strDatas)
    nome = json.dumps(strNome)
    deferidos = json.dumps(listDeferido)


    strConteudo = """
    <html>
<head>
    <meta charset='utf-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <title>GCF - Gestor de Conteúdo Financeiro</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>  
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>     
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
</head>
    <body>
<canvas id="myChart" ></canvas>
      <script>
        
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
          type: 'line',
          data: {
              labels: 
              """+str(strDatas)+"""
              ,
              datasets: [{
                  label: '"""+str(strNome)+"""',
                  data: 
                  """+str(listDeferido)+"""
                  ,
                  backgroundColor: ['rgba(30, 96, 163, 0.5)'], 
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  yAxes: [{
                      ticks: {
                            max: 70,
                            min: 0,
                            stepSize: 1,
                          beginAtZero: true
                      }
                  }]
              }
          }
      });
      </script>
      </body>
      </html>
"""
    print(strConteudo)   

    try:
        return (strConteudo)
    except Exception as e:
        return(str(e))

def carregarAnalistaTodos():
    strNome = "alert('valor')"
    nome = json.dumps(strNome)
    try:
        return render_template('analistas.html',strNome=strNome)
    except Exception as e:
        return(str(e))

def carregarAnalistas():
    colecao = []
    try:
        colecao = persistenciaAnalistas.consultarAnalistas()
    except Exception as e:
        print("Não conseguiu acessar o Banco de Dados")
        return(str(e))

    df = DataFrame(colecao)
    strDatas = []
    #Definir nome para consulta
    strNome = df.iloc[0].NOME 
    listDeferido = []
    # Pegar os deferimentos de nome definido anteriormente
    listd = df[(strNome == df.NOME)].DEFERIDO.values
    for item in listd:
        listDeferido.append(int(item))
    for data in df.DATA.unique():
        #print(data)    
        splitData = str(data).split("-");             
        strDatas.append(splitData[2][0:2]+"/"+splitData[1]+"/"+splitData[0])
    print(strDatas)
    print(strNome)
    print(listDeferido)        
    datas = json.dumps(strDatas)
    nome = json.dumps(strNome)
    deferidos = json.dumps(listDeferido)
    listaNomes = []
    for nome in df.NOME.unique():
        listaNomes.append(nome.title())
    
    try:
        return render_template('analista.html', datas=datas, nome=nome, deferidos=deferidos, listaNomes=listaNomes,lenAnalistas=len(listaNomes))
    except Exception as e:
        return(str(e))     