import os

# Analisador token
digito = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letra = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",]
delimitadores = [";", ",", "(", ")", "[", "]", "{", "}", "."]
reservadas = ["var", "const", "struct", "procedure", "function", "start", "return", "if", "else", "then", "while", "read", "print", "int", "real", "boolean", "string", "true", "false"]
aritmeticos = ["+", "-", "/", "*", "++", "--"]
relacionais = ["!=", "==", "<", "<=", ">", ">=", "="]
logicos = ["!", "&&", "||"]
espaco = [" ", "\t"]

tabela_ascii = []
for i in range(32, 126): 
    tabela_ascii.append(chr(i))
tabela_ascii.pop(2)
tabela_ascii.append(chr(9))

def ler_arquivo(caminho_arquivo):
    arquivo = open('files/input/' + caminho_arquivo)
    linhas = arquivo.readlines()
    arquivo.close()
    return linhas

# Funcao responsavel por escrever os tokens e 
def escrever_arquivo(caminho_arquivo, tokens, erros):
    buffer = ""
    for token in tokens:
        buffer += token + "\n"

    buffer += "\n"

    for erro in erros:
        buffer += erro + "\n"

    arquivo = open("files/output/"+caminho_arquivo.replace(".txt", "")+'-saida.txt', 'w')
    arquivo.write(buffer)

def adicionar_token(tokens, linha, sigla, lexema):
    token = str(linha).zfill(2) + " " + sigla + " " + lexema
    tokens.append(token)

def adicionar_erro(erros, linha, sigla, lexema):
    erro = str(linha).zfill(2) + " " + sigla + " " + lexema
    erros.append(erro)

