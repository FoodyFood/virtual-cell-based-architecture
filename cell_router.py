'''
Virtual cell based architecture 
'''

from random import randrange, sample
from uuid import uuid4


NUMBER_OF_TENANTS: int = 10
NUMBER_OF_CELLS: int = 3
NUMBER_OF_REQUESTS_TO_SIMULATE: int = 15


class Tenant():
    '''
    A tenant and their information.
    '''

    def __init__(self, tenant_id: str, cell_ids: list[int]):
        self.tenant_id: str = tenant_id
        self.cell_ids: list[int] = cell_ids

    def get_cell_ids(self):
        '''
        Returns a list of the tenants assigned cells
        '''

        return self.cell_ids

    def get_tenant_id(self):
        '''
        Returns the tenant id as a string
        '''

        return self.tenant_id

class TenantManager():
    '''
    Manages tenants, part of the control place.
    '''

    list_of_tenants: list = []

    def add_tenant(self):
        '''
        This adds a new tenant with a random tenant_id and a random cell_id
        '''

        tenant: Tenant = Tenant(tenant_id=str(uuid4()), cell_ids=sample(range(0, NUMBER_OF_CELLS), 2))
        self.list_of_tenants.append(tenant)

    def get_list_of_tenants(self):
        '''
        Returns the complete list of tenants as a list of tenant objects
        '''

        return self.list_of_tenants

    def get_list_of_tenant_ids(self) -> list[str]:
        '''
        Returns a list of all current tenant ids
        '''

        list_of_tenant_ids: list[str] = []
        for tenant in self.list_of_tenants:
            list_of_tenant_ids.append(tenant.get_tenant_id())

        return list_of_tenant_ids

    def get_cell_ids_for_tenant(self, tenant_id: str) -> list[int]:
        '''
        Gets the cells assigned to a tenant
        '''

        for tenant in self.list_of_tenants:
            if tenant_id == tenant.get_tenant_id():
                return tenant.get_cell_ids()

        return []

tenant_manager: TenantManager = TenantManager()


class Cell():
    '''
    This represents a single cell
    '''

    def __init__(self, cell_id: int):
        self.cell_id: int = cell_id
        self.health: str = "Healthy"

    def get_cell_id(self):
        return self.cell_id
    
    def get_cell_health(self):
        return self.health

    def request_handler(self, request: dict):
        '''
        This is the ingress of a cell, it could be an ALB in the real world.

        If the order is for 5 bags of chips, it is a black swan request and will kill the cell
        '''

        if request['data'].startswith('5'):
            print(f"Health - Cell {self.cell_id} - Unhealthy")
            self.health = "Unhealthy"

        print(f"Handled Request ID: {request['request_id']} Tenant: {request['tenant_id']} Cell: {self.cell_id} Data: {request['data']}")

class CellManager():
    '''
    Manages the current cells, part of the control plane.
    '''
    list_of_cells: list[Cell] = []

    def add_cell(self):
        cell: Cell = Cell(cell_id=len(self.list_of_cells))
        self.list_of_cells.append(cell)

    def get_list_of_cells(self):
        return self.list_of_cells

    def get_list_of_healthy_cells(self):
        list_of_healthy_cells: list = []
        for cell in self.list_of_cells:
            if cell.get_cell_health() == "Healthy":
                list_of_healthy_cells.append(cell)
        return list_of_healthy_cells

    def get_list_of_unhealthy_cells(self):
        list_of_unhealthy_cells: list = []
        for cell in self.list_of_cells:
            if cell.get_cell_health() == "Unhealthy":
                list_of_unhealthy_cells.append(cell)
        return list_of_unhealthy_cells

cell_manager: CellManager = CellManager()


def cell_router(request: dict):
    '''
    This routes a request to a cell based on cell-tenant affinity, it is the ingress 
    to the system as a whole, 'the thinnest possible layer'.
    '''

    list_of_healthy_cells: list[Cell] = cell_manager.get_list_of_healthy_cells()
    healthy_cell_ids = []
    for healthy_cell in list_of_healthy_cells:
        healthy_cell_ids.append(healthy_cell.cell_id)
    print(healthy_cell_ids)

    current_tenants_cell_ids: list[int] = tenant_manager.get_cell_ids_for_tenant(tenant_id=request['tenant_id'])

    for cell_id in current_tenants_cell_ids:
        for cell in list_of_healthy_cells:
            if cell_id == cell.get_cell_id():
                cell.request_handler(request)
                return

    print(
        f"Unhandled Request ID: {request['request_id']},",
        f"Tenant ID: {request['tenant_id']},",
        f"Cell IDs: {tenant_manager.get_cell_ids_for_tenant(tenant_id=request['tenant_id'])}",
    )


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

    # Add tenants
    for _ in range(NUMBER_OF_TENANTS):
        tenant_manager.add_tenant()

    # Add cells
    for _ in range(NUMBER_OF_CELLS):
        cell_manager.add_cell()

    # Generate and send requests to the cell router
    for __ in range(NUMBER_OF_REQUESTS_TO_SIMULATE):
        cell_router(request=generate_request())

    # See how many unhealthy cells we have at the end
    print(f"Unhealthy Cells: {len(cell_manager.get_list_of_unhealthy_cells())}\n")


if __name__ == '__main__':
    main()
