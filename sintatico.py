'''
EXA869 - MI Processadores de Linguagens de Programação
Problema 3 - Analisador Sintático
Discente: Antony Araujo
'''
from lexico import *


def analise_constante(tokens):
    print("chegou aq")
    print(tokens[0])
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] == 'const'):
        if (tokens[1]['token'] == 'DEL' and tokens[1]['valor'] == '{'):
            retorno = verificar_atribuicao_const(tokens[2:])
            if (retorno[0]):
                if (retorno[1][0]['valor'] in tipos):
                    tokens = retorno[1]
                    for i in range(0, len(tokens)):
                        retorno = verificar_atribuicao_const(tokens[0:])
                        if (retorno[0]):
                            if (retorno[1][0]['token'] == 'DEL' and retorno[1][0]['valor'] == '}'):
                                return [True, retorno[1][1:]]
                            else:
                                tokens = retorno[1]
                                continue
                        else:
                            return [False, tokens[0:], tokens[0]['linha'], retorno[3]]
                elif (retorno[1][0]['token'] == 'DEL' and retorno[1][0]['valor'] == '}'):
                    return [True, retorno[1][1:]]
                else:
                    return [False, tokens[0:], tokens[0]['linha'], 'Esperava \'}\'']
        else:
            return [False, tokens[0:], tokens[0]['linha'], 'Esperava \'{\'']
    else:
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava const']


def verificar_atribuicao_const(tokens):
    for i in range(len(tokens)):
        if (tokens[0]['token'] == 'PRE'):
            # Verifica se foi adicionado o tipo à declaração atual de variável
            if (tokens[0]['valor'] in tipos):
                # Altera o inicio da range, removendo o token já verificado anteriormente
                for j in range(1, len(tokens)-2):
                    # Verifica se foi adicionado um identificador
                    if (tokens[j]['token'] == 'IDE'):
                        # ATRIBUICAO MULTIPLA DE VARIAVEL OU DECLARACAO SEM ATRIBUICAO DE VALOR
                        # Verifica se foi adicionado virgula
                        if (tokens[j+1]['token'] == 'DEL'):
                            if (tokens[j+1]['valor'] == ','):
                                if (tokens[j+2]['token'] == 'REL' and tokens[j+2]['valor'] == '='):
                                    return verificar_atribuicao(tokens[j+3:])
                                elif (tokens[j+3]['valor'] == ';'):
                                    return [False, tokens[j+3], tokens[j+3]['linha'], 'Esperava \';\'']
                                else:
                                    j += 2
                                    continue
                            if (tokens[j+2]['valor'] == ';'):
                                return True
                        # ATRIBUICAO UNICA DE VARIAVEL
                        if (tokens[j+1]['token'] == 'REL' and tokens[j+1]['valor'] == '='):
                            return verificar_atribuicao(tokens[j+2:])
                        else:
                            if (tokens[j+1]['valor'] == ';'):
                                return [False, tokens[j+2], tokens[j+2]['linha'], 'Esperava \';\'']
                    j += 2
        i += 1
    return [False, tokens, tokens[0]['linha'], 'Esperava tipo ' + str(tipos)]


def analise_variavel(tokens):
    print("chegou aq")
    print(tokens[0])
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] == 'var'):
        if (tokens[1]['token'] == 'DEL' and tokens[1]['valor'] == '{'):
            retorno = verificar_atribuicao_var(tokens[2:])
            if (retorno[0]):
                if (retorno[1][0]['valor'] in tipos):
                    tokens = retorno[1]
                    for i in range(0, len(tokens)):
                        retorno = verificar_atribuicao_var(tokens[0:])
                        if (retorno[0]):
                            if (retorno[1][0]['token'] == 'DEL' and retorno[1][0]['valor'] == '}'):
                                return [True, retorno[1][1:]]
                            else:
                                tokens = retorno[1]
                                continue
                        else:
                            return [False, tokens[0:], tokens[0]['linha'], retorno[3]]
                elif (retorno[1][0]['token'] == 'DEL' and retorno[1][0]['valor'] == '}'):
                    return [True, retorno[1][1:]]
                else:
                    return [False, tokens[0:], tokens[0]['linha'], 'Esperava \'}\'']
        else:
            return [False, tokens[0:], tokens[0]['linha'], 'Esperava \'{\'']
    else:
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava var']


