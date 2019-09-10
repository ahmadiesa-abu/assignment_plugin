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
