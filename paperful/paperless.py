import logging

import requests

import paperful.requests


class Session(
        ):
    def __init__(
                self,
                paperless_api_token,
                paperless_api_url,
            ):
        self.logger = logging.getLogger(
            __name__,
        )

        self.paperless_api_url = paperless_api_url

        self.requests_session = requests.Session(
        )

        self.requests_session.hooks['response'].append(
            paperful.requests.response_hook,
        )

        self.requests_session.headers = {
            'Authorization': 'Token ' + paperless_api_token,
            'Accept': 'application/json; version=2',
        }

        self.printopt_tag_ids = self.get_printopt_tag_ids(
        )

    def get_correspondent_name(
                self,
                correspondent_id,
            ):
        response = self.requests_session.get(
            f'{self.paperless_api_url}/api/correspondents/{correspondent_id}/',
        )

        assert response.status_code == requests.codes.ok

        response_data = response.json(
        )

        return response_data['name']

    def get_document_type_name(
                self,
                document_type_id,
            ):
        response = self.requests_session.get(
            f'{self.paperless_api_url}/api/document_types/{document_type_id}/',
        )

        assert response.status_code == requests.codes.ok

        response_data = response.json(
        )

        return response_data['name']

    def get_document(
                self,
                document_id,
            ):
        response = self.requests_session.get(
            f'{self.paperless_api_url}/api/documents/{document_id}/',
        )

        assert response.status_code == requests.codes.ok

        response_data = response.json(
        )

        return response_data

    def get_tag_name(
                self,
                tag_id,
            ):
        response = self.requests_session.get(
            f'{self.paperless_api_url}/api/tags/{tag_id}/',
        )

        assert response.status_code == requests.codes.ok

        response_data = response.json(
        )

        return response_data['name']

    def get_tag_id(
                self,
                tag_name,
            ):
        response = self.requests_session.get(
            self.paperless_api_url + '/api/tags/',
            params={
                'name__iexact': tag_name,
            },
        )

        assert response.status_code == requests.codes.ok

        response_data = response.json(
        )

        assert response_data['count'] == 1

        tag_id = response_data['results'][0]['id']

        self.logger.debug(
            'tag ID: `%s`: %s',
            tag_name,
            tag_id,
        )

        return tag_id

    def get_printopt_tag_ids(
                self,
            ):
        all_printopt_tag_ids = {
        }

        url = self.paperless_api_url + '/api/tags/'
        while url:
            printopt_tag_ids, url = self.get_printopt_tag_ids_pager(
                url=url,
            )

            all_printopt_tag_ids.update(
                printopt_tag_ids,
            )

        return all_printopt_tag_ids

    def get_printopt_tag_ids_pager(
                self,
                url,
            ):
        printopt_tag_ids = {
        }

        response = self.requests_session.get(
            url,
            params={
                'name__istartswith': 'printopt:',
            },
        )

        assert response.status_code == requests.codes.ok

        response_data = response.json(
        )

    #    printopt_tag_ids = {
    #        tag['name'][9:]: tag['id']
    #        for tag in response_data['results']
    #    }

        for tag in response_data['results']:
            printopt = tag['name'][9:]
            self.logger.debug(
                'printopt found: %s',
                printopt,
            )

            printopt_tag_ids[printopt] = tag['id']

        return (
            printopt_tag_ids,
            response_data['next'],
        )

    def retag_document(
                self,
                correspondent_id,
                document_id,
                document_type_id,
                tag_ids,
            ):
        response = self.requests_session.put(
            self.paperless_api_url + '/api/documents/' + str(document_id) + '/',
            json={
                'correspondent': correspondent_id,
                'document_type': document_type_id,
                'tags': tag_ids,
            },
        )

        assert response.status_code == requests.codes.ok

    def traverse(
                self,
                handler,
                query=None,
            ):
        url = self.paperless_api_url + '/api/documents/'
        while url:
            url = self.traverse_next(
                handler=handler,
                query=query,
                url=url,
            )

    def traverse_next(
                self,
                handler,
                query,
                url,
            ):
        response = self.requests_session.get(
            url,
            params={
                'query': query,
            },
        )

        if response.status_code == requests.codes.ok:
            response_data = response.json(
            )

            documents = response_data['results']
            for document in documents:
                handler.handle(
                    document=document,
                    paperless_api_session=self,
                )

            return response_data['next']
        else:
            self.logger.error(
                'lalala: %s',
                response.text,
            )


class TraverseHandler(
        ):
    def handle(
                self,
                document,
                paperless_api_session,
            ):
        pass
