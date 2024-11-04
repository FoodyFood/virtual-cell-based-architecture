'''
This will generate requests, a request for 5 bags of chips os considered a black swan
and will render any cell it hits as unhealthy. Only 1 tenant will be able to generate 
these requests and will slowly poison their cells.
'''

from uuid import uuid4
from random import sample, randrange

from tenant_management import tenant_manager

def generate_request() -> dict:
    '''
    Generates a random request for a random tenant
    '''

    tenant_id: str = sample(tenant_manager.get_list_of_tenant_ids(), 1)[0]

    if tenant_id == tenant_manager.get_list_of_tenant_ids()[2]:
        request = {
            'tenant_id': tenant_id,
            'request_id': str(uuid4()),
            'data': f'{randrange(1, 6)} bag(s) of chips'
        }
    else:
        request = {
            'tenant_id': tenant_id,
            'request_id': str(uuid4()),
            'data': f'{randrange(1, 5)} bag(s) of chips'
        }

    return request
