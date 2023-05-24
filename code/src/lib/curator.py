import datetime
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def curator_delete(opensearch, prefix, count, today):
    pattern = r"^"+prefix+r".*$"
    filtered_items = [item for item in opensearch.list_index().all_indices if re.match(pattern, item)]
    if (len(filtered_items)>0):
        for item in filtered_items:
            # the creation date of each index matches the prefix
            index_Creation_time = datetime.datetime.fromtimestamp(opensearch.list_index().index_info[item]['age']['creation_date'])
            diff = (today - index_Creation_time.date()).days
            if ( diff >=  count):
                    try:
                        response = opensearch.client.indices.delete(index = item)
                        logger.info("Deleting index : " + item)
                        logger.info(response)
                    except:
                        logger.warning(item +": cant be deleted")
            else:
                logger.info("Index "+item+" is not in older direction")
    else:
        logger.warning("No Indices Found for "+prefix)

def do_curator_action(opensearch , action, today):
    index_list = {}
    if action['action'] == 'delete_indices':
        for filter_lists in action['filters']:
            if filter_lists['filtertype'] == 'age':
                    index_list['unit_count']=filter_lists['unit_count']
            if filter_lists['filtertype'] == 'pattern':
                    index_list['value']=filter_lists['value']
    curator_delete(opensearch, index_list['value'] , index_list['unit_count'] , today)
