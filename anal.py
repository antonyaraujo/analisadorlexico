import os

# Analisador token
digito = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letra = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",]
delimitadores = [";", ",", "(", ")", "[", "]", "{", "}", "."]
reservadas = ["var", "const", "struct", "procedure", "function", "start", "return", "if", "else", "then", "while", "read", "print", "int", "real", "boolean", "string", "true", "false"]
aritmeticos = ["+", "-", "/", "*", "++", "--"]
relacionais = ["!=", "==", "<", "<=", ">", ">=", "="]
logicos = ["!", "&&", "||"]

tabela_ascii = []
for i in range(32, 126): 
    tabela_ascii.append(chr(i))
print(tabela_ascii[2])
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

def analise(arquivo):
    erros = []
    tokens = []
    acumulador = ""
    for linha in arquivo:        
        # Percorre caracter a caracter da linha
        corrigida = linha.replace("\n", "")
        if(len(acumulador) > 2):
            if(acumulador[0] != "/" or acumulador[1] != "*"):
                acumulador = ""             
        for caracter in corrigida:            
            # verifica se o caracter atual é válido
            if(caracter in tabela_ascii):
                acumulador += caracter      
                # Classifica delimitadores de comentário
                if(acumulador[0] == "/"):
                    if(len(acumulador) > 1):
                        if(acumulador[1] == "*" or acumulador[1] == "/"):
                            # É um comentário                        
                            if(len(acumulador) >= 4):
                                if(acumulador[len(acumulador)-1] == "/" and acumulador[len(acumulador)-2] == "*"):
                                    token = "<CoM, /*>"
                                    tokens.append(token)
                                    token = "<CoM, */>"
                                    tokens.append(token)
                                    acumulador = ""
                                    next
                                else:
                                    if(acumulador[len(acumulador)-1] == "\\" and acumulador[len(acumulador)-2] == "n"):
                                        token = "<CoM, //>"
                                        tokens.append(token)
                                        acumulador = ""
                                        next
                            else:                                
                                    next
                        else:
                            # Classifica eventualmente a barra como operador aritmético
                            token = "<ART, " + acumulador[:-1] + ">"
                            tokens.append(token)
                            acumulador = acumulador[1:]
                else:                    
                    # Classifica delimitadores                    
                    if(acumulador[0] in delimitadores):
                        print(acumulador[0])
                        token = "<DEL, " + acumulador[0] + ">"
                        tokens.append(token)
                        acumulador = acumulador[1:]
                    else:
                        # Classifica numeros
                        if(acumulador[0] in digito or acumulador[0] == '-' or acumulador[0] == " " or acumulador[0] == "    "):
                            # Verificar ponto no número                        
                            if(caracter == '.'):
                                if(acumulador[:-1].find('.') != -1): #verifica se já há ponto no número
                                    erro = "<NMF, " + acumulador + ">"
                                    erros.append(erro)
                                    acumulador = acumulador[:-1] #remove o último caracter
                                else:
                                    if(acumulador == ("-")):
                                        erro = "<NMF, " + acumulador + ">"
                                        erros.append(erro)
                                        acumulador = acumulador[:-1]
                            else:
                                if(caracter not in digito):
                                    if(caracter != " " or acumulador[0] != " "):
                                        token = "<NRO, " + acumulador[:-1] + ">"
                                        tokens.append(token)
                                        acumulador = caracter

                        else:
                            # Verifica espaçoe tab
                            if(acumulador[0] == "\t" or acumulador[0] == " "):
                                acumulador = acumulador[1:]
                                next
                            else:
                                # Classifica Cadeia de caracteres
                                print("ALGO CHEGOU", acumulador)
                                if(acumulador[0] == "\""):
                                    print("ENTROU NO PRIMEIRO")
                                    if(len(acumulador) > 1):
                                        if(caracter  == "\""):
                                            token = "<CAC, " + acumulador + ">"
                                            tokens.append(token)
                                            acumulador = ""
                                    else:
                                        print("PORTA: ", acumulador)
                                        next
                                else:
                                    # Classifica operadores aritmeticos
                                        if(acumulador[0] in aritmeticos):
                                            if(acumulador in aritmeticos):
                                                if(acumulador == "+" or acumulador == "-"):
                                                    next
                                                else:
                                                    token = "<ART, " + acumulador + ">"
                                                    tokens.append(token)
                                                    acumulador = ""
                                            else:                                
                                                token = "<ART, " + acumulador[:-1] + ">"
                                                tokens.append(token)
                                                acumulador = caracter
                                        else:
                                            if(acumulador[0] == "!"):
                                                if(acumulador == "!="):
                                                    token = "REL, " + acumulador + ">"
                                                    tokens.append(token)
                                                    acumulador = ""
                                                else:
                                                    token = "<LOG, " + acumulador[:-1] + ">"
                                                    tokens.append(token)
                                                    acumulador = acumulador[1:]
                                            else:
                                                #Classifica operadores relacionais
                                                if(acumulador[0] in relacionais):
                                                    if(acumulador[0] == "<" or acumulador[0] == ">" or acumulador[0] == "="):
                                                        if(caracter not in relacionais):
                                                            token = "<REL, " + acumulador[:-1] + ">"
                                                            tokens.append(token)
                                                            acumulador = caracter
                                                        else:
                                                            next
                                                    else:
                                                        if(acumulador in relacionais):
                                                            token = "<REL, " + acumulador + ">"
                                                            tokens.append(token)
                                                            acumulador = ""
                                                else:
                                                    # Classifica operadores lógicos                  
                                                    # print("chega aqui: ", acumulador)                          
                                                    if(acumulador[0] == "&" or acumulador[0] == "|"):                                                
                                                        if(acumulador in logicos):                                                    
                                                            token = "<LOG, " + acumulador + ">"
                                                            tokens.append(token)
                                                            acumulador = ""                                        
                                                        else:
                                                            next
                                                    else:
                                                        # Classifica identificadores
                                                        if(acumulador[0] in letra):
                                                            # Classifica palavras reservadas
                                                            if(acumulador in reservadas):                                                                
                                                                token = "<PRE, " + acumulador + ">"
                                                                tokens.append(token)
                                                                acumulador = ""
                                                            else:
                                                                if(caracter not in letra and caracter not in digito and caracter != "_" and caracter == " "):
                                                                    token = "<IDE, " + acumulador[:-1] + ">"
                                                                    tokens.append(token)
                                                                    acumulador = caracter
                                                        else:
                                                            next
            else:         
                # Se o caracter não é válido (de 32 a 126 a tabela ASCII, com excecao do 34 e acrescimo do caracter de tab (9))       
                erro = "<TMF, " + caracter + ">"
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