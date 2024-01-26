#!/usr/bin/python3

from minio import Minio
import os
import logging
import re
from ufs.ufs import Ufs

HOST = os.environ.get('HOST')
USERNAME = os.environ.get('USERNAME')
FORMAT_LOG = '%(asctime)s %(clienthost)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT_LOG)
logger_config = {'clienthost': HOST, 'user': USERNAME}
logger = logging.getLogger('persiste_arquivos_storage')

class PersistenceFile:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
            return cls.instance

    def __init__(self):
        self.minio_endpoint = os.environ.get('MINIO_ENDPOINT')
        self.minio_access_key = os.environ.get('MINIO_ACCESS_KEY')
        self.minio_secret_key = os.environ.get('MINIO_SECRET_KEY')
        self.client = Minio(self.minio_endpoint,
                            self.minio_access_key,
                            self.minio_secret_key,
                            secure=False)

    def __persists_state(self, filename):
        result = self.client.fput_object('estados',
                                         filename,
                                         'downloaded/{}'.format(filename),
                                         content_type='text/csv')
        logger.info('Arquivo de Estados enviado ao storage.',
                    result,
                    extra=logger_config)

    def __persists_city(self, filename):
        result = self.client.fput_object('cidades',
                                         filename,
                                         'downloaded/{}'.format(filename),
                                         content_type='text/csv')
        logger.info('Arquivo de Cidades enviado ao storage.',
                    result,
                    extra=logger_config)

    def __persists_ceps(self, filename):
        result = self.client.fput_object('ceps',
                                         filename,
                                         'downloaded/{}'.format(filename),
                                         content_type='text/csv')
        logger.info('Arquivo de ceps enviado ao storage.',
                    result,
                    extra=logger_config)

    def persists_file(self, filename, parameters):
        bucket_choose = re.findall('name=[a-zA-Z]+', parameters)[0]
        bucket_choose = bucket_choose.split('=')[1]
        if bucket_choose == 'states':
            self.__persists_state(filename)
            return

        if bucket_choose == 'cities':
            self.__persists_city(filename)
            return

        ufs = Ufs()
        uf_found = ufs.get_uf(bucket_choose)

        if uf_found is not None:
            self.__persists_ceps(filename)
        else:
            logger.info('Nenhum Estado localizado para persistir dados de cep no storage.', filename, parameters)