def verificar_atribuicao_var(tokens):
    for i in range(len(tokens)):
        if (tokens[0]['token'] == 'PRE'):
            # Verifica se foi adicionado o tipo à declaração atual de variável
            if (tokens[0]['valor'] in tipos):
                # Altera o inicio da range, removendo o token já verificado anteriormente
                for j in range(1, len(tokens)-2):
                    # Verifica se foi adicionado um identificador
                    if (tokens[j]['token'] == 'IDE'):
                        # ATRIBUICAO MULTIPLA DE VARIAVEL OU DECLARACAO SEM ATRIBUICAO DE VALOR
                        # Verifica se foi adicionado virgula
                        if (tokens[j+1]['token'] == 'DEL'):
                            if (tokens[j+1]['valor'] == ','):
                                if (tokens[j+2]['token'] == 'REL'):
                                    if (tokens[j+2]['valor'] == '='):
                                        return verificar_atribuicao(tokens[j+3:])
                                else:
                                    j += 2
                                    continue
                            if (tokens[j+2]['valor'] == ';'):
                                return True
                        # ATRIBUICAO UNICA DE VARIAVEL
                        if (tokens[j+1]['token'] == 'REL'):  # Verifica se foi adicionado '='
                            if (tokens[j+1]['valor'] == '='):
                                return verificar_atribuicao(tokens[j+2:])
                    j += 2
        i += 1
    return [False, tokens, tokens[0]['linha'], 'Esperava tipo ' + str(tipos)]


def verificar_atribuicao(tokens):
    print("CHEGA ATR")
    verificado = verificar_aritmetica(tokens[0:])
    if (verificado[0]):
        tokens = verificado[1]
        if (tokens[0]['valor'] == ";"):
            return [True, tokens[1:]]
        else:
            return [False, tokens[4:], tokens[4]['linha'], 'Esperava \';\'']
    verificado = verificar_logica(tokens[0:])
    if (verificado[0]):
        tokens = verificado[1]
        if (tokens[0]['valor'] == ";"):
            return [True, tokens[1:]]
        else:
            return [False, tokens[0:], tokens[0]['linha'], 'Esperava \';\'']
    else:
        print("correta atribuição")
        print(tokens[0])
        if (tokens[0]['token'] in ['IDE', 'NRO', 'CAC', 'DEL']):
            if (tokens[1]['valor'] == ';'):
                return [True, tokens[2:]]
            elif (tokens[0]['valor'] == '['):
                print("chegou cá")
                for token in range(1, len(tokens), 2):
                    if (tokens[token]['token'] in ['NRO', 'IDE', 'CAC', 'DEL']):
                        if (tokens[token+1]['valor'] == ']'):
                            if (tokens[token+2]['valor'] == ";"):
                                print("chega em quei")
                                return [True, tokens[token+3:]]
                        elif (tokens[token+1]['valor'] == ','):
                            continue
                if (tokens[0]['valor'] == ']'):
                    return [True, tokens]
                else:
                    pass
        else:
            return [False, tokens[0:], tokens[0]['linha'], 'Esperava IDE, NRO, CAC ou \'[\' \']\'']
    return [False, tokens[0:], tokens[0]['linha'], 'Esperava IDE, NRO, CAC ']


def verificar_struct(tokens):
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] == 'struct'):
        if (tokens[1]['token'] == 'IDE'):
            if (tokens[2]['token'] == 'DEL' and tokens[2]['valor'] == '{'):
                retorno = verificar_atribuicoes_struct(tokens[3:])
                if (retorno[1][0]['token'] == 'DEL' and retorno[1][0]['valor'] == '}'):
                    return [True, retorno[1][1:]]
                else:
                    return [False, retorno[1][0:], retorno[1][0]['linha'], 'Esperava \'}\'']
            else:
                return [False, tokens[2:], tokens[2]['linha'], 'Esperava \'{\'']
        else:
            return [False, tokens[1:], tokens[1]['linha'], 'Esperava IDE']
    else:
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava struct']
    return [False, tokens[0:], tokens[0]['linha'], 'Esperava IDE, NRO, CAC ']


