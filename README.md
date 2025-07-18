# Q_correct

## Sumário

1. Introdução
    - Objetivo do projeto
    - Descrição do projeto
2. Requisitos
    - Funcionais
    - Não-funcionais
    - Dependências
3. Explicação do código


4. Contato

## Introdução

### Objetivo do projeto
<p style="text-align: justify;">O código foi criado com base em um problema, corrigir nomes de logradouros (ruas) que estavam em tabelas de atributos de arquivos GPKG, no Qgis, pois a equipe necessitava realizar essas correções e haviam muitos arquivos, dos quais alguns possuim mais de 10 mil linhas e eles teriam de verificar linha a linha quais campos de nomes de logradouros possuiam erro ortográfico; outro tarefa necesária era, em outra atividade, a exclusão de linhas que apresentassem o elemento "EXCLUIR".<p>

### Descrição do projeto
<p style="text-align: justify;">O código foi desenvolvido em linguagem Python com o intuíto de rodar no terminal do Python do Qgis, por isso, é possivel observar o uso de uma biblioteca como o PyQt5, já que ela dispensa o uso de instalações, já que o Qgis a possui nativamente, outro uso é o módulo qgis.core, para acessar funções de manipulação internas do Qgis. Um ponto adicional para este código é que como o código roda diretamente no terminal Qgis, o dicionário que está no arquivo word_base.txt deve ser copiado e colado antes da operação.<p>

## Requisitos

### Funcionais

- <p style="text-align: justify;">Peritir que o usuário escolha entre as operações que deseja realizar;<p>
- <p style="text-align: justify;">Acessar pastas e arquivos para que o usuário não seja preso a um procedimento que pode gerar erros, mas executar o código independente de onde os arquivos gpkg estejam;<p>
- <p style="text-align: justify;">Localizar um campo da tabela para realizar os procedimentos e estreitar os processos;<p>
- <p style="text-align: justify;">Colocar os arquivos para o modo de edição para que o arquivo seja editado sem a necessidade do usuário ativar a camada para edição manualmente;<p>
- <p style="text-align: justify;">Corrigir palavras com erros ortográficos através de palavras já sem acentuação gráfica;<p>
- <p style="text-align: justify;">Excluir linhas, com base em campos da tabela de atributo que apresentem a solicitação de exclusão;<p>
- <p style="text-align: justify;">Salvar alterações que forem feitas nas camadas;<p>
- <p style="text-align: justify;">Fechar a camada para edição, para que o arquivo não permaneça aberto para edição e feche sem salvamento;<p>
- <p style="text-align: justify;">Informar os arquivos de camadas gpkg que apresentaram erros e, por isso, não foram editados.<p>

### Não funcionais

- <p style="text-align: justify;">Ser executável dentro do terminal Qgis sem que apresente problemas maiores, ou processos difíceis para execução;<p>
- <p style="text-align: justify;">Conseguir processar mais de 20 mil linhas de tabelas sem apresentar travamentos;<p>
- <p style="text-align: justify;">Executar operações em menos de 30 minutos;<p>

### Dependências

1. Bibliotecas
    - <p style="text-align: justify;">Biblioteca os – utilizada para acessar os arquivos e criar listas, com o método listdir;<p>
    - <p style="text-align: justify;">Biblioteca PyQt5.QtWidgets – utilizada para acessar a ferramenta QInputDialog que serve para conseguir as entradas do usuário;<p>
    - <p style="text-align: justify;">Biblioteca qgis.core – utilizada para alterações vetoriais no Qgis, permitindo edições.<p>

## Explicação do código

### Correção de nomes

#### Funções

1. Formatação de palaras
    - <p style="text-align: justify;">É uma função que formata as palavras de entrada para que sejam localizáveis no dicionário da função correct_form. Ela retorna a execução e uma função que se enccarrega de unir as palavras da list_words e subir para o banco de dados da planilha atualizando.<br>
    enter_word é uma string de entrada que passa por filtros depois de ter seu formato alterado para minúscuo, isso para que mantenha o padrão estaabelecido para o documento.<p>
    ```python
    def spelling_correction(object_edit):
        list_words = []
        trust_text = object_edit.split()

        for word_to_correct in trust_text:
            enter_word = word_to_correct.lower()
            result_word = correct_form(enter_word=enter_word)
            if result_word in ["pb", "br", "ii", "i"]:
                list_words.append(result_word.upper())
            elif result_word in connectives:
                list_words.append(result_word)
            else:
                list_words.append(result_word.capitalize())
        return une_and_up(*list_words)
    ```

2. Correção de palavras com base no nome
    - <p style="text-align: justify;">Função realiza operação correção de nomes baseado na relação chave-valor entre as palavras.<br>
    - enter_word (param): é a palavra de entrada, uma string, que será corrigida através de comparação chave-valor.<br>
    - corrected (var): é uma variável que contém um dicionário para comparação. O ideal seria inserí-lo em um arquivo .json, mas optei para não estressar o Qgis com mais uma operação com arquivos.<br>
    - o retorno da função é uma string com o nome corrigido, mas que retorna o mesmo valor de entrada caso não encontrado.<p>
    ```python
    def correct_form(enter_word=""):
       corrected = ... #COPY AND PASTE THE DICTIONARY (WORD_BASE) HERE
        return corrected.get(enter_word, enter_word)
    ```

3. Unindo o texto
    - <p style="text-align: justify;">Recebe um conjunto de argumentos e une esses argumentos num texto que redefine a frase que é o nome do logradouro (rua), que é uma String, não retornando nada no processo, mas atualizando o valor da linha.<p>
    ```python
    def une_and_up(*args):

        new_street_name = ' '.join(args)
        feature.setAttribute(field_name, new_street_name)
        layer_name.updateFeature(feature)
    ```

#### Explicando algumas estruturas do código

1. Conectando com a tabela do banco de dados do Qgis
    - <p style="text-align: justify;">Nesse trecho é definida a string de conexão em uri_connect, sendo passada essa string para se obter um objeto QgsVectorLayer na variável layer_name, que cria a camada vetorial necessária para abrir e editar o banco de dados do arquivo GPKG.<p>
    ```python
    uri_conect = f"{path_gpkg}|layername={name_gpkg}"
    layer_name = QgsVectorLayer(uri_conect, name_gpkg, "ogr")
    ```
2. Subindo as mudanças e limpando as referências do arquivo
    - <p style="text-align: justify;">Nesse trechos são definidas as subidas para o banco de dados, por meio do método commitChanges e através da instância QgsProject é feita a remoção das referências do projeto que são criadas e podem comprometer a execução do código por esgotamento do Qgis.<p>
    ```python
    layer_name.commitChanges()
    [...]
    QgsProject.instance().removeMapLayer(layer_name)
    ```

### Exclusão de linhas

#### Função

- <p style="text-align: justify;">Esta função exclui uma linha da tabela se o valor passado, uma string, do campo passado é igual a "EXCLUIR".<p>
```python
def exclude_feature(object_edit):
    if object_edit == "EXCLUIR":
        layer_name.deleteFeature(feature.id())
```

## Contato