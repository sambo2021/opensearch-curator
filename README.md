# opensearch-curator
## my case that opnesearch has a private DNS can be reachable from inisde aws account 
## if u want to deploy app on ec2 instance or to run it on lambda function u can use dir code 
run 'python3 ./src/main.py -c ./config/etc/curator/config.yml -d ./config/etc/curator/action_file.yml'
## if u want to use it as a cronejob on eks running on the same account u can use dir chart 
## if eks or ec2 running on another account u need to define vpc endpoint and a record in ur hosted zone "will be added details later"
