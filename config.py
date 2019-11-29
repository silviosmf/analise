from datetime import datetime

class Variaveis():    

    #Parâmetros do Servidor
    '''
    caminhodb = "localhost"
    portadb = 27017
    hostServiorAplicacao = "192.168.1.60"
    '''

    #Parâmetros do Notebook

    caminhodb = "177.6.208.189"
    portadb = 27017
    hostServiorAplicacao = "localhost"

    
    #Parâmetros do PC
    '''
    caminhodb = "10.217.30.40"
    portadb = 27017
    hostServiorAplicacao = "localhost"
   
    caminhodb = "192.168.1.60"
    portadb = 27017
    hostServiorAplicacao = "localhost"
     '''
    dataAtual = datetime.now()
    diaSemana = str(dataAtual.strftime("%w"))
    dia = str(dataAtual.strftime("%d-%m-%Y")) 
    hora = dataAtual.strftime("%H:%M")

    horarioEuro = False
    
    #Horário Euro
    if((diaSemana == "0") and (hora > "17:00")):
        horarioEuro = True