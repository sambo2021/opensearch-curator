from opensearchpy import OpenSearch
# from opensearchpy import  AWSV4SignerAuth, RequestsHttpConnection
import yaml
import boto3
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

        # if _.get(client_info, 'aws_auth'):
        #     credentials = boto3.Session().get_credentials()
        #     auth = AWSV4SignerAuth(credentials, _.get(client_info, 'region', 'ap-northeast-1'), _.get(client_info, 'service', 'es'))
        #     self.client = OpenSearch(
        #         hosts = opensearch_hosts,
        #         http_auth = auth,
        #         use_ssl = True,
        #         verify_certs = True,
        #         connection_class = RequestsHttpConnection,
        #         pool_maxsize = 20
        #     )           
        # else:
        auth = (_.get(client_info, 'username'), _.get(client_info, 'password')) # For testing only. Don't store credentials in code.

        #     # Provide a CA bundle if you use intermediate CAs with your root CA.
        #     # If this is not given, the CA bundle is is discovered from the first available
        #     # following options:
        #     # - OpenSSL environment variables SSL_CERT_FILE and SSL_CERT_DIR
        #     # - certifi bundle (https://pypi.org/project/certifi/)
        #     # - default behavior of the connection backend (most likely system certs)
        #     # ca_certs_path = '/full/path/to/root-ca.pem'

        #     # Optional client certificates if you don't want to use HTTP basic authentication.
        #     # client_cert_path = '/full/path/to/client.pem'
        #     # client_key_path = '/full/path/to/client-key.pem'

        #     # Create the client with SSL/TLS enabled, but hostname verification disabled.
        #     self.client = OpenSearch(
        #         hosts = opensearch_hosts,
        #         http_compress = True, # enables gzip compression for request bodies
        #         # http_auth = auth,
        #         # # client_cert = client_cert_path,
        #         # # client_key = client_key_path,
        #         use_ssl = _.get(client_info, 'use_ssl', True),
        #         verify_certs = _.get(client_info, 'verify_certs', False),
        #         ssl_assert_hostname = False,
        #         ssl_show_warn = False
        #     )
        
        self.client = OpenSearch(
                hosts = opensearch_hosts,
                http_compress = True, # enables gzip compression for request bodies
                http_auth = auth,
                # # client_cert = client_cert_path,
                # # client_key = client_key_path,
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

    # def create_index(self, index_name):
    #     # Create an index with non-default settings.
    #     index_body = {
    #         'settings': {
    #             'index': {
    #             'number_of_shards': 4
    #             }
    #         }
    #     }

    #     response = self.client.indices.create(index_name, body=index_body)
    #     print('Creating index:')
    #     print(response)
