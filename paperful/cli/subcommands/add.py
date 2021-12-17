import paperful.cli.subcommand
import paperful.paperless


class Subcommand(
            paperful.cli.subcommand.Subcommand,
        ):
    aliases = [
        'upload',
        'ul',
    ]
    description = 'Add a document to a Paperless instance'
    epilog = 'Inbox tags (such as `TODO`) are not added by default.'

    def build_argument_parser(
                self,
                configuration,
                argument_parser,
            ):
        argument_parser.add_argument(
            '-t',
            '--title',
            dest='title',
            help='title',
            metavar='TITLE',
            required=False,
        )

        argument_parser.add_argument(
            '-T',
            '--type',
            dest='type_name',
            help='document type',
            metavar='DOCUMENT_TYPE',
            required=False,
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
        paperless_session.add(
            path=args.path,
        )
