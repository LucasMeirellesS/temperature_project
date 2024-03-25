import pandas as pd
from datetime import datetime
import numpy as np
import seaborn.objects as so

class temperature_proj():

    def __init__(self):
        pass

    def visualiza_dados_totais(self, inicio_intervalo:str, fim_intervalo:str, arquivo:str, opcao = 1):
        """
            Método para visualizar os dados de acordo com o intervalo desejado pelo usuário.
            O método converte os dados inseridos da data inicial e final do intervalo de datas desejado em datetime, 
            salvando-os em variáveis para compara-los com os dados de data do arquivo para selecionar os dados que aparecerão na tela.
            sendo eles: 
                        1) todos os dados
                        2) apenas os de precipitação
                        3) apenas os de temperatura
                        4) apenas os de umidade e vento para o período informado
            Parâmetros:
                        inicio_intervalo: recebe uma string do formato "mês/ano" referindo-se ao ponto inicial do intervalo
                        fim_intervalo: recebe uma string do do formato "mês/ano" referindo-se ao ponto final do intervalo
                        arquivo: recebe uma string com o caminho do arquivo a ser utilizado
                        opcao: recebe um valor inteiro referênte as opções para quais dados o usuário deseja ver
        """
        # abrindo o arquivo para leitura
        with open(arquivo, "r") as arq:
            # percorrendo as linhas do arquivo
            for num, linha in enumerate(arq):
                linha = linha.split(",")
                # optei por usar a estrutura try except para o método ignorar a primeira linha quando fosse fazer as comparações e conversões de dados
                try:
                    # convertendo os dados para o formato datetime
                    formato_data = "%d/%m/%Y"
                    i_mes, i_ano = inicio_intervalo.split("/")
                    f_mes, f_ano = fim_intervalo.split("/")
                    data_i, data_f = datetime(int(i_ano), int(i_mes), 1).date(), datetime(int(f_ano), int(f_mes), 1).date()
                    
                    data = datetime.strptime(linha[0], formato_data).date()
                    
                    # criando condicionais para as opções desejadas
                    if opcao == 1:
                    
                        if data >= data_i and data <= data_f:
                            print(f"""
                                    data: {linha[0]}
                                    precip: {linha[1]}              
                                    maxima: {linha[2]}              
                                    minima: {linha[3]}             
                                    horas_insol: {linha[4]} 
                                    temp_media: {linha[5]}         
                                    um_relativa: {linha[6]}         
                                    vel_vento: {linha[7]}
                                    """)
                            
                    elif opcao == 2:
                        print(f"""
                                    data: {linha[0]}
                                    precip: {linha[1]}              
                                    """)
                    
                    elif opcao == 3:
                        print(f"""
                                    data: {linha[0]} 
                                    temp_media: {linha[5]}
                                    """)
                    
                    elif opcao == 4:
                        print(f"""
                                    data: {linha[0]}         
                                    um_relativa: {linha[6]}         
                                    vel_vento: {linha[7]}
                                    """)
                    
                except:
                    pass
    

    def remove_primeira_linha(self, arquivocsv:str):
        """
            Esse método foi criado para arquivos de dados csv
            cuja primeira linha é o nome das colunas dos quais os dados das linhas abaixo pertencem.
            Em vista disso esse método retira a primeira linha utilizando a tecnica de slicing de listas 
            para utilizar os dados das linhas seguintes e assim analisar dados. Reescrevendo-os em um novo arquivo

            parâmetros:
                        arquivocsv: Recebe o caminho do arquivo
            
            return:
                    retorna o arquivo sem a linha inicial.
        """
        # percorrendo as linhas do arquivo
        with open(arquivocsv, "r") as arq:
            # percorrendo os arquivos pelo método readlines que transforma cada linhas em um elemento de uma lista
            linhas = arq.readlines()
        
        # utilizando slicing para remover a primeira linha
        linhas = linhas[1:]
        
        # criando novo arquivo com as linha removidas
        novo_arquivo = 'novo_arquivo.txt'
        with open(novo_arquivo, 'w+') as arq2:
            for linha in linhas:
                arq2.write(linha)
            return novo_arquivo
        


    def cria_dicionario(self, arquivocsv:str):
        """
            Esse método transforma os dados de cada linha do arquivo em listas e os converte em dicionários
            onde os dados da primeira linha são as chaves e os dados restantes onde as respectivas posições 
            são relativas as posições dos dados.

            parâmetros:
                        arquivocsv: recebe o caminho do arquivo

            return:
                    retorna um dicionário e o arquivo sem a primeira linha para usos futuros
        """
        # abrindo o arquivo para leitura 
        with open(arquivocsv, "r") as arq:
            
            # percorrendo o arquvio e transformando as linhas em listas
            for num, linha in enumerate(arq):
                linha = linha.split(",")
                
                # Criando as chaves do dicionário com a primeira linha do arquivo
                if num == 0:
                    dicio = {dado.replace("\n",""):[] for dado in linha}
            
            # retornando dicionário e arquivo de dados para sua inserção
            return dicio, self.remove_primeira_linha(arquivocsv)
        
    
    def inclui_dados(self, arquivocsv:str, dicio:dict):
        """ 
            Esse método inclui os dados de um arquivo csv dem um dicionário.
            parâmetros:
                        arquivocsv: recebe o caminho de um arquivo
                        dicio: recebe o dicionário a ser colocado
            return:
                    Retorna um dicionário
        """
        # abrindo o arquivo para leitura 
        with open(arquivocsv, "r") as proj:
            
            # percorrendo o arquvio e transformando as linhas em listas
            for num, linha in enumerate(proj):
                linha = linha.split(",")
                
                # percorrendo dicionário e incluindo os dados respectivos no mesmo
                for num, dado in enumerate(linha):
                    dicio[list(dicio.keys())[num]].append(linha[num].replace("\n",""))
        return dicio
    
    def cria_conjunto(self, arquivocsv:str):
        """
            Esse método executa os métodos cria_dicionário e inclui_dados
            para criar um dicionário.
            parâmetros:
                        arquivocsv: recebe o caminho de um arquivo do formato csv
            
            return:
                    retorna um dicionário com todos os dados invluídos
        """
        # rodando função para cirar dicionário
        conjunto, novo_arquivo = self.cria_dicionario(arquivocsv)
        
        # retornando um dicionário com os dados inclusos
        return self.inclui_dados(novo_arquivo, conjunto)
    

    def dict_temp_data_conversor(self, dicio:dict):
        """
        Esse método converte os dados de um dicionário de string para o tipo apropriado, dada ou float
        parâmetros:
                    dicio: recebe um dicionário
        return:
                retorna o dicionário com os dados convertidos
        """
        # percorrendo as chaves do dicionário
        for chave in dicio:
            
            # percorrendo cada valor do dicionário
            for i, item in enumerate(dicio[chave]):
                
                # optei por usar a estrutura try except para para fazer as conversões caso dê erro na primeira tentativa de converter os dados para data, ele converte para float
                try:
                    # definindo relatanto o formato da data no arquivo
                    formato_data = "%d/%m/%Y"
                    
                    # convertendo os dados para data
                    dicio[chave][i] = datetime.strptime(item, formato_data)
                    
                    # caso erro
                except ValueError:
                    
                    # converter para float
                    try:
                        dicio[chave][i] = float(item)
                    
                    # casi erro, mostrar mensagem de que não foi possível converter
                    except ValueError:
                        print("Impossível de converter os dados!")
        return dicio
    
    def mes_mais_chuvoso(self, arquivocsv:str):
        """
        Esse método compara os dados do arquivo para saber qual o mês que teve a maior precipitação 
        para e imprime na tela o mês mais chuvoso com o valor de sua precipitação
        parâmetros:
                    arquivocsv: recebe o caminho de um arquivo
        """
        # coloquei as chaver de dados para facilitar na seleção do mês
        meses = {1:'Janeiro', 2:'Fevereiro', 3:'Março', 4:'Abril', 5:'Maio', 6:'Junho', 7:'Julho', 8:'Agosto', 9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'}
        
        # iniciando uma variável para maior precipitação
        maior_precid = 0
        
        # abrindo arquivo no modo de leitura
        with open(arquivocsv, "r") as proj:

            # percorrendo as linhas do arquivo e transformando as linhas em listas
            for num, linha in enumerate(proj):
                linha = linha.split(",")

                # usei o try except aqui apra 
                try:
                    formato_data = "%d/%m/%Y"
                    mes = datetime.strptime(linha[0], formato_data).month
                    ano = datetime.strptime(linha[0], formato_data).year
                    linha[1] = float(linha[1])
                    if maior_precid == 0:
                        maior_precid = linha[1]
                        mes_maior_precid = meses[mes]
                        ano_maior = ano
                    
                    elif linha[1] > maior_precid:
                        maior_precid = linha[1]
                        mes_maior_precid = meses[mes]
                        ano_maior = ano
                
                except:
                    pass
        print(f"O mês com maior precipicação foi {mes_maior_precid} do ano {ano_maior} com a precipitação de {maior_precid}")

    
    def temp_min_media_mes_ultimos11(self, arquivocsv:str, mes:str):
        """
        Esse método calcula a média mínima da temperatura de um determinado mês a cada ano
        e salva esses dados num dicionário.
        parâmetros:
                    arquivocsv: recebe o caminho de um arquivo
        
                    mes: recebe o número do mês desejado
        return:
                retorna um dicionário
        """
        # criando dicionário para facilitar a seleção do mês
        meses = {1:'janeiro', 2:'fevereiro', 3:'março', 4:'abril', 5:'maio', 6:'junho', 7:'julho', 8:'agosto', 9:'setembro', 10:'outubro', 11:'novembro', 12:'dezembro'}
        
        # criando dicionário de m~es
        meses_med = {}
        
        # criando loop para inserção de datas de 2006 a 2016
        for a in range(2006, 2017):
            meses_med[f"{mes}{a}"] = ''
            
        # abrindo arquivo para leitura
        with open(arquivocsv, "r") as arq:
            for key in meses_med:
                soma = 0
                count = 0

                # utilizei o método seek para ele reiniciar a leitura do arquivo para conseguir comparar todos os dados
                arq.seek(0)
                # convertendo as linhas em listas
                for num, linha in enumerate(arq):
                    linha = linha.split(",")
                    
                    # utilizei o try except aqui apra ignorar a primeira linha do arquivo  
                    try:
                        # relatando o formato da data no arquivo
                        formato_data = "%d/%m/%Y"

                        # capturando o numero do mês
                        mes_num = datetime.strptime(linha[0], formato_data).month
                        
                        # capturando o ano
                        ano = datetime.strptime(linha[0], formato_data).year
                        
                        # criando a chave para o dicionário para comparação
                        chave = f"{meses[mes_num]}{ano}"
                        
                        # comparando chave criada com a chave do dicionário anterios
                        if chave == key:
                            
                            # realizando soma dos dados para pegar a média 
                            soma += float(linha[3])

                            # criando variável de contágem para o calculo da média
                            count +=1

                    except:
                        pass
                # condicional para evitar erro de divisão por 0
                if soma != 0:
                    media = soma/count
                else:
                    media = 0
                
                # salvando média no dicionário criado para média
                meses_med[key] = media
            
        return meses_med
    
    def analise_gradica_11anos(self, arquivocsv:str, mes:str):
        
        """
        Esse método mostra na tela uma representação gráfica do dicionário de médias criado anteriormete
        parâmetros:
                    arquivo: recebe o caminho de um arquivo
                    mes: recebe o nome de um mês 
        return:
                retorna um gráfico criado utilizando o seaborn.objects
        """
        # criando o dicionário das médias com o método temp_min_media_mes_ultimos11
        dicio = self.temp_min_media_mes_ultimos11(arquivocsv, mes)
        y = list(dicio.values())
        x = list(dicio.keys())
        
        # gerando o plot com o seaborn.objects
        plot= (
            so.Plot(dicio,
                    y=y,
                    x=x,
                    color=x)
            .layout(size=(15,10))
            .label(title=f"Média de temperatura mínima do {mes.capitalize()} em 11 anos")
            .add(so.Bars(),so.Stack())


        )
        return plot
    

    def media_geral_mes_11(self, arquivocsv:str, mes:str):
        """
        Método criado para retornar a média do dicionário de médias conforme foi pedido no projeto
        percorrendo o dicionário criado nos métodos anteriores.
        parâmetros:
                arquivocsv: recebe o caminho de um arquivo
                mes: recebe o nome do mês desejado para criar o dicionário
        return:
                retorna a o valor da média geral
        """
        # criando o dicionário
        dicio = self.temp_min_media_mes_ultimos11(arquivocsv, mes)
        # extraindo a média por meio do numpy
        media_geral = np.mean(list(dicio.values()))
        return media_geral
    

