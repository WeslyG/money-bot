from datetime import datetime
from elasticsearch import Elasticsearch

from os import environ

from config.config import Config
class Database():
    def __init__(self, index: str, connection_string: str, config: Config):
        self.index = index
        self.es = Elasticsearch(hosts=connection_string,
                                basic_auth=(config.elastic_user, config.elastic_password),
                                ca_certs='http_ca.crt')

    def write(self, data: dict):
        resp = self.es.index(index=self.index, document=data)
        return resp['result']

    def get_doc_by_id(self, doc_id: str):
        resp = self.es.get(index=self.index, id=doc_id)
        print(resp['_source'])

    def refresh_index(self):
        self.es.indices.refresh(index=self.index)

    def search(self, request: dict | None = {"match_all": {}}):
        resp = self.es.search(index=self.index, query=request)
        print("Got %d Hits:" % resp['hits']['total']['value'])
        for hit in resp['hits']['hits']:
            print(hit["_source"])