def analise(arquivo):
    erros = []
    tokens = []
    acumulador = ""
    contagem_linha = 0
    for linha in arquivo:        
        contagem_linha += 1
        corrigida = linha.replace("\n", " ")        
        if(len(acumulador) > 2):
            if(acumulador[0] == "/" and acumulador[1] == "/"):
                adicionar_token(tokens, contagem_linha, "CoM", acumulador)
                acumulador = ""
        # Percorre caracter a caracter da linha
        for caracter in corrigida:
            # Adiciona o caracter ao acumulador
            acumulador += caracter
            # verifica se o caracter inicial do lexema é válido
            if(acumulador[0] in tabela_ascii or acumulador[0] != "\""):
                # Classifica delimitadores de comentário
                if(acumulador[0] == "/"):
                    if(len(acumulador) > 1):
                        if(acumulador[1] == "*"): # É um comentário em bloco
                            if(len(acumulador) >= 4):
                                # Verifica se o comentário em bloco foi fechado
                                if(acumulador[len(acumulador)-1] == "/" and acumulador[len(acumulador)-2] == "*"):                                    
                                    adicionar_token(tokens, contagem_linha, "CoM", acumulador)                                    
                                    acumulador = ""
                                    next
                                else:
                                    next
                                """
                                else:
                                     if(acumulador[1] == "*" and acumulador[0] == "/"):
                                        erro = str(contagem_linha).zfill(2) + " CoMF " + acumulador
                                        erros.append(erro)
                                        acumulador = ""    
                                """    
                            else:                                           
                                next
                        else:
                            if(acumulador[1] == "/"):
                                next
                            else:
                                # Classifica a barra como operador aritmético e parte para o próximo estado                                
                                adicionar_token(tokens, contagem_linha, "ART", acumulador[0])
                                acumulador = acumulador[1:]
                else:                                        
                    # Classifica delimitadores                    
                    if(acumulador[0] in delimitadores):
                        adicionar_token(tokens, contagem_linha, "DEL", acumulador[0])                        
                        acumulador = acumulador[1:]
                    else:
                        # Verifica espaço e tab e separa
                        if(acumulador[0] == "\t" or acumulador[0] in espaco):                            
                            acumulador = acumulador[1:]
                            next
                        else:
                            # Classifica numeros
                            if(acumulador[0] in digito or acumulador[0] == '-' or acumulador[0] in espaco):
                                # Verificar ponto no número                                                                
                                if(acumulador[0] == "-"): # É um número negativo
                                    if(len(acumulador) > 1):                                        
                                        if(acumulador[0] == "-" and acumulador[1] == "."):
                                            adicionar_erro(erros, contagem_linha, "NMF", acumulador)
                                            acumulador=""
                                        else:
                                            if(caracter == "."):
                                                if(acumulador[:-1].find('.') != -1):
                                                    adicionar_erro(erros, contagem_linha, "NMF", acumulador[:-1])
                                                    acumulador=""
                                            else:
                                                if(caracter == '-'):
                                                    if(acumulador[len(acumulador)-2] in digito):
                                                        adicionar_token(tokens, contagem_linha, "NRO", acumulador[:-1])
                                                        acumulador=caracter
                                                    else:                                                        
                                                        if(acumulador[len(acumulador)-2] == "-"):
                                                            adicionar_token(tokens, contagem_linha, "ART", acumulador)
                                                            acumulador=""
                                                else:
                                                    if(caracter not in digito):                                                        
                                                        if(caracter == "-"):
                                                            adicionar_token(tokens, contagem_linha, "NRO", acumulador[:-1])
                                                            adicionar_token(tokens, contagem_linha, "ART", acumulador[len(acumulador)-1])
                                                            acumulador=""
                                                        else:
                                                            if(acumulador[len(acumulador)-2] in digito):
                                                                if(caracter == "-"):
                                                                    adicionar_token(tokens, contagem_linha, "NRO", acumulador[:-1])
                                                                    adicionar_token(tokens, contagem_linha, "ART", acumulador[len(acumulador)-1])
                                                                    acumulador=""
                                                                adicionar_token(tokens, contagem_linha, "NRO", acumulador[:-1])
                                                            else:
                                                                adicionar_token(tokens, contagem_linha, "ART", acumulador[:-1])
                                                            acumulador=caracter                                                    
                                else: # Número positivo
                                    if(acumulador[0] in digito):
                                        if(caracter not in digito or caracter not in espaco):                                            
                                            if(caracter == "."):                                                
                                                if(acumulador[:-1].find('.') != -1):
                                                    if(acumulador[len(acumulador)-2] in digito):
                                                        adicionar_token(tokens, contagem_linha, "NRO", acumulador[:-1])
                                                    else:
                                                        adicionar_erro(erros, contagem_linha, "NMF", acumulador[:-1])
                                                    acumulador=caracter
                                                else:
                                                    next
                                            else:
                                                if(caracter not in digito):
                                                    if(acumulador[len(acumulador)-2] in digito):
                                                        adicionar_token(tokens, contagem_linha, "NRO", acumulador[:-1])
                                                    else:
                                                        adicionar_erro(erros, contagem_linha, "NMF", acumulador[:-1])
                                                    acumulador = caracter                                                                               
                                        else:
                                            if(caracter == "."):
                                                print("")
                                    else:
                                        if(acumulador[0] in espaco):
                                            if(caracter not in espaco):
                                                acumulador= acumulador[:-1]
                            else:
                                # Classifica operadores aritmeticos
                                    if(acumulador[0] in aritmeticos):                                            
                                        if(acumulador[0] in aritmeticos and (caracter != "+" or caracter != "-")):                                                                                                                                            
                                            adicionar_token(tokens, contagem_linha, "ART", acumulador[:-1])
                                            acumulador = caracter
                                        else:
                                            if(acumulador in aritmeticos):                                                    
                                                adicionar_token(tokens, contagem_linha, "ART", acumulador)
                                                acumulador = ""
                                    else:
                                        if(acumulador[0] == "!"):
                                            if(acumulador == "!="):                                                    
                                                adicionar_token(tokens, contagem_linha, "REL", acumulador)
                                                acumulador = ""
                                            else:                                                    
                                                adicionar_token(tokens, contagem_linha, "LOG", acumulador[0])
                                                acumulador = acumulador[1:]
                                        else:
                                            #Classifica operadores relacionais
                                            if(acumulador[0] in relacionais):
                                                if(acumulador[0] == "<" or acumulador[0] == ">" or acumulador[0] == "="):
                                                    if(caracter not in relacionais):                                                            
                                                        adicionar_token(tokens, contagem_linha, "REL", acumulador[:-1])
                                                        acumulador = caracter
                                                    else:
                                                        next
                                                else:
                                                    if(acumulador in relacionais):                                                            
                                                        adicionar_token(tokens, contagem_linha, "REL", acumulador)
                                                        acumulador = ""
                                            else:
                                                # Classifica operadores lógicos                  
                                                # print("chega aqui: ", acumulador)                          
                                                if(acumulador[0] == "&" or acumulador[0] == "|"):                                                
                                                    if(acumulador in logicos):                                                                                                                
                                                        adicionar_token(tokens, contagem_linha, "LOG", acumulador)
                                                        acumulador = ""                                        
                                                    else:
                                                        next
                                                else:
                                                    # Classifica identificadores
                                                    if(acumulador[0] in letra):
                                                        # Classifica palavras reservadas
                                                        if(acumulador in reservadas):
                                                            adicionar_token(tokens, contagem_linha, "PRE", acumulador)
                                                            acumulador = ""
                                                        else:
                                                            #print("acumulador ", acumulador, "caracter ", caracter)
                                                            if(caracter not in letra and caracter not in digito and caracter != "_" and caracter not in espaco):                                                                                                                                        
                                                                adicionar_token(tokens, contagem_linha, "IDE", acumulador[:-1])
                                                                acumulador = caracter                                                                                                                                    
                                                            else:
                                                                if(caracter in espaco):                                                                        
                                                                    adicionar_token(tokens, contagem_linha, "IDE", acumulador[:-1])
                                                                    acumulador = caracter

                                                    else:
                                                        # Token mal formado
                                                        if(caracter in digito or caracter in espaco or caracter in letra):
                                                            erro = str(contagem_linha).zfill(2) + " TMF " + acumulador[:-1]
                                                            erros.append(erro)
                                                            acumulador = caracter
            else:         
                print(acumulador)
                # verifica se é uma cadeia de caracteres
                if(acumulador[0] == "\""):
                    if(len(acumulador) > 1):                        
                        if(caracter not in tabela_ascii):
                            erro = str(contagem_linha).zfill(2) + " CMF " + acumulador
                            erros.append(erro)
                            acumulador = ""
                        else:
                            if(caracter == "\""):                                
                                adicionar_token(tokens, contagem_linha, "CAC", acumulador)
                                acumulador = ""
                            else:
                                if(caracter in espaco):
                                    erro = str(contagem_linha).zfill(2) + " CMF " + acumulador
                                    erros.append(erro)
                                    acumulador = ""

                else:
                    # Se o caracter não é válido (de 32 a 126 a tabela ASCII, com excecao do 34 e acrescimo do caracter de tab (9))       
                    if(len(acumulador)>=4):
                        if(acumulador[len(acumulador)-2] != "*" and acumulador[len(acumulador)-1] != "/"):
                            adicionar_erro(erros, contagem_linha, 'CoMF', acumulador)
                        else:
                            erro = str(contagem_linha).zfill(2) + " TMF " + caracter
                            erros.append(erro)

    return [tokens, erros]

def main():
    pasta = './files/input'
    arquivos_filtrados = []
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            if(arquivo.endswith(".txt")):
                arquivos_filtrados.append(arquivo)
    
    for arquivo in arquivos_filtrados:
        [tokens, erros] = analise(ler_arquivo(arquivo))
        escrever_arquivo(arquivo, tokens, erros)
    
if __name__ == "__main__":    
    main()