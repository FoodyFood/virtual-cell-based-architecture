'''
Contains a class that represents a tenant, as well as a tenant manager, this 
would typically be part of the control plane.
'''

from random import sample
from uuid import uuid4

from cell_management import cell_manager

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

        # TODO: Currently 2 random cells are picked, ultimately CellManager should pick cells that are of low usage
        tenant: Tenant = Tenant(tenant_id=str(uuid4()), cell_ids=sample(cell_manager.get_list_of_healthy_cell_ids(), 2))
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