def verificar_condicional(tokens):
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] == 'if'):
        if (tokens[1]['token'] == 'DEL' and tokens[1]['valor'] == '('):
            retorno = verificar_logica(tokens[2:])
            if (retorno[0]):
                if (retorno[1][0]['token'] == 'DEL' and retorno[1][0]['valor'] == ')'):
                    if (retorno[1][1]['token'] == 'PRE' and retorno[1][1]['valor'] == 'then'):
                        if (retorno[1][2]['token'] == 'DEL' and retorno[1][2]['valor'] == '{'):
                            retorno = bloco_if(
                                retorno[1][3:])
                            if (retorno[1][0]['valor'] == '}'):
                                return [True, retorno[1][1:]]
                            else:
                                return [False, retorno[1], retorno[1][0]['linha'], 'Esperado \'}\'']
            else:
                return retorno
    else:
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava if']
    return [False, tokens[0:], tokens[0]['linha'], 'Esperado \'}\'']


def verificar_loop(tokens):
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] == 'while'):
        if (tokens[1]['token'] == 'DEL' and tokens[1]['valor'] == '('):
            retorno = verificar_logica(tokens[2:])
            if (retorno[0]):
                if (retorno[1][0]['token'] == 'DEL' and retorno[1][0]['valor'] == ')'):
                    if (retorno[1][1]['token'] == 'DEL' and retorno[1][1]['valor'] == '{'):
                        retorno = bloco_expressoes(
                            retorno[1][2:])
                        if (retorno[1][0]['valor'] == '}'):
                            return [True, retorno[1][1:]]
                        else:
                            return [False, retorno[1], retorno[1][0]['linha'], 'Esperado \'}\'']
            else:
                return retorno
    else:
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava if']
    return [False, tokens[0:], tokens[0]['linha'], 'Esperado \'}\'']


def verificar_expressao_logica(tokens):
    if (tokens[0]['token'] == 'PRE'):
        if (tokens[0]['valor'] == 'true' or tokens[0]['valor'] == 'false'):
            if (tokens[1]['token'] == 'DEL'):
                if (tokens[1]['valor'] == ')' or tokens[1]['valor'] == ';'):
                    return [True, tokens[1:]]
    if (tokens[0]['token'] == 'NRO' or tokens[0]['token'] == 'IDE'):
        if (tokens[1]['token'] == "LOG"):
            return verificar_logica(tokens[2:])
        if (tokens[1]['valor'] == ')'):
            return [True, tokens[1:]]
    if (tokens[0]['valor'] == ')'):
        return [True, tokens[0:]]
    return [False, tokens]

# Verifica expressão lógica


def verificar_logica(tokens):
    for i in range(0, len(tokens), 2):
        print("i = " + str(i), "valor = " + str(tokens[i]['valor']))
        print("i+1 = " + str(i+1) + "valor = " + str(tokens[i+1]['valor']))
        print("i+2 = " + str(i+2) + "valor = " + str(tokens[i+2]['valor']))
        if (tokens[i]['token'] == 'NRO' or tokens[i]['token'] == 'IDE' or tokens[i]['token'] == 'PRE'):
            if (tokens[i]['token'] == 'PRE'):
                if (tokens[i]['valor'] != 'true' and tokens[i]['valor'] != 'false'):
                    return [False, tokens[i], tokens[i]['linha'], 'Expressão inválida)']
            if (tokens[i+1]['token'] == 'REL'):
                tokens = verificar_relacional(tokens[i:])[1]
                print("chega log " + str(tokens[i]))
            if (tokens[i+1]['token'] == 'LOG' or tokens[i+1]['valor'] == ')'):
                if (tokens[i+1]['valor'] == ')'):
                    return [True, tokens[i+1:]]
                else:
                    if (tokens[i+2]['valor'] != ')' and tokens[i+2]['token'] != 'LOG'):
                        return verificar_logica(tokens[i+2:])
                    else:
                        if (tokens[i+1]['token'] == 'REL'):
                            tokens = verificar_relacional(tokens[i:])[1]
                        else:
                            return [False, tokens[i+1], tokens[i+i]['linha'], 'Esperado NRO, IDE, true ou false']
            else:
                return [False, tokens[i+1], tokens[i+i]['linha'], 'Esperado LOG ou )']
        else:
            if (tokens[i]['valor'] == ')'):
                return [True, tokens[i:], tokens[i]['linha']]
            else:
                return [False, tokens[i], tokens[i]['linha'], 'Esperado NRO, IDE, true ou false']
    return [False, tokens, -1, 'Expressão lógica incorreta']

