Assignment Plugin
========================

Cloudify plugin project that invokes an api to get ip and assign it to IP of a compute Node.


Creating Python Server that will host the API to be used
-----------------------------
using the following repo :

https://github.com/ahmadiesa-abu/pool_and_resources

some steps needed to be done on the environment
[linux : Centos ]
```
sudo yum install -y postgresql-server postgresql-contrib python-psycopg2 python-devel postgresql-devel python-pip
sudo yum groupinstall -y "Development Tools"
sudo postgresql-setup initdb
sudo vi /var/lib/pgsql/data/pg_hba.conf (change ident to trust -to make the python connect to db-)
sudo systemctl start postgresql
sudo passwd postgres (provide it with password to login and use psql)
```

[linux : Ubuntu ]
```
sudo apt-get install -y postgresql postgresql-contrib python-pip python-psycopg2 libpq-dev python-dev libxml2-dev libxslt-dev libffi-dev
update-rc.d postgresql enable
service postgresql start
sudo passwd postgres (provide it with password to login and use psql)
```

after login we create a user using (```createuser --interactive --pwprompt```)

and then connecting to db (```create database pools```)

modify user and pass in the app/main/config.py

------ if the above is done ( the host will be ready to service requests on port 5000 )




Creating wagon file :
-----------------------------

first we have to install requirments
```
pip install -r dev-requirements.txt
```

then install wagon

```
pip install wagon
```
some dependencies might be required

-- after installation is done we create the wagon file using the following command inside the plugin directory
```
wagon create .
```
the above command will generate the wagon file

Uploading the plugin locally
-- after creating the wagon file we can upload it to cloudify manager using CLI
```
cfy plugins upload -y plugin.yaml [wagon_file_name]
```

Testing the plugin :
-----------------------------
we execute this command that will install the blueprint (assignment_blueprint.yaml)
```
cfy install assignment_blueprint.yaml -d [Deployment Name] -b [Blueprint Name] -i python_host_ip=[ip_address_of python server]
```


Creating blueprint file :
-----------------------------
we write the blueprint by modifying import to include :

```
imports :
  ....
  - plugin: [local plugin name]
```

then we write the node types that we want to implement from the plugin 

```
node_types:
  ...
  derived_from: ...
  properties: ...
  interfaces:
    cloudify.interfaces.lifecycle:
      create:
        implementation: [plugin mapping name].plugin.tasks.[function name]
        inputs:
          ... [inputs for the function]
          
```

and we use the node type inside the node_templates
