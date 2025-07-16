import os

from PyQt5.QtWidgets import QInputDialog
from qgis.core import QgsVectorLayer, QgsProject

dir_path = QInputDialog.getText(None, "Diretório dos arquivos .gpkg", "Caminho da pasta")[0]
operation = QInputDialog.getText(None, "Seleção de operação", "pressione 1 ou 2\n1 - corrigir palavras\n2 - exclusão de linhas")[0]
field_name = QInputDialog.getText(None, "Campo da tabela para alteração", "Nome do campo da tabela")[0]

list_gpkg = os.listdir(dir_path)

connectives = {'de', 'des', 'da', 'das', 'do', 'dos', 'em', 'para', 'com', 'a', 'as', 'o', 'os', 'na', 'nas', 'no', 'nos', 'e'}


def correct_form(enter_word=""):

    """
    Função realiza operação correção de nomes baseado na relação chave-valor entre as palavras.

    enter_word (param): é a palavra de entrada que será corrigida através de comparação chave-valor
    corrected (var): é uma variável que contém um dicionário para comparação.
        O ideal seria inserí-lo em um arquivo .json, mas optei para não estressar o Qgis com mais uma operação com arquivos.

    returns:
        tipo: o retorno da função é uma string com o nome corrigido, mas que retorna o mesmo valor de entrada caso não encontrado.
    """

    corrected = ... #COPY AND PASTE THE DICTIONARY (WORD_BASE) HERE
    return corrected.get(enter_word, enter_word)


def une_and_up(*args):

    new_street_name = ' '.join(args)
    feature.setAttribute(field_name, new_street_name)
    layer_name.updateFeature(feature)


def spelling_correction(object_edit):
    """
    Função formata palavras e realiza a chamada da função de correct_form e sobe as alterações na linha alterada.

    :param object_edit: é uma string contendo o nome de um logradouro
    :return: None
    """

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


def exclude_feature(object_edit):

    """
    Realiza a exclusão de uma linha a depender do status

    :param object_edit: é uma string maiúscula contendo o status da linha ("NONE", "DÚVIDA" e "EXCLUIR")
    :return: None
    """

    if object_edit == "EXCLUIR":
        layer_name.deleteFeature(feature.id())


menu = {'1': spelling_correction, '2': exclude_feature}
function_exe = menu[operation]

for gpkg_file in list_gpkg:

    path_gpkg = os.path.join(dir_path, gpkg_file)
    name_gpkg = gpkg_file[:-5]
    #realização da conexão com a camada no banco de dados
    uri_conect = f"{path_gpkg}|layername={name_gpkg}"
    layer_name = QgsVectorLayer(uri_conect, name_gpkg, "ogr")

    if not layer_name.isValid():
        print(f"Erro ao carregar a camada. Verifique a extensão do arquivo: {name_gpkg}")
        layer_name = QgsVectorLayer(fr"{dir_path}\{field_name}", gpkg_file, "ogr")
        continue

    if not layer_name.isEditable():
        layer_name.startEditing()

    for feature in layer_name.getFeatures():
        object_edit = feature[field_name]

        # Pulando repetição em casos nulos, vazios ou de não string
        if object_edit in [None, ""] or not isinstance(object_edit, str):
            continue

        function_exe(object_edit)

    if layer_name.isEditable():
        layer_name.commitChanges()
        print(f"Alterações salvas para o arquivo: {gpkg_file}")
    else:
        print(f"Falha ao salvar as alterações. Verifique a extensão do arquivo: {gpkg_file}")

        # Limpando referências
    QgsProject.instance().removeMapLayer(layer_name)

print("Processo finalizado! Verifique as camadas.")
