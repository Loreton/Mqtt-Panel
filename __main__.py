#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Date .........: 23-12-2021 13.07.32
#
import  sys; sys.dont_write_bytecode = True
import  os, socket
from    pathlib import Path
this=sys.modules[__name__]
__version__="Mqtt-Panel V2021-12-23_130732"

#todo: calcolare sunrise per shellies
#todo: modificare pulsetime: 0 su tasmota telegram message

# in caso di file.zip la lnLib.zip viene e stratta in area temp e messa nel path per essere utiizzata.
# questo perché non riesco ad importaremoduli da un zip dentro un altro zip
from    Source.main.setPathsLN import setPaths; setPaths(sub_dirs=[
                                                        'Source',
                                                        'Source/main',
                                                        # 'Source/lnLib', # used only for building Source/LnLib.zip...
                                                        'Source/lnLib.zip',
                                                        # 'Source/mqtt',
                                                        # 'Source/mqtt/mqtt_msg',
                                                        # 'Source/telegram',
                                                        # 'Source/telegram/API',
                                                        # '/home/pi/GIT-REPO/Python/LnPyLib/Configuration-LN',
                                                        ],
                                                        prj_arg=1, # argument containing prj_name utile per unzip lnlib
                                                        fDEBUG=False)


# from  LnLib.loggerLN     import getLnLogger, getNullLogger
# from  LnLib.YamlLoaderLN import LoadConfigurationFile
# from  LnLib.toYaml       import readYamlFile, writeYamlFile, print_dict

from  parseInput         import parseInput

from Configuration_Interface import ConfigurationInterface_Class


##########################################################################
# https://coloredlogs.readthedocs.io/en/latest/readme.html#installation
# https://coloredlogs.readthedocs.io/en/latest/api.html#changing-the-colors-styles
##########################################################################
def getColoredLogger(logging_file=None):
    import logging, coloredlogs


    def add_StreamingHandler():
        # coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s'
        coloredlogs.DEFAULT_LOG_FORMAT = '[%(name)s.%(funcName)-30s:%(lineno)4s %(process)d]: %(levelname)-8s %(message)s'
        # coloredlogs.DEFAULT_LOG_FORMAT = '[%(funcName)-30s:%(lineno)4s %(process)d]: %(levelname)-8s %(message)s'
        coloredlogs.install(level='DEBUG') # set also log level


    logger = logging.getLogger(__name__)
    # logger.setLevel('WARNING') # ROOT level default - decide il livello massimo

    add_StreamingHandler()
    # add_FileHandler(logging_file=logging_file, level=logging.DEBUG)
    logger.setLevel('DEBUG') # ROOT level - decide il livello massimo
    return logger




if __name__ == '__main__':
    logger=getColoredLogger()

    _this_filepath=Path(sys.argv[0]).resolve()
    script_path=_this_filepath.parent # ... then up one level
    os.chdir(script_path) #  cambiamo dir per avere riferimenti relativi ai file
    appl_name='mqtt_panel'
    log_dir=f'/tmp/{appl_name}'

    """ parsing input --------------- """
    args, log, dbg=parseInput(version=__version__)

    prj_name=script_path.stem
    if prj_name in ['bin']: # in caso di python.zip
        prj_name=script_path.parent.stem

    os.environ['script_path']=str(script_path) # potrebbe essere usata nel config_file
    # os.environ['TG_GROUP']=args.tggroup_name # usata nel config_file
    os.environ['LOG_DIR']=str(log_dir) # usata nel config_file



    # """ logger start ----------- """
    # logger=getLnLogger(logger_config_file=f'config/logger_config.yaml', #deve lavorare con il relative_path
    #             log_dir=log_dir,
    #             # log_filename=f'/tmp/{args.action}/{args.action}.log',
    #             logger_name=appl_name,
    #             console_level=log.console,
    #             program_version=__version__,
    #             )

    # """ status_logger ----------- """
    # status_logger=getNullLogger()
    # logger.include_modules(log.include)
    # logger.exclude_modules(log.exclude)
    # logger.exclude_modules(['decorator'])
    # logger.info('application arguments: %s', vars(args))
    # logger.debug('logging arguments: %s', log)
    # logger.debug('debugging arguments: %s', vars(dbg))
    # """ logger end ------------- """



    ###########################################
    #
    ###########################################
    # create object class
    myConfig=ConfigurationInterface_Class(configuration_file=args.file, logger=logger)


    logger.debug('exiting....')
    sys.exit(0)
