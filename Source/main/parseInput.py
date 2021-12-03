# #############################################
#
# updated by ...: Loreto Notarantonio
# Date .........: 2021-09-10
#
# #############################################

import sys
import argparse
import os

Version='Mqtt-Client V1.0'

##############################################################
# - MAin Options
##############################################################
def mainArguments():
    parser=argparse.ArgumentParser(description='Mqtt Client (by: Ln)',
                formatter_class=argparse.RawTextHelpFormatter)

    """ -------- mqtt-client """
    parser.add_argument('--file', required=True, type=str,
                            help='file to be processed')


    parser.add_argument('--systemd', action='store_true', help='systemd is active')

    common_options(parser)

    return parser




def common_options(my_parser):

    my_parser.add_argument('------------  debug options', action='store_true')

    my_parser.add_argument('--display-args', action='store_true', help='Display input paramenters')

    my_parser.add_argument('--debug', action='store_true', help='display paths and input args')

    my_parser.add_argument('--version', action='version',
                            version=Version, help="Show program's version number and exit.")


    my_parser.add_argument('------------  overriding log options', action='store_true')

    my_parser.add_argument('--no-log', action='store_true', help='disable logging')

    my_parser.add_argument( "--log-console",
                            metavar='<log--console-level>',
                            type=str,
                            default='disable',
                            choices=['critical','error','warning','info','debug', 'disable'],
                            help='specify console log level and activate it.'
                        )

    my_parser.add_argument('--log-exclude',
                                metavar='',
                                required=False,
                                default=[],
                                nargs='*',
                                help="""Activate log.
    E' anche possibile indicare una o più stringhe separate da BLANK
    per identificare le funzioni che si vogliono filtrare nel log.
    Possono essere anche porzioni di funcName.
    Es: --log-module nudule1 module2 module3
        """)

    my_parser.add_argument('--log-include',
                                metavar='',
                                required=False,
                                default=['*'],
                                nargs='*',
                                help="""Activate log.
    E' anche possibile indicare una o più stringhe separate da BLANK
    per identificare le funzioni che si vogliono filtrare nel log.
    Possono essere anche porzioni di funcName.
    Es: --log-module nudule1 module2 module3
        """)







def post_process(args):
    # separazione degli args di tipo debug con quelli applicativi
    dbg=argparse.Namespace()
    log=argparse.Namespace()

    '''
    il processo che segue è per evitare:
       RuntimeError: dictionary changed size during iteration
       suddividiamo le varie options
    '''
    keys=list(args.__dict__.keys())
    _dargs=args.__dict__
    for key in keys:
        val=getattr(args, key)
        if key in ['log', 'no_log']:
            setattr(log, key, val)
        elif key.startswith('log_'):
            setattr(log, key[4:], val)
        elif key.startswith('  '): # ignore
            pass
        elif key.startswith('+log'):
            pass # le ignoro in quanto servono solo ad impostare il valore
        elif key in ['debug', 'display_args']:
            setattr(dbg, key, val)
        elif 'debug options' in key:
            pass
        elif 'log options' in key:
            pass
        else:
            continue

        delattr(args, key)

    app=args

    if dbg.display_args:
        del dbg.display_args
        # import ujson as json
        import json
        json_data = json.dumps(vars(app), indent=4, sort_keys=True)
        print('application arguments: {json_data}'.format(**locals()))
        json_data = json.dumps(vars(log), indent=4, sort_keys=True)
        print('logging arguments: {json_data}'.format(**locals()))
        json_data = json.dumps(vars(dbg), indent=4, sort_keys=True)
        print('debugging arguments: {json_data}'.format(**locals()))
        sys.exit(0)

    return app, log, dbg

##############################################################
# - Parse Input
##############################################################
def parseInput(version=None):
    global Version
    if version:
        Version=version
    # =============================================
    # = Parsing
    # =============================================
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    # parser=mainOptions(server_list)
    parser=mainArguments()

    args=parser.parse_args()
    return post_process(args)

