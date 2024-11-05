'''
Contains a class that represents a tenant, as well as a tenant manager, this 
would typically be part of the control plane.
'''

from uuid import uuid4

class Tenant():
    '''
    A tenant and their information.
    '''

    def __init__(self, cell_router, tenant_id: str, cell_ids: list[int]):
        self.tenant_id: str = tenant_id
        self.cell_ids: list[int] = cell_ids

        cell_router.register_tenant(tenant_id=tenant_id, cell_ids=cell_ids)

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

    def __init__(self, cell_manager, cell_router):
        self.list_of_tenants: list = []
        self.cell_manager = cell_manager
        self.cell_router = cell_router

    def add_tenant(self):
        '''
        This adds a new tenant with a random tenant_id and a random cell_id
        '''

        # TODO: Currently 2 random cells are picked, ultimately CellManager should pick cells that are of low usage
        tenant: Tenant = Tenant(cell_router=self.cell_router, tenant_id=str(uuid4()), cell_ids=self.cell_manager.assign_cells_to_new_tenant())
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
