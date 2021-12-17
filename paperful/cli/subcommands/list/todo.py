import paperful.cli.subcommand
import paperful.cli.subcommands.list


class Subcommand(
            paperful.cli.subcommand.Subcommand,
        ):
    aliases = [
    ]
    description = 'List documents whose metadata must be reviewed'
    epilog = 'All documents listed have the tag `TODO`.'

    def run(
                self,
                args,
                paperless_session,
            ):
        tag_id_todo = paperless_session.get_tag_id(
            tag_name='TODO',
        )

        traverse_handler = paperful.cli.subcommands.list.ListingHandler(
            omit_tags = {
                tag_id_todo,
            },
        )

        paperless_session.traverse(
            handler=traverse_handler,
            query='tag:TODO',
        )
