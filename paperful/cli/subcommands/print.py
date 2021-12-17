import logging

import paperful.cli.subcommand
import paperful.cups
import paperful.paperless

logger = logging.getLogger(
    __name__,
)


class Subcommand(
            paperful.cli.subcommand.Subcommand,
        ):
    aliases = [
    ]
    description = 'Print documents stored in a Paperless instance'
    epilog = 'By default, print all documents tagged `TOPRINT` but not `TODO`, as listed by the subcommand `list toprint`. Tag printed documents with `meta:printed`. Standard printing options are listed at https://www.cups.org/doc/options.html#OPTIONS.'

    def __init__(
                self,
            ):
        self.printer = paperful.cups.Printer(
        )

    def get_default_configuration(
                self,
            ):
        return {
            'cups': {
                'printer': self.printer.cups_printer_name,
            },
        }

    def build_argument_parser(
                self,
                configuration,
                argument_parser,
            ):
        argument_parser.add_argument(
            '-o',
            '--option',
            action='append',
            default=[
            ],
            dest='cups_printing_options',
            help='CUPS printing option',
            metavar=(
                'KEY',
                'VALUE',
            ),
            nargs=2,
        )

        argument_parser.add_argument(
            '-p',
            '--pages',
            dest='cups_page_list',
            help='pages to print',
            metavar='PAGE_LIST',
        )

        argument_parser.add_argument(
            '-P',
            '--printer',
            default=configuration['cups']['printer'],
            dest='cups_printer_name',
            help='CUPS printer to use',
            metavar='PRINTER',
        )

        argument_parser.add_argument(
            '-q',
            '--queue',
            action='append_const',
            const=(
                'job-hold-until',
                'indefinite',
            ),
            dest='cups_printing_options',
            help='queue print job instead of printing immediatly',
        )

        argument_parser.add_argument(
            '--skip-first-page',
            action='append_const',
            const=(
                'page-ranges',
                '2-9999',
            ),
            dest='cups_printing_options',
            help='skip first page',
        )

        argument_parser.add_argument(
            'ids',
            help='ID(s) of the document(s) to print',
            metavar='ID',
            nargs='*',
        )

    def run(
                self,
                args,
                paperless_session,
            ):
        tag_id_printed = paperless_session.get_tag_id(
            tag_name='meta:printed',
        )
        tag_id_toprint = paperless_session.get_tag_id(
            tag_name='TOPRINT',
        )

        self.printer.cups_printing_options = {
            cups_printing_option_pair[0]: cups_printing_option_pair[1]
            for cups_printing_option_pair in args.cups_printing_options
        }
        if args.cups_page_list:
            self.printer.cups_printing_options['page-ranges'] = args.cups_page_list
        self.printer.cups_printer_name = args.cups_printer_name
        self.printer.paperless_session = paperless_session

        if args.ids:
            for document_id in args.ids:
                self.printer.print(
                    document_id=document_id,
                )

                document = paperless_session.get_document(
                    document_id=document_id,
                )
                new_tag_ids = new_tags(
                    current_tags=document['tags'],
                    tag_id_printed=tag_id_printed,
                    tag_id_toprint=tag_id_toprint,
                )
                paperless_session.retag_document(
                    correspondent_id=document['correspondent'],
                    document_id=document_id,
                    document_type_id=document['document_type'],
                    tag_ids=new_tag_ids,
                )
        else:
            raise KeyError
            traverse_handler = PrintingTraverser(
                paperless_session=paperless_session,
                printer=self.printer,
            )

            paperless_session.traverse(
                handler=traverse_handler,
                query='tag:TOPRINT NOT tag:TODO',
            )

            for document in traverse_handler.queue:
                new_tag_ids = new_tags(
                    current_tags=document['tags'],
                    tag_id_printed=tag_id_printed,
                    tag_id_toprint=tag_id_toprint,
                )
                paperless_session.retag_document(
                    correspondent_id=document['correspondent'],
                    document_id=document['id'],
                    document_type_id=document['document_type'],
                    tag_ids=new_tag_ids,
                )


def new_tags(
            current_tags,
            tag_id_printed,
            tag_id_toprint,
        ):
    logger.debug(
        'current tags: %s',
        current_tags,
    )

    new_tags = [
        tag
        for tag in current_tags
        if tag != tag_id_toprint and tag != tag_id_printed
    ]
    new_tags.append(
        tag_id_printed,
    )

    logger.debug(
        'new tags: %s',
        new_tags,
    )

    return new_tags


class PrintingTraverser(
            paperful.paperless.TraverseHandler,
        ):
    def __init__(
                self,
                paperless_session,
                printer,
            ):
        self.printer = printer
        self.queue = {
        }

    def handle(
                self,
                document,
                paperless_api_session,
            ):
        document_id = document['id']

        self.printer.print(
            document_id=document_id,
        )

        self.queue.append(
            document,
        )
