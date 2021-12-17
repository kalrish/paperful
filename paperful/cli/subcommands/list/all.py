import paperful.cli.subcommand
import paperful.cli.subcommands.list


class Subcommand(
            paperful.cli.subcommand.Subcommand,
        ):
    aliases = [
    ]
    description = 'List all documents'
    epilog = None

    def run(
                self,
                args,
                paperless_session,
            ):
        traverse_handler = paperful.cli.subcommands.list.ListingHandler(
        )

        paperless_session.traverse(
            handler=traverse_handler,
        )