# realiza a verificacao de uma expressao aritmetica (ART)


def expressao_base(tokens):
    if (tokens[0]['token'] in ['NRO', 'IDE']):
        if (tokens[1]['token'] == 'ART'):
            if (tokens[2]['token'] in ['NRO', 'IDE']):
                return [True, tokens[3:]]
            else:
                return [False, tokens, tokens[2]['linha'], 'Esperava NRO ou IDE']
        else:
            return [False, tokens, tokens[1]['linha'], 'Esperava ' + str(aritmeticos)]
    else:
        return [False, tokens, tokens[0]['linha'], 'Esperava NRO ou IDE']


def expressao_secundaria(tokens):
    if (tokens[0]['token'] == 'ART'):
        if (tokens[1]['token'] in ['NRO', 'IDE']):
            return [True, tokens[2:]]
        else:
            # Pode ser uma expressão numérica ()
            return [False, tokens, tokens[1]['linha'], 'Esperava NRO ou IDE']
    else:
        return [False, tokens, tokens[0]['linha'], 'Esperava ' + str(aritmeticos)]


def verificar_aritmetica(tokens):
    if (tokens[0]['token'] in ['NRO', 'IDE']):
        expressao = expressao_base(tokens)
        if (expressao[0]):
            tokens = expressao[1]
            if (tokens[0]['token'] == 'ART'):
                if (tokens[1]['token'] in ['NRO', 'IDE'] or tokens[1]['valor'] == '('):
                    expressao = verificar_aritmetica(tokens[1:])
                    if (expressao[0]):
                        return [True, expressao[1]]
                    else:
                        tokens = expressao[1]
                        return [False, tokens, tokens[0]['linha'], 'Esperava NRO, IDE ou \'(\'']
                else:
                    return [False, tokens[1:], tokens[1]['linha'], 'Esperava NRO ou IDE']
            else:
                return [True, tokens]
        else:
            if (expressao[1][0]['token'] in ['NRO', 'IDE'] and expressao[1][1]['valor'] == ';'):
                return [True, expressao[1][1:]]
            elif (expressao[1][0]['token'] in ['NRO', 'IDE'] and expressao[1][1]['token'] == 'ART'):
                if (expressao[1][2]['valor'] == '('):
                    return verificar_aritmetica(expressao[1][2:])
    elif (tokens[0]['valor'] == '('):
        expressao = verificar_aritmetica(tokens[1:])
        if (expressao[0]):
            tokens = expressao[1]
            if (tokens[0]['valor'] == ')'):
                if (tokens[1]['token'] == 'ART' and tokens[2]['token'] in ['NRO', 'IDE']):
                    expressao = verificar_aritmetica(tokens[2:])
                    if (expressao[0]):
                        return [True, expressao[1]]
                    else:
                        return [False, expressao[1], expressao[1][0]['linha'], 'Esperava \')\'']
                else:
                    return [True, tokens[1:]]
            else:
                return [False, tokens, tokens[0]['linha'], 'Esperava \')\'']
    elif (tokens[0]['valor'] == ';'):
        return [True, tokens]
    else:
        return [False, tokens, tokens[0]['linha'], 'Esperava NRO, IDE ou \'(\'']
    return [False, tokens, tokens[0]['linha'], 'Esperava expressão aritmetica']


# realiza a verificao de uma condicao relacional
def termo_relacional(tokens):
    if (tokens[0]['token'] in ['NRO', 'IDE']):
        if (tokens[1]['token'] == 'REL'):
            if (tokens[2]['token'] in ['NRO', 'IDE']):
                return [True, tokens[3:]]
            else:
                return [False, tokens, tokens[2]['linha'], 'Esperava NRO ou IDE']
        else:
            return [False, tokens, tokens[1]['linha'], 'Esperava ' + str(relacionais)]
    else:
        return [False, tokens, tokens[0]['linha'], 'Esperava NRO ou IDE']


