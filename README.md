# JsonKeySearch
This project solve the following problem : Given a json file, it parse and find the frequency of given search key 

Workflow:
---------
Assets folder contains json folder. This has `sample.json`
In `parse_json.py`, main  calls  `get_key_count_from_file`. This in turn calls `get_json_key_count_from_obj` [ or we can use `get_metadata_types_count` for a particular case mentioned in Specian node, section 1] to get the key and its frequency. 

 
How to Run this project:
--------------------------
From command line, please run `python parse_json.py  <json file path> <search key> <nested json path>` 
Default File path is : 'assets/json/sample.json'
Default Search key is : 'metadata-type'
Default nested json path is: 'results/metadata'

Example: 
```
$ python parse_json.py assets/json/sample.json  metadata-type results/metadata
```

Expected output:
-----------------
If you are using sample.json (which is added in asses/json folder) and searching for  "metadta-types" , the output looks like 
```
attribute: 148
constraint: 166
element: 201
```

Special Note
------------
In this file I have written two ways of solving it. 
1. `get_metadata_types_count` This method is specific to find `metadata_types` frequency from a json file named `sample.json` 
2. `get_json_key_count_from_obj` This is the generic version of finding key from a nested json object and finding its frequency. 

3. I have not added unit test case yes. 

