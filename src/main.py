import lib.curator as curator
import lib.config_parser as config_parser
from lib.opensearch import OpensearchClient
import pydash as _
import yaml
import argparse
import datetime


def get_parser():
    '''
    The argparse module’s support for command-line interfaces is built around an instance of argparse.ArgumentParser. 
    It is a container for argument specifications and has options that apply the parser as whole:
    '''
    parser = argparse.ArgumentParser(description='Opensearch Curator')
    parser.add_argument('-c', '--config',required=True)
    parser.add_argument('-d', '--dry-run',required=False, action='store_true')
    parser.add_argument('action_path', metavar='action_file_path', help='an integer for the accumulator')
    return parser

parser = get_parser()
args = parser.parse_args()
config = config_parser.parse_config(args.config)
# print(_.get(config, 'client'))
#dry_run = args.dry_run
dry_run = False
action_path = args.action_path
# print(config_path)
options = {}
options['dry_run'] = dry_run
opensearch = OpensearchClient(_.get(config, 'client'))


#using today date at aech day to delete old indices
today = datetime.datetime.now().date()

with open(action_path, "r") as stream:
    try:
        actions = yaml.safe_load(stream)
        for action_list in actions['actions']:
            curator.do_curator_action(opensearch , actions['actions'][action_list], today )
    except yaml.YAMLError as exc:
        print(exc)