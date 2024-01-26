#!/usr/bin/python3

import os
import logging

HOST = os.environ.get('HOST')
USERNAME = os.environ.get('USERNAME')
FORMAT_LOG = '%(asctime)s %(clienthost)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT_LOG)
logger_config = {'clienthost': HOST, 'user': USERNAME}
logger = logging.getLogger('persiste_arquivos_storage')

class Ufs:
    def __init__(self):
        self.__ufs = ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO', 'AL', 'BA',
                      'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE', 'DF', 'GO',
                      'MT','MS', 'ES', 'MG', 'RJ', 'SP', 'PR', 'RS', 'SC']

    def get_uf(self, uf):
        uf_index = [index for (index, item) in enumerate(self.__ufs) if item == uf]
        if uf_index is not None and len(uf_index) > 0:
            index_returned = uf_index[0]
            return self.__ufs[index_returned]
        else:
            logger.warning('Nenhum UF localizado.', uf)

    def get_ufs(self):
        return self.__ufs
