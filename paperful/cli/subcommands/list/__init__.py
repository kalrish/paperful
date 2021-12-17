import sys

import paperful.cli.subcommand
import paperful.paperless


class Subcommand(
            paperful.cli.subcommand.Subcommand,
        ):
    aliases = [
    ]
    description = 'List documents stored in a Paperless instance'
    epilog = None


class ListingHandler(
            paperful.paperless.TraverseHandler,
        ):
    def __init__(
                self,
                omit_tags=set(
                ),
            ):
        self.correspondent_cache = {
        }
        self.document_type_cache = {
        }
        self.tags_cache = {
        }

        self.omit_tags = omit_tags

    def handle(
                self,
                document,
                paperless_api_session,
            ):
        document_id = document['id']

        sys.stdout.write(
            f'id           \t{document_id}\ntitle        \t',
        )
        sys.stdout.write(
            document['title'],
        )
        sys.stdout.write(
            '\nkind         \t',
        )

        document_type_id = document['document_type']
        if document_type_id:
            try:
                document_type_name = self.document_type_cache[document_type_id]
            except KeyError:
                document_type_name = paperless_api_session.get_document_type_name(
                    document_type_id=document_type_id,
                )
                self.document_type_cache[document_type_id] = document_type_name
            sys.stdout.write(
                document_type_name,
            )
        sys.stdout.write(
            '\ncorrespondent\t',
        )

        correspondent_id = document['correspondent']
        if correspondent_id:
            try:
                correspondent_name = self.correspondent_cache[correspondent_id]
            except KeyError:
                correspondent_name = paperless_api_session.get_correspondent_name(
                    correspondent_id=correspondent_id,
                )
                self.correspondent_cache[correspondent_id] = correspondent_name
            sys.stdout.write(
                correspondent_name,
            )
        sys.stdout.write(
            '\ntags         \t',
        )

        tag_ids = document['tags']
        for tag_id in tag_ids:
            if tag_id not in self.omit_tags:
                try:
                    tag_name = self.tags_cache[tag_id]
                except KeyError:
                    tag_name = paperless_api_session.get_tag_name(
                        tag_id=tag_id,
                    )
                    self.tags_cache[tag_id] = tag_name
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
