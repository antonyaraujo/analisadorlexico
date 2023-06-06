'''
EXA869 - MI Processadores de Linguagens de Programação
Problema 3 - Analisador Sintático
Discente: Antony Araujo
'''

import os
from lexico import *
from sintatico import *


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

    arquivo = open("files/output/" +
                   caminho_arquivo.replace(".txt", "")+'-saida.txt', 'w')
    arquivo.write(buffer)


def escrever_arquivo_sintatico(caminho_arquivo, erros, tokens):
    buffer = ""
    for token in tokens:
        buffer += token + "\n"

    buffer += "\n"

    buffer += "\n"

    buffer += erros + "\n"

    arquivo = open("files/output/" +
                   caminho_arquivo.replace(".txt", "")+'-saida.txt', 'w')
    arquivo.write(buffer)


def print_erro(erro, debug, arquivo, tokens):
    print("chegou cá")
    erro = "Ocorreu um erro na linha " + \
        str(erro[2]) + ". " + erro[3] + ' recebeu: ' + str(erro[1][0]['valor'])
    if (debug):
        erro = erro[1]
    print(erro)
    escrever_arquivo_sintatico(arquivo, erro, tokens)


def main():
    pasta = './files/input'
    arquivos_filtrados = []
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            if (arquivo.endswith(".txt")):
                arquivos_filtrados.append(arquivo)

    for arquivo in arquivos_filtrados:
        [tokens, erros] = analise(ler_arquivo(arquivo))
        escrever_arquivo(arquivo, tokens, erros)
        resultado = sintatico(tokens)
        if (resultado[0]):
            print("Código compilado com sucesso!!")
        else:
            print_erro(resultado, False, arquivo, tokens)


if __name__ == "__main__":
    main()
