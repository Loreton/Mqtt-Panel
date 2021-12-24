#!/usr/bin/python
# -*- coding: utf-8 -*-

# updated by ...: Loreto Notarantonio
# Date .........: 2021-10-09

# https://github.com/python-telegram-bot/python-telegram-bot


import  sys; sys.dont_write_bytecode = True
import  os
import  socket
import  time
from    benedict import benedict
from    pathlib import Path
import  yaml
import uuid, random # per il client_id

from LnLib.YamlLoaderLN import LoadConfigurationFile
from iotmqttpanel_StandAlone import dict_to_yaml, yamlFileToJsonFile

########################################################
# Crea puntatori e non verso i dati di configurazione
# inserendoli direttamente nella classe chiamante
#
#   appl_type: telegram or mqtt
########################################################
class ConfigurationInterface_Class():
    def __init__(self, *, configuration_file, logger):
        self.logger=logger

        # db_user=os.getenv('MARIADB_USER')
        # db_password=os.getenv('MARIADB_PASSWORD')
        # db_host=os.getenv('MARIADB_HOST')
        # hostname=socket.gethostname()
        """-------------
            Load configuration file and create dict
        ------------- """
        self.logger.info('going to read: %s', configuration_file)
        conf=LoadConfigurationFile(filename=configuration_file, logger=self.logger)
        self.Config=benedict(conf)

        print(dict_to_yaml(self.Config))

        import pdb; pdb.set_trace(); pass # by Loreto
        r = self.Config.search('Power state', in_keys=False, in_values=True, exact=False, case_sensitive=False)
        r = self.Config.match("confirmationMessa*", indexes=True)
        r = self.Config.keypaths(indexes=True)

        yamlFileToJsonFile(configuration_file, replace=True)