def verificar_relacional(tokens):
    print("PRIMERIO: " + str(tokens[0]))
    if (tokens[0]['token'] == 'NRO' or tokens[0]['token'] == 'IDE' or tokens[0]['token'] == 'PRE'):
        if (tokens[0]['token'] == 'PRE'):
            if (tokens[0]['valor'] != 'true' and tokens[0]['valor'] != 'false'):
                return [False, tokens[0:], tokens[0]['linha'], 'Expressão inválida)']
        if (tokens[1]['token'] == 'REL'):
            if (tokens[2]['token'] == 'NRO' or tokens[2]['token'] == 'IDE' or tokens[2]['token'] == 'PRE'):
                if (tokens[2]['token'] == 'PRE'):
                    if (tokens[2]['valor'] != 'true' and tokens[2]['valor'] != 'false'):
                        return [False, tokens[2:], tokens[2]['linha'], 'Expressão inválida)']
                return [True, tokens[2:]]
            else:
                return [False, tokens[2:], tokens[2]['linha'], 'Esperado NRO, IDE, true ou false']
        else:
            return [False, tokens[1:], tokens[1]['linha'], 'Esperando ' + str(relacionais[:-1])]
    else:
        if (tokens[0]['valor'] == '('):
            termo = termo_relacional(tokens[0])
            if (termo[0]):
                if (termo[1][0]['valor'] == ')'):
                    return [True, termo[1][1:]]

    return [False, tokens[2:], tokens[2]['linha'], 'Esperado NRO, IDE, true ou false']


def verificar_expressao(tokens):
    expressao_aritmetica = verificar_aritmetica(tokens[0:])
    expressao_logica = verificar_expressao_logica(tokens[0:])
    if (expressao_aritmetica[0] or expressao_logica[0]):
        if (expressao_aritmetica[0]):
            tokens = expressao_aritmetica[1]
        elif (expressao_logica[0]):
            tokens = expressao_logica[1]
        if (tokens[0]['token'] == 'LOG'):
            expressao = verificar_expressao(tokens[1:])
            return expressao
        if (expressao_aritmetica[0]):
            return expressao_aritmetica
        elif (expressao_logica[0]):
            return expressao_logica
        elif (tokens[0]['token'] == 'DEL' and tokens[0]['valor'] == ';'):
            return [True, tokens[1:]]
        else:
            return [False, tokens[0:], tokens[0]['linha'], 'Esperava \';\'']
    else:
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava expressão relacional, lógica ou aritmética']


def verificar_atribuicoes_struct(tokens):
    if (tokens[0]['token'] in ['PRE', 'IDE']):
        # <struct_var> ::= tipo <struct_aux> <struct_var>
        # <struct_aux> ::= ide <struct2> | <vetor> <struct2> | <matriz> <struct2>
        # <struct2> ::= ',' <struct_aux> |  ';'
        if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] in tipos):
            if (tokens[1]['token'] == 'IDE'):
                if (tokens[2]['valor'] == ';'):
                    print("chegou no ; inicial")
                    return [True, tokens[3:]]
                else:
                    for j in range(2, len(tokens)-1):
                        if (tokens[j]['token'] == 'DEL' and tokens[j]['valor'] == ','):
                            if (tokens[j+1]['token'] == 'IDE'):
                                continue
                            else:
                                return [False, tokens[0:], tokens[0]['linha'], 'Esperava IDE']
                        if (tokens[j]['valor'] == ';'):
                            print("chegou no ; final")
                            return [True, tokens[j+1:]]
# Automato de verificacao de print()


def verificar_print(tokens):
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] == 'print'):
        if (tokens[1]['valor'] == '('):
            if (tokens[2]['token'] == 'CAC'):
                if (tokens[3]['valor'] == ')'):
                    if (tokens[4]['valor'] == ';'):
                        return [True, tokens[5:]]
                    else:
                        return [False, tokens[4:], tokens[4]['linha'], 'Esperava \';\'']
                else:
                    return [False, tokens[3:], tokens[3]['linha'], 'Esperava \')\'']
            else:
                return [False, tokens[2:], tokens[2]['linha'], 'Esperava cadeia de caracteres']
        else:
            return [False, tokens[1:], tokens[1]['linha'], 'Esperava \'(\'']
    else:
        return [False, tokens, tokens[0]['linha'], 'Esperava print']

# Automato de verificacao de read()


