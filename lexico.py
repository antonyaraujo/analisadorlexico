'''
EXA869 - MI Processadores de Linguagens de Programação
Problema 1 - Analisador Léxico
Discente: Antony Araujo
'''

digito = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letra = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
         "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",]
delimitadores = [";", ",", "(", ")", "[", "]", "{", "}", "."]
reservadas = ["var", "const", "struct", "procedure", "function", "start", "return", "if",
              "else", "then", "while", "read", "print", "int", "real", "boolean", "string", "true", "false"]
aritmeticos = ["+", "-", "/", "*", "++", "--"]
relacionais = ["!=", "==", "<", "<=", ">", ">=", "="]
logicos = ["!", "&&", "||"]
espaco = [" ", "\t", "  "]

tipos = ["int", "real", "boolean", "string"]

# Analisador token


tabela_ascii = []
for i in range(32, 126):
    tabela_ascii.append(chr(i))
tabela_ascii.pop(2)
tabela_ascii.append(chr(9))


def adicionar_token(tokens, linha, sigla, lexema):
    token = str(linha).zfill(2) + " " + sigla + " " + lexema
    tokens.append(token)


def adicionar_erro(erros, linha, sigla, lexema):
    erro = str(linha).zfill(2) + " " + sigla + " " + lexema
    erros.append(erro)


