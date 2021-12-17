import paperful.cli.subcommand
import paperful.cli.subcommands.list


class Subcommand(
            paperful.cli.subcommand.Subcommand,
        ):
    aliases = [
    ]
    description = 'List documents ready to be printed'
    epilog = 'All documents listed have the tag `TOPRINT`.'

    def run(
                self,
                args,
                paperless_session,
            ):
        tag_id_toprint = paperless_session.get_tag_id(
            tag_name='TOPRINT',
        )

        traverse_handler = paperful.cli.subcommands.list.ListingHandler(
            omit_tags = {
                tag_id_toprint,
            },
        )

        paperless_session.traverse(
            handler=traverse_handler,
            query='tag:TOPRINT NOT tag:TODO',
        )
