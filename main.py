'''
Virtual cell based architecture 
'''

from random import randrange, sample
from uuid import uuid4

from cell_management import Cell, cell_manager
from tenant_management import Tenant, tenant_manager


NUMBER_OF_TENANTS: int = 10
NUMBER_OF_CELLS: int = 3
NUMBER_OF_REQUESTS_TO_SIMULATE: int = 15




def generate_request() -> dict:
    '''
    Generates a random request for a random tenant
    '''

    request = {
        'tenant_id': tenant_manager.get_list_of_tenant_ids()[randrange(0, NUMBER_OF_TENANTS)],
        'request_id': uuid4(),
        'data': f'{randrange(1, 6)} bag(s) of chips'
    }
    return request


def main():
    # Add cells
    for _ in range(NUMBER_OF_CELLS):
        cell_manager.add_cell()

    # Add tenants
    for _ in range(NUMBER_OF_TENANTS):
        tenant_manager.add_tenant()

    # Generate and send requests to the cell router
    for __ in range(NUMBER_OF_REQUESTS_TO_SIMULATE):
        print(
            "Healthy Cell Count:", len(cell_manager.get_list_of_healthy_cell_ids()), "-", 
            "Healthy Cell IDs:", cell_manager.get_list_of_healthy_cell_ids(), "-",
            "Unhealthy Cell Count:", len(cell_manager.get_list_of_unhealthy_cell_ids()), "-", 
            "Unhealthy Cell IDs:", cell_manager.get_list_of_unhealthy_cell_ids()
        )

        cell_router(request=generate_request())

    # See how many unhealthy cells we have at the end
    print(f"Unhealthy Cells: {len(cell_manager.get_list_of_unhealthy_cell_ids())}\n")


if __name__ == '__main__':
    main()