def verificar_read(tokens):
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] == 'read'):
        if (tokens[1]['valor'] == '('):
            if (tokens[2]['token'] == 'IDE'):  # Pode ser IDE, matriz[1][1] ou vetor[2]
                if (tokens[3]['valor'] == ')'):
                    if (tokens[4]['valor'] == ';'):
                        return [True, tokens[5:]]
                    else:
                        return [False, tokens[1:], tokens[1]['linha'], 'esperava \';\'']
                else:
                    return [False, tokens[1:], tokens[1]['linha'], 'esperava \')\'']
        else:
            return [False, tokens[1:], tokens[1]['linha'], 'esperava \'(\'']
    else:
        return [False, tokens, tokens[0]['linha'], 'Esperava read']
# Verificacao de Funcao


def verificar_parametros(tokens):
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] in tipos):
        if (tokens[1]['token'] == 'IDE'):
            if (tokens[2]['token'] == 'DEL' and tokens[2]['valor'] == ','):
                return verificar_parametros(tokens[3:])
            elif (tokens[2]['token'] == 'DEL' and tokens[2]['valor'] == ')'):
                return [True, tokens[3:]]
            else:
                return [False, tokens[2:], tokens[2]['linha'], 'Esperava \'(\' ou \',\'']
        else:
            return [False, tokens[1:], tokens[1]['linha'], 'Esperava \')\'']
    else:
        if (tokens[0]['token'] == 'DEL' and tokens[0]['valor'] == ')'):
            return [True, tokens[1:]]
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava ' + str(tipos)]


def verificar_funcao(tokens):
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] == 'function'):
        if (tokens[1]['token'] == 'DEL' and tokens[1]['valor'] == '('):
            retorno_parametros = verificar_parametros(tokens[2:])
            if (retorno_parametros[0]):
                tokens = retorno_parametros[1]
                if (tokens[0]['token'] == 'DEL' and tokens[0]['valor'] == '{'):
                    retorno_bloco = bloco_expressoes(tokens[1:])
                    if (retorno_bloco[0]):
                        tokens = retorno_bloco[1]
                        if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] == 'return'):
                            retorno_logico = verificar_expressao(
                                tokens[1:])
                            if (retorno_logico[0]):
                                tokens = retorno_logico[1]
                                if (tokens[0]['token'] == 'DEL' and tokens[0]['valor'] == ';'):
                                    if (tokens[1]['token'] == 'DEL' and tokens[1]['valor'] == '}'):
                                        return [True, tokens[2:]]
                                    else:
                                        return [False, tokens[1:], tokens[0]['linha'], 'Esperava \'}\'']
                                else:
                                    return [False, tokens[0:], tokens[0]['linha'], 'Esperava \';\'']
                            else:
                                return [False, tokens[0:], tokens[0]['linha'], 'Esperava expressão lógica']
                        else:
                            return [False, tokens[0:], tokens[0]['linha'], 'Esperava return']
                    else:
                        return retorno_bloco
                else:
                    return [False, tokens[0:], tokens[0]['linha'], 'Esperava \'{\'']
            else:
                return retorno_parametros
        else:
            return [False, tokens[1:], tokens[0]['linha'], 'Esperava \'(\'']
    else:
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava function']

# Verificacao de procedures


def verificar_procedure(tokens):
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] == 'procedure'):
        if (tokens[1]['token'] == 'DEL' and tokens[1]['valor'] == '('):
            retorno_parametros = verificar_parametros(tokens[2:])
            if (retorno_parametros[0]):
                tokens = retorno_parametros[1]
                if (tokens[0]['token'] == 'DEL' and tokens[0]['valor'] == '{'):
                    retorno_bloco = bloco_expressoes(tokens[1:])
                    if (retorno_bloco[0]):
                        tokens = retorno_bloco[1]
                        if (tokens[0]['token'] == 'DEL' and tokens[0]['valor'] == '}'):
                            return [True, tokens[1:]]
                        else:
                            return [False, tokens[0:], tokens[0]['linha'], 'Esperava \'}\'']
                    else:
                        return retorno_bloco
                else:
                    return [False, tokens[0:], tokens[0]['linha'], 'Esperava \'{\'']
            else:
                return retorno_parametros
        else:
            return [False, tokens[1:], tokens[0]['linha'], 'Esperava \'(\'']
    else:
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava function']


