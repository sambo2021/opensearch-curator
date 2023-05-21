from opensearchpy import OpenSearch
import curator
import pydash as _

class OpensearchClient:
    def __init__(self, client_info):

        opensearch_hosts = []
        for opensearch_host in _.get(client_info, 'hosts'):
            opensearch_hosts.append({
                'host': opensearch_host,
                'port': _.get(client_info, 'port')
            })

        auth = (_.get(client_info, 'username'), _.get(client_info, 'password')) # For testing only. Don't store credentials in code.
        
        self.client = OpenSearch(
                hosts = opensearch_hosts,
                http_compress = True, # enables gzip compression for request bodies
                http_auth = auth,
                use_ssl = _.get(client_info, 'use_ssl', True),
                verify_certs = _.get(client_info, 'verify_certs', False),
                ssl_assert_hostname = False,
                ssl_show_warn = False
            )

    def list_index(self):
        index_list = curator.IndexList(self.client)
        return index_list
    
    def get_client(self):
        return self.client

