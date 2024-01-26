#!/usr/bin/python3

from persistence.storage import PersistenceFile
from file_manager.file_manager import FileManager
from ufs.ufs import Ufs
import logging
import requests
import os

HOST = os.environ.get('HOST')
USERNAME = os.environ.get('USERNAME')
FORMAT_LOG = '%(asctime)s %(clienthost)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT_LOG)
logger_config = {'clienthost': HOST, 'user': USERNAME}
logger = logging.getLogger('persiste_arquivos_storage')
storage = PersistenceFile()
file_mgmt = FileManager()
ufs = Ufs()
ROOT_CEP_URL = 'https://www.cepaberto.com/downloads.csv?'

def download_cep_files(parameters):
    try:
        response = requests.post(ROOT_CEP_URL + parameters)
        filename = 'downloaded.zip'
        file_saved = file_mgmt.save_downloaded_file(filename, response.content)
        file_saved = file_saved.split('/')[1]
        storage.persists_file(file_saved, parameters)
        file_mgmt.delete_downloaded_file(filename)
        logger.info('Arquivo persistido com sucesso no storage.', file_saved)
    except Exception as e:
        logger.error('Falha ao persistir arquivo no storage.', e)

download_cep_files('name=states')
download_cep_files('name=cities')
for uf in ufs.get_ufs():
    for i in range(1, 6):
        parameters = 'name={}&part={}'.format(uf, str(i))
        download_cep_files(parameters)



















