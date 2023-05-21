import lib.opensearch as opensearch
import pydash as _
import datetime
import re

def curator_delete(opensearch, prefix, count, today):
    pattern = r"^"+prefix+r".*$"
    filtered_items = [item for item in opensearch.list_index().all_indices if re.match(pattern, item)]
    print(filtered_items)
    if (len(filtered_items)>0):
        for item in filtered_items:
            print(opensearch.list_index().index_info[item])
            # the creation date of each index matches the prefix 
            index_Creation_time = datetime.datetime.fromtimestamp(opensearch.list_index().index_info[item]['age']['creation_date'])
            diff = (today - index_Creation_time.date()).days
            if ( diff >=  count):
                try:  
                    response = opensearch.client.search(index=item)
                    try:
                        response = opensearch.client.indices.delete(index = item)
                        print("deleting index : " + item)
                        print(response)
                    except:
                        print(item +": cant be deleted")
                except: 
                 print("index not found")
            else:
                print("no indices for "+prefix+" in older direction")
    else:
        print("no indices found for "+prefix)

def do_curator_action(opensearch , action, today):
    index_list = {}
    if action['action'] == 'delete_indices':
        for filter_lists in action['filters']:
            if filter_lists['filtertype'] == 'age':
                    index_list['unit_count']=filter_lists['unit_count']      
            if filter_lists['filtertype'] == 'pattern':
                    index_list['value']=filter_lists['value']
    curator_delete(opensearch, index_list['value'] , index_list['unit_count'] , today)
                    

