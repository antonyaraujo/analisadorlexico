# Compilador - README

Este repositório contém um compilador desenvolvido como parte do projeto da disciplina EXA869 - MI Processadores de Linguagens de Programação. O compilador é responsável pela análise léxica e sintática de um código fonte em uma determinada linguagem de programação.

## Analisador Sintático

O código fornecido neste repositório implementa o analisador sintático do compilador. O analisador sintático é responsável por verificar se a estrutura do código fonte está correta de acordo com as regras gramaticais da linguagem.

O analisador sintático está dividido em diferentes funções, cada uma responsável por analisar uma parte específica da gramática da linguagem. O código começa com a função `sintatico()`, que é o ponto de partida da análise sintática.

## Instruções de Uso

Siga as instruções abaixo para executar o compilador:

1. Certifique-se de ter o Python instalado em sua máquina.

2. Faça o download ou clone este repositório.

3. Navegue até o diretório do projeto.

4. Certifique-se de que o arquivo `lexico.py` esteja presente no diretório.

5. No código fonte principal (`main.py`), verifique se o caminho dos arquivos de entrada e saída está correto.

   - O diretório de entrada padrão é `files/input`, onde devem estar os arquivos de código fonte a serem compilados.
   - O diretório de saída padrão é `files/output`, onde serão gerados os arquivos com os resultados da compilação.

6. Execute o comando `python main.py` para iniciar a compilação.

   - O compilador irá percorrer todos os arquivos presentes no diretório de entrada.
   - Para cada arquivo, será gerado um arquivo de saída com a extensão `-saida.txt` no diretório de saída.
   - O arquivo de saída conterá os tokens encontrados durante a análise léxica e quaisquer erros sintáticos encontrados.

7. Verifique a saída gerada no diretório de saída para cada arquivo compilado.

   - Os tokens encontrados durante a análise léxica serão exibidos primeiro, seguidos por quaisquer erros sintáticos encontrados.

8. Analise os resultados da compilação para determinar se o código fonte está correto ou se há erros a serem corrigidos.
   - Se não houver erros sintáticos, a mensagem "Código compilado com sucesso!!" será exibida.

## Observações

- Certifique-se de fornecer o código fonte correto no diretório de entrada antes de executar o compilador.
- Os arquivos de entrada devem estar no formato de texto (.txt).
- O código fornecido neste repositório lida apenas com a análise sintática. A análise léxica é realizada por um módulo externo chamado `lexico.py`, que deve estar presente no mesmo diretório do arquivo principal (`main.py`).
- Certifique-se de que todas as dependências necessárias estejam instaladas antes de executar o compilador.
- Este compilador é fornecido como exemplo e pode não abranger todos os casos de uso ou atender a todas as necessidades
