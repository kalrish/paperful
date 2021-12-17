import logging
import os
import tempfile

import cups

logger = logging.getLogger(
    __name__,
)


class Printer(
        ):
    def __init__(
                self,
            ):
        self.cups_connection = cups.Connection(
        )
        self.cups_printer_name = self.cups_connection.getDefault(
        )

    def print(
                self,
                document_id,
            ):
        url = f'{self.paperless_session.paperless_api_url}/api/documents/{document_id}/download/'

        response = self.paperless_session.requests_session.get(
            url,
            params={
                'original': 'true',
            },
            stream=True,
        )

        content_type = response.headers['content-type']
        if content_type == 'application/pdf':
            file, path = tempfile.mkstemp(
                suffix='.pdf',
            )

            iterator = response.iter_content(
                chunk_size=8192,
            )
            for chunk in iterator:
                os.write(
                    file,
                    chunk,
                )

            os.close(
                file,
            )

            self.cups_connection.printFile(
                filename=path,
                options=self.cups_printing_options,
                printer=self.cups_printer_name,
                title=f'paperless-{document_id}',
            )

            os.remove(
                path,
            )
        else:
            logger.warning(
                'cannot print because type: %s',
                content_type,
            )

        response.close(
        )
