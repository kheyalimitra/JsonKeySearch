"""
    This module take json file
    and  will count the total number of metadata types across all records,
    and print them out in order sorted by name.
"""
import json

def generate_queue_from_json_obj(json_obj, json_nesting):
    """
    This is a helper function called by get_json_key_count_from_obj.
    This method iterates through json object and
    generates a queue with all leaf level children for a given json path
    :param json_obj: parsed json object
    :param json_nesting: nested json path separated by '/'
    :return:  meta data types : a key value pair dictionary
    """
    json_path_list = json_nesting.split("/")
    queue = list()
    # add first object to the queue.
    # This queue contains tuple: json node and its corresponding level.
    queue.append((json_obj, 0))
    # this loop will continue until last level has reached
    while queue[0][1] < len(json_path_list):
        new_obj, new_level = queue.pop(0)
        # dequeue each queue entry and enqueue its children in queue
        for obj in new_obj[json_path_list[new_level]]:
            queue.append((obj, new_level+1))
    return queue


def get_json_key_count_from_obj(json_obj, json_nesting, search_key):
    """
    This is the generalization to get_metadata_types_count_from_obj method.
    This method iterates through json object and returns search key and its count in a dictionary
    :param json_obj: parsed json object
    :param json_nesting: nested json path separated by '/'
    :param search_key: The key which needs to be found in nested Json
    :return: meta data types : a key value pair dictionary
    """
    queue = generate_queue_from_json_obj(json_obj, json_nesting)
    metadata_types = {}
    for (entry, _) in queue:
        if search_key in entry:
            if entry[search_key] in metadata_types:
                metadata_types[entry[search_key]] += 1
            else:
                metadata_types[entry[search_key]] = 1
    return metadata_types


def get_metadata_types_count(json_obj):
    """
    This is a helper method for get_metadata_types_count_from_file.
    This method is specific to solve 1 problem:
    "finding "metadata-type" inside "results/metadata" path."
    This method will iterate through json object
    and return the required metadata count in a dictionary
    :param json_obj: parsed json object
    :return: meta data types : a key value pair dictionary
    """
    metadata_types = {}
    results_length = len(json_obj['results'])
    if results_length > 0:
        for entry in json_obj['results']:
            metadata_length = len(entry['metadata'])
            if metadata_length > 0:
                for data_type in entry['metadata']:
                    if data_type['metadata-type'] in metadata_types:
                        metadata_types[data_type['metadata-type']] += 1
                    else:
                        metadata_types[data_type['metadata-type']] = 1
    return metadata_types


def get_key_count_from_file(file_path, json_nesting="results/metadata",
                            search_key="metadata-type", is_sorted=True):
    """
    This method process json file and return search key and its count.
    This method will return metadata type and count in a dictionary object
    :param file_path: json file path
    :param json_nesting: nested json path separated by '/'
    :param search_key: The key which needs to be found in nested Json
    :param is_sorted:
    :return: meta data types : a key value pair dictionary
    """
    with open(file_path) as json_file:
        json_data = json.load(json_file)
        if json_data is not None:
            # We can also use its specific version
            # metadata_types = get_json_key_count_from_obj(json_data)
            # I am using the generic version of it.
            metadata_types = get_json_key_count_from_obj(json_data, json_nesting, search_key)
            if is_sorted:
                sorted(metadata_types)
            return metadata_types
        else:
            print("Error. Cannot read given json file.")
            return None


# main method:
# This is an example of how to use above method
if __name__ == '__main__':
    import sys

    argv_length = len(sys.argv)
    JSON_FILE_PATH = 'assets/json/sample.json'
    SEARCH_KEY = 'metadata-type'
    JSON_PATH = 'results/metadata'
    IS_SORTED = True

    if argv_length > 1:
        JSON_FILE_PATH = sys.argv[1]
    if argv_length > 2:
        SEARCH_KEY = sys.argv[2]
    if argv_length > 3:
        JSON_PATH = sys.argv[3]

    try:
        RESULT = get_key_count_from_file(JSON_FILE_PATH, JSON_PATH,
                                         SEARCH_KEY, IS_SORTED)
        if RESULT:
            for key in RESULT:
                print("%s: %s" % (key, RESULT[key]))
        else:
            print("Error. Unable to get search key count from given json file")
    except IOError:
        print('Sorry, we could not find this file:' + JSON_FILE_PATH)
