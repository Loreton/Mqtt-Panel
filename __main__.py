#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Date .........: 26-11-2021 08.57.18
#
import  sys; sys.dont_write_bytecode = True
import  os, socket
from    pathlib import Path
this=sys.modules[__name__]
__version__="Mqtt-Client V2021-11-26_085718"

#todo: calcolare sunrise per shellies
#todo: modificare pulsetime: 0 su tasmota telegram message

# in caso di file.zip la lnLib.zip viene e stratta in area temp e messa nel path per essere utiizzata.
# questo perché non riesco ad importaremoduli da un zip dentro un altro zip
from    Source.main.setPathsLN import setPaths; setPaths(sub_dirs=[
                                                        'Source',
                                                        'Source/main',
                                                        # 'Source/lnLib', # used only for building Source/LnLib.zip...
                                                        'Source/lnLib.zip',
                                                        'Source/mqtt',
                                                        'Source/mqtt/mqtt_msg',
                                                        # 'Source/telegram',
                                                        # 'Source/telegram/API',
                                                        # '/home/pi/GIT-REPO/Python/LnPyLib/Configuration-LN',
                                                        ],
                                                        prj_arg=1, # argument containing prj_name utile per unzip lnlib
                                                        fDEBUG=False)


from  LnLib.fernetLN     import FernetLN
from  LnLib.loggerLN     import getLnLogger, getNullLogger
from  LnLib.YamlLoaderLN import LoadConfigurationFile
from  LnLib.toYaml       import readYamlFile, writeYamlFile, print_dict

from  parseInput         import parseInput






if __name__ == '__main__':
    print('starting....')
    _this_filepath=Path(sys.argv[0]).resolve()
    script_path=_this_filepath.parent # ... then up one level
    os.chdir(script_path) #  cambiamo dir per avere riferimenti relativi ai file
    log_dir='/tmp/mqtt_client'

    """ parsing input --------------- """
    args, log, dbg=parseInput(version=__version__)

    prj_name=script_path.stem
    if prj_name in ['bin']: # in caso di python.zip
        prj_name=script_path.parent.stem

    os.environ['script_path']=str(script_path) # potrebbe essere usata nel config_file
    os.environ['TG_GROUP']=args.tggroup_name # usata nel config_file
    os.environ['LOG_DIR']=str(log_dir) # usata nel config_file



    """ logger start ----------- """
    logger=getLnLogger(logger_config_file=f'conf/logger_config.yaml', #deve lavorare con il relative_path
                log_dir=log_dir,
                # log_filename=f'/tmp/{args.action}/{args.action}.log',
                logger_name='mqtt_client',
                console_level=log.console,
                program_version=__version__,
                )

    """ status_logger ----------- """
    status_logger=getNullLogger()
    logger.include_modules(log.include)
    logger.exclude_modules(log.exclude)
    logger.exclude_modules(['decorator'])
    logger.info('application arguments: %s', vars(args))
    logger.debug('logging arguments: %s', log)
    logger.debug('debugging arguments: %s', vars(dbg))
    """ logger end ------------- """




    kwargs={
        'logger': logger,
        'status_logger': status_logger,
        'pass_phrase': args.pass_phrase,
        'configuration_file': 'conf/mqtt_config.yaml',
        'systemd': args.systemd, # under systemd control
    }


    # if args.action=='mqtt':
    logger.info('starting Mqtt_Client')
    import  Mqtt_class as MqttClient
    MqttClient.Main(appl_name='mqtt_client', **kwargs)

    # else:
    #     print('exiting.... NO valid action:', args.action)

    logger.debug('exiting....')
    sys.exit(0)
