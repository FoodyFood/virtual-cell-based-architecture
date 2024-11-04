'''
Virtual cell based architecture 
'''

from cell_management import cell_manager
from tenant_management import tenant_manager
from cell_router import cell_router
from request_generator import generate_request


NUMBER_OF_TENANTS: int = 10
NUMBER_OF_CELLS: int = 3
NUMBER_OF_REQUESTS_TO_SIMULATE: int = 150


def main():
    '''
    Here we create our virtual cell based architecture, then we create some tenants to
    use it, and finally we simulate requests from those tenants, including some black
    swan events which render cells they hit unhealthy
    '''

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

        print(cell_router(request=generate_request()))

    # See how many unhealthy cells we have at the end
    print(f"Unhealthy Cells: {len(cell_manager.get_list_of_unhealthy_cell_ids())}\n")


if __name__ == '__main__':
    main()
