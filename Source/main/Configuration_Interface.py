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

# from LnLib.fernetLN     import FernetLN
# from LnLib.toYaml       import readYamlFile, writeYamlFile, print_dict
from LnLib.YamlLoaderLN import LoadConfigurationFile
# from LnLib.HttpLN_Class import ApiHttp
# from LnLib.arpScan      import ipFromMac


# from SendTelegramMsg            import SendTelegram_CLASS
# from LnLib.netUtils             import check_socket as pingPort
from  LnLib.loggerLN            import getLnLogger

# from LnLib.MariaDB_LnClass      import LnMariaDB, mariaDBTable



########################################################
# Crea puntatori e non verso i dati di configurazione
# inserendoli direttamente nella classe chiamante
#
#   appl_type: telegram or mqtt
########################################################
class ConfigurationInterface_Class():
    def __init__(self, *, appl_name, configuration_file, logger):
        self.logger=logger

        db_user=os.getenv('MARIADB_USER')
        db_password=os.getenv('MARIADB_PASSWORD')
        db_host=os.getenv('MARIADB_HOST')
        hostname=socket.gethostname()
        """-------------
            Load configuration file and create dict
        ------------- """
        self.logger.info('going to read: %s', configuration_file)
        conf=LoadConfigurationFile(filename=configuration_file, logger=self.logger)
        self.Config=benedict(conf)