def analisa_caracter(linha, inicial, tokens, erros, contagem_linha):
    # Percorre caracter a caracter da linha
    acumulador = inicial
    for caracter in linha:
        # print("CARACTER: " + caracter)
        if (caracter == "\n"):
            if (len(acumulador) > 1):
                if (acumulador[0] == "/" and acumulador[1] == "*"):
                    inicial = acumulador
                    continue

        # Adiciona o caracter ao acumulador
        acumulador += caracter
        # verifica se o caracter inicial do lexema é válido
        if (acumulador[0] in tabela_ascii or acumulador[0] != "\""):
            # Classifica delimitadores de comentário
            if (acumulador[0] == "/"):
                if (len(acumulador) > 1):
                    if (acumulador[1] == "*"):  # É um comentário em bloco
                        # Verifica se o comentário em bloco foi fechado
                        if (caracter == "\n"):
                            continue
                        if (acumulador[-1] == "/" and acumulador[-2] == "*"):
                            adicionar_token(
                                tokens, contagem_linha, "CoM", acumulador)
                            acumulador = ""
                        elif (acumulador[len(acumulador)-1] == "/" and acumulador[len(acumulador)-2] == "*"):
                            adicionar_token(
                                tokens, contagem_linha, "CoM", acumulador)
                            acumulador = ""
                        else:
                            continue
                        continue
                    else:  # se for um comentário em linha
                        if (acumulador[1] == "/"):
                            continue
                        else:
                            # Classifica a barra como operador aritmético e parte para o próximo estado
                            adicionar_token(
                                tokens, contagem_linha, "ART", acumulador[0])
                            acumulador = acumulador[1:]
            else:
                # Classifica delimitadores
                # print("chega aqui: " + acumulador)
                if (acumulador[0] == "/" and acumulador[1] == "*"):
                    continue
                if (acumulador[0] in delimitadores):
                    adicionar_token(tokens, contagem_linha,
                                    "DEL", acumulador[0])
                    acumulador = acumulador[1:]
                else:
                    # Verifica espaço e tab e separa
                    if (acumulador[0] == "\t" or acumulador[0] in espaco):
                        acumulador = acumulador[1:]
                        next
                    else:
                        # Classifica numeros
                        if (acumulador[0] in digito or acumulador[0] == '-' or acumulador[0] in espaco):
                            print("caractere", caracter)
                            print("acumulador", acumulador)

                            # Verificar ponto no número
                            if (acumulador[0] == "-"):  # É um número negativo
                                if (len(acumulador) > 1):
                                    if (caracter == "."):
                                        print("chega aqui")
                                        if (acumulador[:-1].find('.') != -1):
                                            adicionar_erro(
                                                erros, contagem_linha, "NMF", acumulador[:-1])
                                            acumulador = ""
                                    else:
                                        if (caracter == '-'):
                                            if (len(acumulador) == 2):
                                                if (acumulador[len(acumulador)-2] == "-"):
                                                    adicionar_token(
                                                        tokens, contagem_linha, "ART", acumulador)
                                                    acumulador = ""
                                            else:
                                                if (acumulador[len(acumulador)-2] == "-"):
                                                    adicionar_token(
                                                        tokens, contagem_linha, "ART", acumulador)
                                                    acumulador = caracter
                                        else:
                                            if (caracter not in digito):
                                                if (acumulador[len(acumulador)-2] in digito):
                                                    adicionar_token(
                                                        tokens, contagem_linha, "NRO", acumulador[:-1])
                                                    acumulador = caracter
                                                else:
                                                    if (acumulador[len(acumulador)-1] in digito and acumulador[len(acumulador)-2 == "-"]):
                                                        adicionar_token(
                                                            tokens, contagem_linha, "ART", acumulador[:-1])
                                                        acumulador = acumulador[len(
                                                            acumulador)-1]
                                                    else:
                                                        print(
                                                            "segue um caso ##")
                                                        print(acumulador)
                                                        adicionar_token(
                                                            tokens, contagem_linha, "ART", acumulador[:-1])
                                                        acumulador = caracter
                                            else:
                                                if (len(acumulador) > 2):
                                                    if (caracter != "-"):
                                                        adicionar_token(
                                                            tokens, contagem_linha, "NRO", acumulador[:-2])
                                                        adicionar_token(
                                                            tokens, contagem_linha, "ART", acumulador[len(acumulador)-2])
                                                        acumulador = acumulador[len(
                                                            acumulador)-1]
                                                    else:
                                                        if (acumulador[len(acumulador)-2] in digito):
                                                            adicionar_token(
                                                                tokens, contagem_linha, "NRO", acumulador[:-1])
                                                            acumulador = caracter
                                                        else:
                                                            if (acumulador[len(acumulador)-2] == "-"):
                                                                adicionar_token(
                                                                    tokens, contagem_linha, "NRO", acumulador[:-2])
                                                                adicionar_token(
                                                                    tokens, contagem_linha, "ART", "--")
                                                                acumulador = ""

                            else:  # Número positivo
                                if (acumulador[0] in digito):
                                    if (caracter not in digito or caracter not in espaco):
                                        if (caracter == "."):
                                            if (acumulador[:-1].find('.') != -1):
                                                if (acumulador[len(acumulador)-2] in digito):
                                                    adicionar_token(
                                                        tokens, contagem_linha, "NRO", acumulador[:-1])
                                                else:
                                                    adicionar_erro(
                                                        erros, contagem_linha, "NMF", acumulador[:-1])
                                                acumulador = caracter
                                            else:
                                                next
                                        else:
                                            if (caracter not in digito):
                                                if (acumulador[len(acumulador)-2] in digito):
                                                    adicionar_token(
                                                        tokens, contagem_linha, "NRO", acumulador[:-1])
                                                else:
                                                    adicionar_erro(
                                                        erros, contagem_linha, "NMF", acumulador[:-1])
                                                acumulador = caracter
                                                next
                                    else:
                                        if (caracter == "."):
                                            print("")
                                else:
                                    if (acumulador[0] in espaco):
                                        if (caracter not in espaco):
                                            acumulador = acumulador[:-1]
                        else:
                            # Classifica operadores aritmeticos
                            if (acumulador[0] in aritmeticos):
                                if (acumulador[0] in aritmeticos and (caracter != "+" or caracter != "-")):
                                    adicionar_token(
                                        tokens, contagem_linha, "ART", acumulador[:-1])
                                    acumulador = caracter
                                else:
                                    if (acumulador in aritmeticos):
                                        adicionar_token(
                                            tokens, contagem_linha, "ART", acumulador)
                                        acumulador = ""
                            else:
                                if (acumulador[0] == "!"):
                                    if (acumulador == "!="):
                                        adicionar_token(
                                            tokens, contagem_linha, "REL", acumulador)
                                        acumulador = ""
                                    else:
                                        adicionar_token(
                                            tokens, contagem_linha, "LOG", acumulador[0])
                                        acumulador = acumulador[1:]
                                else:
                                    # Classifica operadores relacionais
                                    if (acumulador[0] in relacionais):
                                        if (acumulador[0] == "<" or acumulador[0] == ">" or acumulador[0] == "="):
                                            if (caracter not in relacionais):
                                                adicionar_token(
                                                    tokens, contagem_linha, "REL", acumulador[:-1])
                                                acumulador = caracter
                                            else:
                                                next
                                        else:
                                            if (acumulador in relacionais):
                                                adicionar_token(
                                                    tokens, contagem_linha, "REL", acumulador)
                                                acumulador = ""
                                    else:
                                        # Classifica operadores lógicos
                                        if (acumulador[0] == "&" or acumulador[0] == "|"):
                                            if (acumulador in logicos):
                                                adicionar_token(
                                                    tokens, contagem_linha, "LOG", acumulador)
                                                acumulador = ""
                                            else:
                                                next
                                        else:
                                            # Classifica identificadores
                                            if (acumulador[0] in letra):
                                                # Classifica palavras reservadas
                                                if (acumulador in reservadas):
                                                    adicionar_token(
                                                        tokens, contagem_linha, "PRE", acumulador)
                                                    acumulador = ""
                                                else:
                                                    if (caracter not in letra and caracter not in digito and caracter != "_" and caracter not in espaco):
                                                        adicionar_token(
                                                            tokens, contagem_linha, "IDE", acumulador[:-1])
                                                        acumulador = caracter
                                                    else:
                                                        if (caracter in espaco):
                                                            if (acumulador[0] == "/"):
                                                                next
                                                            else:
                                                                adicionar_token(
                                                                    tokens, contagem_linha, "IDE", acumulador[:-1])
                                                                acumulador = caracter

                                            else:
                                                # Token mal formado
                                                # print("ERRO: ", acumulador)
                                                if (acumulador != "\n"):
                                                    erro = str(contagem_linha).zfill(
                                                        2) + " TMF " + acumulador[:-1]
                                                    erros.append(erro)
                                                    acumulador = caracter
        else:
            # verifica se é uma cadeia de caracteres
            if (acumulador[0] == "\""):
                if (len(acumulador) > 1):
                    if (caracter == "\""):
                        validacao = True
                        for value in acumulador:
                            if (value not in tabela_ascii and value != "\"" and value != "\'"):
                                validacao = False
                        if (validacao):
                            adicionar_token(
                                tokens, contagem_linha, "CAC", acumulador)
                            acumulador = ""
                        else:
                            erro = str(contagem_linha).zfill(
                                2) + " CMF " + acumulador
                            erros.append(erro)
                            acumulador = ""
                    else:
                        if (caracter == ";"):
                            erro = str(contagem_linha).zfill(
                                2) + " CMF " + acumulador
                            erros.append(erro)
                            acumulador = ""
                        else:
                            if (caracter == "\n"):
                                print("CHEGOU cá")
                                print("ultimo: " + acumulador)
                                acumulador = acumulador[:-1]
                                print("ultimo: " + acumulador)
                                erro = str(contagem_linha).zfill(
                                    2) + " CMF " + acumulador
                                erros.append(erro)
                                acumulador = ""
                            else:
                                continue

            else:
                # Se o caracter não é válido (de 32 a 126 a tabela ASCII, com excecao do 34 e acrescimo do caracter de tab (9))
                print("FINAL CUM: " + acumulador)
                if (len(acumulador) >= 4):
                    if (acumulador[-2] != "*" and acumulador[-1] != "/"):
                        adicionar_erro(erros, contagem_linha,
                                       'CoMF', acumulador)
                    else:
                        if (caracter != "\n"):
                            erro = str(contagem_linha).zfill(
                                2) + " TMF " + acumulador
                            erros.append(erro)
                            acumulador = ""
                else:
                    if (caracter != "\n"):
                        erro = str(contagem_linha).zfill(
                            2) + " TMF " + acumulador
                        erros.append(erro)
                    acumulador = ""


def analise(arquivo):
    erros = []
    tokens = []
    acumulador = ""
    contagem_linha = 0
    for linha in arquivo:
        contagem_linha += 1
        # corrigida = linha.replace("\n", " ")
        corrigida = linha
        # Verifica se há um comentário
        if (len(acumulador) > 1):
            if (acumulador[0] == "/" and acumulador[1] == "/"):
                adicionar_token(tokens, contagem_linha, "CoM", acumulador)
                acumulador = ""
        analisa_caracter(
            corrigida, acumulador, tokens, erros, contagem_linha)
    if (len(acumulador) != 0):
        if (acumulador[0] == "\""):
            adicionar_erro(erros, contagem_linha, "CMF", acumulador)
            acumulador = ""
        else:
            if (len(acumulador) > 1):
                if (acumulador[0] == "/" and acumulador[1] == "*"):
                    adicionar_erro(erros, contagem_linha, "CoMF", acumulador)
                    acumulador = ""

    return [tokens, erros]


def varredura_tokens(lista_tokens):
    lista = []
    for tk in lista_tokens:
        if (tk[3:6] != "CoM"):
            lista.append(
                {'token': tk[3:6], 'valor': tk[7:], 'linha': tk.split(" ")[0]})
    return lista
