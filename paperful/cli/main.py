import argparse
import configparser
import importlib
import logging
import pkgutil

import xdg.BaseDirectory

import paperful.cli.logging
import paperful.cli.subcommands
import paperful.paperless

logger = logging.getLogger(
    __name__,
)


def entry_point(
        ):
    paperful.cli.logging.set_up(
    )

    configuration = configparser.ConfigParser(
    )

    configuration.read_dict(
        {
            'logging': {
                'everything': False,
                'level': 'INFO',
            },
            'paperless': {
            },
        },
    )

    paperful.cli.logging.set_level(
        level=configuration['logging']['level'],
    )

    parser = argparse.ArgumentParser(
        description='Manage documents stored in Paperless',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subcommand_parsers = parser.add_subparsers(
        dest='action',
        title='subcommands',
    )

    subcommands = load_subcommands(
        package=paperful.cli.subcommands.__name__,
        paths=paperful.cli.subcommands.__path__,
    )

    load_subcommand_defaults(
        configuration=configuration,
        subcommands=subcommands,
    )

    configuration_directory = xdg.BaseDirectory.save_config_path(
        'paperful',
    )
    configuration_path = configuration_directory + '/config.ini'

    configuration.read(
        configuration_path,
    )

    parser.add_argument(
        '-l',
        '--logging-level',
        choices=[
            'DEBUG',
            'INFO',
            'WARNING',
            'ERROR',
            'CRITICAL',
        ],
        default=configuration['logging']['level'],
        dest='logging_level',
        help='most detailed logging level to emit',
        metavar='LEVEL',
    )

    parser.add_argument(
        '-L',
        '--log-everything',
        action='store_true',
        default=configuration['logging']['everything'],
        dest='log_everything',
        help='emit logs from third-party code too',
    )

    parser.add_argument(
        '-u',
        '--paperless-api-url',
        default=configuration['paperless']['url'],
        dest='paperless_api_url',
        help='Paperless API URL',
        metavar='URL',
    )

    parser.add_argument(
        '-t',
        '--paperless-api-token',
        default=configuration['paperless']['token'],
        dest='paperless_api_token',
        help='Paperless API token',
        metavar='TOKEN',
    )

    load_subcommand_argument_parsers(
        configuration=configuration,
        parser=subcommand_parsers,
        subcommands=subcommands,
    )

    args = parser.parse_args(
    )

    paperful.cli.logging.set_level(
        args.logging_level,
    )

    paperless_session = paperful.paperless.Session(
        paperless_api_token=args.paperless_api_token,
        paperless_api_url=args.paperless_api_url,
    )

    subcommand = args.instance

    subcommand.run(
        args=args,
        paperless_session=paperless_session,
    )


def load_subcommands(
            package,
            paths,
        ):
    subcommands = {
    }

    iterator = pkgutil.iter_modules(
        path=paths,
    )
    for module_info in iterator:
        module_name = module_info.name
        module_path = '.' + module_name
        module = importlib.import_module(
            name=module_path,
            package=package,
        )

        subcommand_class = module.Subcommand
        subcommand_instance = subcommand_class(
        )

        subcommand = {
            'class': subcommand_class,
            'instance': subcommand_instance,
        }

        if module_info.ispkg:
            # subcommand contains subcommands
            subcommand['subcommands'] = load_subcommands(
                package=module.__name__,
                paths=module.__path__,
            )

        subcommands[module_name] = subcommand

    return subcommands


def load_subcommand_defaults(
            configuration,
            subcommands,
        ):
    iterator = subcommands.items(
    )
    for name, subcommand in iterator:
        subcommand_instance = subcommand['instance']

        subcommand_default_configuration = subcommand_instance.get_default_configuration(
        )
        configuration.read_dict(
            subcommand_default_configuration,
        )

        try:
            subsubcommands = subcommand['subcommands']
        except KeyError:
            pass
        else:
            # subcommand contains subcommands
            load_subcommand_defaults(
                configuration=configuration,
                subcommands=subsubcommands,
            )


def load_subcommand_argument_parsers(
            configuration,
            parser,
            subcommands,
        ):
    iterator = subcommands.items(
    )
    for name, subcommand in iterator:
        subcommand_class = subcommand['class']
        subcommand_instance = subcommand['instance']

        if 'subcommands' in subcommand:
            # subcommand contains subcommands

            subparser = parser.add_parser(
                name,
                description=subcommand_class.description,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                #help=module.CommandGroup.help,
            )

            subsubparsers = subparser.add_subparsers(
                dest='action',
                title='subcommands',
            )

            load_subcommand_argument_parsers(
                configuration=configuration,
                parser=subsubparsers,
                subcommands=subcommand['subcommands'],
            )
        else:
            subcommand_parser = parser.add_parser(
                name,
                aliases=subcommand_class.aliases,
                description=subcommand_class.description,
                epilog=subcommand_class.epilog,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )

            subcommand_instance.build_argument_parser(
                configuration=configuration,
                argument_parser=subcommand_parser,
            )

            subcommand_parser.set_defaults(
                instance=subcommand_instance,
            )
