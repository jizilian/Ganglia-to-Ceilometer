import Ganglia_Ceilometer_Plugin
from ceilometerclient import client
from os import environ as env
from ceilometerclient.v2 import samples

CREATE_SAMPLE = {u'counter_name': u'cpu_util',
                  u'user_id': u'b790cc79594f4d79bbf66cfdaf1f91bc',
                  u'resource_id': u'b8f27163-ea06-48d8-b561-aec0da5f7d08',
                  u'timestamp': u'2015-12-13T10:40:00',
                  u'source': u'openstack',
                  u'message_id': u'54558a1c-6ef3-11e2-9875-5453ed1bbb5f',
                  u'counter_unit': u'%',
                  u'counter_volume': 1.0,
                  u'project_id': u'033a0cdd90384488ac1df526a3c17aa2',
                  u'resource_metadata': {u'tag': u'self.counter',
                                         u'display_name': u'test-server'},
                  u'counter_type': u'gauge'}

def insert_into_ceilometer():
    keystone = {}
    keystone['os_username']=env['OS_USERNAME']
    keystone['os_password']=env['OS_PASSWORD']
    keystone['os_auth_url']=env['OS_AUTH_URL']
    keystone['os_tenant_name']=env['OS_TENANT_NAME']
    cclient = client.get_client('2', **keystone)
    query = [dict(field='meter',op='eq',value='cpu_util')]
    cclient.samples.create(**CREATE_SAMPLE)
    meters = cclient.samples.list(meter_name='cpu_util', limit=1)
    print meters

def main():
    gcp = Ganglia_Ceilometer_Plugin.Ganglia_Ceilometer_Plugin()
    results = gcp.get_xml_from_ganglia("localhost", 8649)
    CREATE_SAMPLE['counter_volume'] = 100 - float(results['cpu_idle'])
    insert_into_ceilometer()

if __name__ == "__main__":
    main()
