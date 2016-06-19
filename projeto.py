###############################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:    Gustavo Bernardo Lopes
#            
#
# Email:    gbl3@cin.ufpe.br
#            
#
# Data:        2016-06-12
#
# Descricao:  Este e' um modelo de arquivo para ser utilizado para a implementacao
#                do projeto pratico da disciplina de Programacao 1. 
#                 A descricao do projeto encontra-se no site da disciplina e trata-se
#                de uma adaptacao do projeto disponivel em 
#                http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/
#                O objetivo deste projeto e' implementar um sistema de analise de
#                sentimentos de comentarios de filmes postados no site Rotten Tomatoes.
#
# Licenca: The MIT License (MIT)
#            Copyright(c) 2016 Gustavo Bernardo Lopes
#
###############################################################################

import sys
import re


def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''    
    punctuation = ''''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result

def devolve_stopping_words(caminho):
    le_arquivo = open(caminho,"r")
    linhas = le_arquivo.readlines()
    le_arquivo.close()
    stopping_words = [clean_up(x) for x in linhas]   
    return stopping_words


def split_on_separators(original, separators):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            
    return filter(lambda x: x != '',re.split('[{0}]'.format(separators),original))
                    


def readTrainingSet(fname,caminho_stop_words):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''
    a = open(fname,"r")
    a.seek(0)
    linhas = a.readlines()
    palavras = []
    a.close()    
    words = {}
    stopping_words = devolve_stopping_words(caminho_stop_words)
    #Removendo as stopping words e possiveis erros no comentario
    for x in linhas:
        for y in split_on_separators(x[1:]," "):
            if clean_up(y).strip("0123456789\/`") not in stopping_words:
                palavras.append(clean_up(y).strip("0123456789\/`"))    
    freq = 0
    escore = 0
    escore_final = 0
    #Computando o Score medio das palavras e a frequencia que elas aparecem nas linhas
    for palavra in palavras:
        freq = 0
        escore = 0
        escore_final = 0
        for linha in linhas:
            if palavra in linha.lower():
                escore += int(linha[0])
                freq += 1
        #Evitando o erro de tentar dividir por 0
        if escore > 0 and freq > 0:        
            escore_final = escore / freq 
        else:
            escore_final = 0.0

        words[palavra] = (freq,escore_final)



    # TODO: implementar a funcionalidade aqui
   
    return words

def readTestSet(fname):
    ''' Esta funcao le o arquivo contendo o conjunto de teste
	retorna um vetor/lista de pares (escore,texto) dos
	comentarios presentes no arquivo.
    '''
    a = open(fname,"r")
    a.seek(0)
    linhas = a.readlines()
    a.close()
    reviews = []
    for x in linhas:     
        reviews.append((x[0],x[1:]))
    # TODO: implementar a funcionalidade
    return reviews

def computeSentiment(review,words,caminho_stop_words):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''
	# TODO: implementar a funcionalidade
    score = 0.0
    count = 0
    palavras = []
    stopping_words = devolve_stopping_words(caminho_stop_words)
    #Retirando as stopping words do review para poder ignorá-las
    palavras = [clean_up(x) for x in split_on_separators(review," ") if clean_up(x) not in stopping_words]
    #Computando o score das palavras do test set
    for palavra in palavras:
        if palavra in words:
            score += words[palavra][1]
            count += 1
        else:
            score += 2
            count += 1
#Evitando o erro de divisão por zero
    if score > 0:
        return score/count
    else:
        return 0.0

def computeSumSquaredErrors(reviews,words,caminho_stop_words):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''    
    sse = 0
    erro = 0
    count = 0
    # TODO: implementar a funcionalidade
    #Computando Erro
    for x in reviews:
        erro = computeSentiment(x[1],words,caminho_stop_words) - float(x[0])  
        sse += erro ** 2
        count += 1
    return sse / count

    
def main():
    
    # Os arquivos sao passados como argumentos da linha de comando para o programa
    # Voce deve buscar mais informacoes sobre o funcionamento disso (e' parte do
    # projeto).
    
    # A ordem dos parametros e' a seguinte: o primeiro e' o nome do arquivo
    # com o conjunto de treinamento, em seguida o arquivo do conjunto de teste.
    
    if len(sys.argv) < 4:
        print ('Numero invalido de argumentos')
        print ('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste> <arq-stopping_words>' )
        sys.exit(0)

    # Lendo conjunto de treinamento e computando escore das palavras
    #Inseri mais um argumento como parâmetro, para poder acessar o arquivo das stopping words
    words = readTrainingSet(sys.argv[1],sys.argv[3])
    
    # Lendo conjunto de teste
    reviews = readTestSet(sys.argv[2])
    
    # Inferindo sentimento e computando soma dos quadrados dos erros
    #Inseri mais um argumento como parâmetro, para poder acessar o arquivo das stopping words
    sse = computeSumSquaredErrors(reviews,words,sys.argv[3])

     
    
    print ('A soma do quadrado dos erros e\': {0}'.format(sse))
            

if __name__ == '__main__':
   main()
    
    
