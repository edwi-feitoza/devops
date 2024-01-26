#!/usr/bin/python3

import glob
from zipfile import ZipFile
import os
import logging

HOST = os.environ.get('HOST')
USERNAME = os.environ.get('USERNAME')
FORMAT_LOG = '%(asctime)s %(clienthost)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT_LOG)
logger_config = {'clienthost': HOST, 'user': USERNAME}
logger = logging.getLogger('persiste_arquivos_storage')


class FileManager:

    def save_downloaded_file(self, filename, content):
        try:
            with open('downloaded/{}'.format(filename), mode='wb') as file:
                file.write(content)
            with ZipFile('downloaded/{}'.format(filename), 'r') as zip_object:
                zip_object.extractall('downloaded/')
                os.remove('downloaded/{}'.format(filename))
                dir_path = r'downloaded/*.csv'
                arquivos_csv = glob.glob(dir_path)
                for arquivo_csv in arquivos_csv:
                    if arquivo_csv.endswith('.csv'):
                        return arquivo_csv
        except Exception as e:
            logger.error('Falha ao salvar e devolver arquivo csv '
                         'obtido da API de cepaberto', e)

    def delete_downloaded_file(self, filename):
        try:
            dir_path = r'downloaded/*.csv'
            files_to_delete = glob.glob(dir_path)
            for file_to_delete in files_to_delete:
                os.remove(file_to_delete)
                logger.info('Arquivo csv excluido com sucesso.', file_to_delete)
        except Exception as e:
            logger.error('Falha ao remover arquivo csv.', filename, e)
