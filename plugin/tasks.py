import requests
import json

# ctx is imported and used in operations
from cloudify import ctx

# put the operation decorator on any function that is a task
from cloudify.decorators import operation
from cloudify.exceptions import NonRecoverableError

@operation
def allocate_ip(python_host,pool_id,**kwargs):
    if pool_id == '':
        ctx.logger.error('pool_id was not provided')
        return;
    try:
        resp = requests.get('http://'+python_host+':5000/api/pools/'+pool_id)
        ips = json.loads(resp.content)['resources']
        ip_to_allocate=''
        for ip in ips:
            if ip['status']=='RELEASED':
                try:
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
                except Exception as e:
                    raise NonRecoverableError('Exception happned {}'.format(getattr(e, 'message', repr(e))))
        if ip_to_allocate == '':
            raise NonRecoverableError('no ips found to allocate')
    except Exception as e:
        raise NonRecoverableError('Exception happned {}'.format(getattr(e, 'message', repr(e))))


@operation
def unallocate_ip(python_host,pool_id,resource_id,**kwargs):
    if pool_id == '':
        ctx.logger.error('pool_id was not provided')
        return;
    if resource_id == '':
        ctx.logger.error('resource_id was not provided')
        return;
    try:
        aresp = requests.put('http://'+python_host+':5000/api/pools/'+pool_id+'/release',
                            json.dumps(dict(
                            id=resource_id
                            )),headers={'content-type':'application/json'})
        if aresp.status_code==200:
            ctx.logger.info('ip with id {} is unallocated'.format(resource_id))
        else:
            ctx.logger.error('ip with id {} was not unallocated'.format(resource_id))
    except Exception as e:
        raise NonRecoverableError('Exception happned {}'.format(getattr(e, 'message', repr(e))))
