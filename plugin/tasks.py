########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

import requests
import json

# ctx is imported and used in operations
from cloudify import ctx

# put the operation decorator on any function that is a task
from cloudify.decorators import operation


@operation
def allocate_ip(pool_id,**kwargs):
    if pool_id == '':
        ctx.logger.error('pool_id was not provided')
        return;
    resp = requests.get('http://172.15.21.158:5000/api/pools/'+pool_id)
    ips = json.loads(resp.content)['resources']
    ip_to_allocate=''
    for ip in ips:
        if ip['status']=='RELEASED':
            aresp = requests.put('http://172.15.21.158:5000/api/pools/'+pool_id+'/allocate',
                        json.dumps(dict(
                        id=ip['id']
        		)),headers={'content-type':'application/json'})
            if aresp.status_code==200:
               ip_to_allocate=ip['ip_address']   
               ctx.instance.runtime_properties['ip'] = ip_to_allocate   
               ctx.instance.runtime_properties['ip_id'] = ip['id']
               ctx.logger.info('ip {} is allocated'.format(ip_to_allocate))
               break;
    if ip_to_allocate == '':
       ctx.logger.error('no ips found to allocate')


@operation
def unallocate_ip(pool_id,resource_id,**kwargs):
    if pool_id == '':
        ctx.logger.error('pool_id was not provided')
        return;
    if resource_id == '':
        ctx.logger.error('resource_id was not provided')
        return;
    aresp = requests.put('http://172.15.21.158:5000/api/pools/'+pool_id+'/release',
                        json.dumps(dict(
                        id=resource_id
                        )),headers={'content-type':'application/json'})
    if aresp.status_code==200:
       ctx.logger.info('ip with id {} is unallocated'.format(resource_id))
    else:
       ctx.logger.error('ip with id {} was not unallocated'.format(resource_id))
