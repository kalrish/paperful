import sys

import paperful.cli.subcommand


class Subcommand(
            paperful.cli.subcommand.Subcommand,
        ):
    aliases = [
    ]
    description = 'Show detailed information about a document stored in a Paperless instance'
    epilog = None

    def __init__(
                self,
            ):
        pass

    def get_default_configuration(
                self,
            ):
        return {
        }

    def build_argument_parser(
                self,
                configuration,
                argument_parser,
            ):
        argument_parser.add_argument(
            'id',
            help='ID of the document to describe',
            metavar='ID',
        )

    def run(
                self,
                args,
                paperless_session,
            ):
        document = paperless_session.get_document(
            document_id=args.id,
        )

        sys.stdout.write(
            'title        \t',
        )
        sys.stdout.write(
            document['title'],
        )
        sys.stdout.write(
            '\nkind         \t',
        )

        document_type_id = document['document_type']
        if document_type_id:
            document_type_name = paperless_session.get_document_type_name(
                document_type_id=document_type_id,
            )
            sys.stdout.write(
                document_type_name,
            )
        sys.stdout.write(
            '\ncorrespondent\t',
        )

        correspondent_id = document['correspondent']
        if correspondent_id:
            correspondent_name = paperless_session.get_correspondent_name(
                correspondent_id=correspondent_id,
            )
            sys.stdout.write(
                correspondent_name,
            )
        sys.stdout.write(
            '\ntags         \t',
        )

        tag_ids = document['tags']
        for tag_id in tag_ids:
            tag_name = paperless_session.get_tag_name(
                tag_id=tag_id,
            )
            sys.stdout.write(
                tag_name,
            )
            sys.stdout.write(
                '  ',
            )
        sys.stdout.write(
            '\n\n',
        )

        sys.stdout.flush(
        )
