# Analisador Lexico
digito = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letra = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",]
delimitadores = [";", ",", "(", ")", "[", "]", "{", "}", "."]
reservadas = ["var", "const", "struct", "procedure", "function", "start", "return", "if", "else", "then", "while", "read", "print", "int", "real", "boolean", "string", "true", "false"]
aritmeticos = ["+", "-", "/", "*", "++", "--"]
logicos = ["|", "&&", "||"]
erros = []
lexicos = []

def gerar_simbolos():
    simbolos = []
    for i in range(32, 126):        
        simbolos.append(chr(i))
    simbolos.pop(2)
    return simbolos
    

def ler_arquivo(caminho_arquivo):
    arquivo = open('files/' + caminho_arquivo)
    linhas = arquivo.readlines()
    arquivo.close()
    return linhas

def analise(arquivo):
    for linha in arquivo:
        corrigida = linha.replace("\n", "")
        corrigida = corrigida + " "
        acumulador = ""
        for caracter in corrigida:        
            # 1º Verificar se é um caracter válido
            if (caracter in gerar_simbolos()):                
                # Verifica se é o primeiro caractér do léxico
                if(len(acumulador) == 0):
                    #1º É um digito ou negativo (-) ou espaço ( ) ?
                    if(caracter in digito or caracter == '-' or caracter == " " or caracter == "    "):
                        print("primeiro digito, caracter: " + caracter)
                        acumulador += caracter  
                    else:                        
                        if(caracter == "/"):
                            acumulador += caracter  
                        else:
                            acumulador += caracter
                else:                              
                    # Classifica comentários
                    if(acumulador[0] == "/" and len(acumulador) > 1):
                        if(acumulador[1] == "*" or acumulador[1] == "/"):
                            if(len(acumulador) >= 4):
                                if(acumulador[len(acumulador-1)] == "*" and acumulador[len(acumulador-2)] == "/"):
                                    next
                        else:
                            next
                    else:
                        # Classificando numero
                        if(acumulador[0] in digito or acumulador[0] == '-' or acumulador[0] == " " or acumulador[0] == "    "):
                            # Verificar ponto no número                        
                            if(caracter == '.'):
                                if(acumulador.find('.') != -1):
                                    erros.append(acumulador)
                                else:
                                    if(acumulador != ("-")):
                                        print("analise digito: " + caracter)
                                        acumulador += caracter
                                    else:
                                        erros.append(acumulador)
                                        acumulador = ""
                            else: 
                                print(caracter)
                                # Condição de parada de classificação de número
                                if(caracter in digito):
                                    print("digito adicionado: " + caracter)
                                    acumulador += caracter                                                                
                                else:
                                    if(acumulador != " "):
                                        lexico = "<NRO, " + acumulador + ">"
                                        lexicos.append(lexico)
                                        acumulador = caracter
                                    else:
                                        acumulador=caracter
                        else:
                            # Classificando identificadores
                            if(caracter in letra or caracter in digito or caracter == '_'):
                                acumulador += caracter
                                if(acumulador in reservadas):
                                    lexico = "<PRE, " + acumulador + ">"
                                    lexicos.append(lexico)
                                    acumulador = caracter 
                            else:
                                # Condição de parada da classificação de identificadores
                                if(acumulador[0] in letra):
                                    if(acumulador in reservadas):
                                        lexico = "<PRE, " + acumulador + ">"
                                        lexicos.append(lexico)
                                        acumulador = caracter 
                                    else:
                                        if(caracter not in letra or caracter not in digito or caracter != "_" or caracter == " "):
                                            lexico = "<IDE, " + acumulador + ">"
                                            lexicos.append(lexico)
                                            acumulador = caracter
                                        else:
                                            if(acumulador in aritmeticos):
                                                lexico = "<ART, " + acumulador + ">"
                                                lexicos.append(lexico)
                                                acumulador = caracter
                                            else:
                                                if(acumulador in logicos):
                                                    lexico = "<LOG, " + acumulador + ">"
                                                    lexicos.append(lexico)
                                                    acumulador = caracter

                            if(acumulador[0] in delimitadores):
                                lexico = "<IDE, " + acumulador + ">"
                                lexicos.append(lexico)
                                acumulador = ""
                            

def main():
    nome = input("Informe o nome do arquivo: ")
    arquivo = ler_arquivo(nome)        
    analise(arquivo) 
    output = ""   
    for lexico in lexicos:
        print(lexico)
        output += lexico + "\n"
    output += "\n"
    for erro in erros:
        print(erro)
        output += erro + "\n"
    saida = open("files/output/output.txt", "x")

    saida.write(output)
    
if __name__ == "__main__":
    main()