def bloco_expressoes(tokens):
    print("BLOCO expressões")
    # print(tokens[0])
    # if
    expressao = verificar_condicional(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # while
    expressao = verificar_loop(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # struct
    expressao = verificar_struct(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # print
#    print("CHEGA NO PRINT" + str(tokens[0]))
    expressao = verificar_print(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # read
    expressao = verificar_read(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # function
    expressao = verificar_funcao(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # procedure
    expressao = verificar_procedure(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # var
    expressao = analise_variavel(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # atribuicao
    print(tokens[0])
    if (tokens[0]['token'] == 'IDE'):
        if (tokens[1]['valor'] == '='):
            expressao = verificar_atribuicao(tokens[2:])
            if (expressao[0]):
                tokens = expressao[1]

    if (expressao[0]):
        return expressao
    else:
        return [False, expressao[1], expressao[2], 'Esperava if, while, struct, print, read, function, procedure, var ou atribuição']


def bloco_if(tokens):
    retorno = [True, tokens]
    for i in range(0, len(tokens)):
        expressao = bloco_expressoes(tokens)
        if (expressao[0]):
            tokens = expressao[1]
            if (tokens[0]['valor'] == '}'):
                retorno = expressao
                break
            continue
        else:
            retorno = expressao
            break
    return retorno


def bloco_start(tokens, coringa):
    retorno = [True, tokens]
    for i in range(0, len(tokens)):
        expressao = bloco_expressoes(tokens)
        if (expressao[0]):
            tokens = expressao[1]
            if (tokens[0]['valor'] == coringa):
                retorno = expressao
                break
            continue
        else:
            retorno = expressao
            break
    return retorno


def bloco_expressoes_globais(tokens):
    if (tokens[0]['valor'] == 'start'):
        expressao = [True, tokens]
        return [True, tokens]
    # struct
    expressao = verificar_struct(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # function
    expressao = verificar_funcao(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # procedure
    expressao = verificar_procedure(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # var
    expressao = analise_variavel(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    # const
    expressao = analise_constante(tokens[0:])
    if (expressao[0]):
        tokens = expressao[1]
        return [True, tokens]

    return expressao


def bloco_global(tokens):
    retorno = [True, tokens]
    print("----------------------")
    print(tokens[0])
    print("----------------------")
    if (tokens[0]['valor'] not in ['const', 'var', 'procedure', 'function', 'start']):
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava const, var, procedure, function, struct']

    for i in range(0, len(tokens)):
        expressao = bloco_expressoes_globais(tokens)
        if (expressao[0]):
            tokens = expressao[1]
            retorno = expressao
            return retorno
        else:
            retorno = expressao
            break
    return retorno


def sintatico(lista_tokens):
    tokens = varredura_tokens(lista_tokens)

    # GLOBAL
    expressao = bloco_global(tokens)
    if (expressao[0]):
        tokens = expressao[1]
    else:
        return expressao
    # START
    if (tokens[0]['token'] == 'PRE' and tokens[0]['valor'] in ['start', 'function', 'procedure', 'const', 'var', 'structure']):
        if (tokens[0]['valor'] == 'start'):
            if (tokens[1]['token'] in ['DEL'] and tokens[1]['valor'] in ['(']):
                if (tokens[2]['token'] in ['DEL'] and tokens[2]['valor'] in [')']):
                    if (tokens[3]['token'] in ['DEL'] and tokens[3]['valor'] in ['{']):
                        tokens = tokens[4:]
                        print("VERIFICA ATUAL: " + str(tokens[0]))
                        expressao = bloco_start(tokens, "}")
                        if (expressao[0]):
                            tokens = expressao[1]
                        else:
                            return expressao
                    else:
                        return [False, tokens[0:], tokens[0]['linha'], 'Esperava \'{\'']
                    if (tokens[0]['valor'] == '}'):
                        return [True, tokens]
                    else:
                        return [False, tokens[0:], tokens[0]['linha'], 'Esperava \'}\'']
                else:
                    return [False, tokens[0:], tokens[0]['linha'], 'Esperava \')\'']
            else:
                return [False, tokens[0:], tokens[0]['linha'], 'Esperava \'(\'']
        else:
            return [False, tokens[0:], tokens[0]['linha'], 'Esperava start']
    else:
        return [False, tokens[0:], tokens[0]['linha'], 'Esperava ' + str(['start', 'function', 'procedure', 'const', 'var', 'structure'])]
