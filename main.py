'''
Virtual cell based architecture 
'''

from cell_router import CellRouter
from cell_management import CellManager
from tenant_management import TenantManager
from request_generator import generate_request


NUMBER_OF_TENANTS: int = 10
NUMBER_OF_CELLS: int = 3
NUMBER_OF_REQUESTS_TO_SIMULATE: int = 100


def main():
    '''
    Here we create our virtual cell based architecture, then we create some tenants to
    use it, and finally we simulate requests from those tenants, including some black
    swan events which render cells they hit unhealthy
    '''

    # Data plane
    cell_router: CellRouter = CellRouter()

    # Control plane
    cell_manager: CellManager = CellManager(cell_router=cell_router)
    tenant_manager: TenantManager = TenantManager(cell_manager=cell_manager, cell_router=cell_router)

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

        print(cell_router.route_request(request=generate_request(tenant_manager=tenant_manager)))

    # See how many unhealthy cells we have at the end
    print(f"Unhealthy Cells: {len(cell_manager.get_list_of_unhealthy_cell_ids())}\n")


if __name__ == '__main__':
    main()
