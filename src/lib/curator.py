import lib.opensearch as opensearch
import curator
import pydash as _


def curator_delete(index_list, dry_run):
    try:
        delete_indicies = curator.DeleteIndices(index_list)
        if dry_run:
            delete_indicies.do_dry_run()
        else:
            delete_indicies.do_action()
    except:
        print('Skip for empty index lists.')

def do_curator_action(index_list, action, options):
    try:
        if action['action'] == 'delete_indices':
            print(action['description'])
            for filter_lists in action['filters']:
                if filter_lists['filtertype'] == 'age':
                    index_list.filter_by_age(
                        source=_.get(filter_lists,'source'),
                        direction=filter_lists['direction'],
                        timestring=filter_lists['timestring'],
                        unit=filter_lists['unit'],
                        unit_count=filter_lists['unit_count'],
                        field=filter_lists['field'],
                        stats_result=filter_lists['stats_result'],
                        epoch=filter_lists['epoch'],
                        exclude=_.get(filter_lists, 'exclude', False)
                    )
                if filter_lists['filtertype'] == 'pattern':
                    index_list.filter_by_regex(
                        kind=filter_lists['kind'],
                        value=filter_lists['value'],
                        exclude=_.get(filter_lists, 'exclude', False)
                    )
            curator_delete(index_list, options['dry_run'])
    except:
        print("Skip for empty index")
