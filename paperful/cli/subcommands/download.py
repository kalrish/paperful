import paperful.cli.subcommand
import paperful.paperless


class Subcommand(
            paperful.cli.subcommand.Subcommand,
        ):
    aliases = [
        'dl',
    ]
    description = 'Retrieve a document stored in Paperless'
    epilog = None

    def build_argument_parser(
                self,
                configuration,
                argument_parser,
            ):
        argument_parser.add_argument(
            '-T',
            '--original',
            dest='type_name',
            help='whether to fetch the original document or the archival copy',
            metavar='DOCUMENT_TYPE',
            required=False,
        )

        argument_parser.add_argument(
            'ids',
            help='ID(s) of the document(s) to print',
            metavar='ID',
            nargs='*',
        )

        argument_parser.add_argument(
            'path',
            help='path to the document file',
            metavar='PATH',
        )

    def run(
                self,
                args,
                paperless_session,
            ):
        paperless_session.download(
            path=args.path,
        )
