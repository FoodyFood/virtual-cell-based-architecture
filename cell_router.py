'''
The thinnest possible layer, the cell router, this sits between the real world
and your cells, it takes an inbound request and determines which cell it should
be routed to.
'''

from cell_management import Cell, cell_manager
from tenant_management import tenant_manager


def cell_router(request: dict):
    '''
    This routes a request to a cell based on cell-tenant affinity, it is the ingress 
    to the system as a whole, 'the thinnest possible layer'.
    '''

    # Get the list of all current healthy cells
    list_of_healthy_cell_ids: list[Cell] = cell_manager.get_list_of_healthy_cell_ids()

    # Get the list of cells the tenant is assigned to
    tenants_cell_ids: list[int] = tenant_manager.get_cell_ids_for_tenant(
        tenant_id=request['tenant_id']
    )

    # Try find a healthy cell to handle the request
    for cell_id in tenants_cell_ids:
        for healthy_cell_id in list_of_healthy_cell_ids:
            if cell_id == healthy_cell_id:
                request_handler = cell_manager.get_cell_handler(cell_id=cell_id)
                if request_handler is not None:
                    return request_handler(request=request)

    # If there were no healthy cells, return an error
    return(
        "ROUTER FAILURE - No healthy cells found, -"
        f"Unhandled Request ID: {request['request_id']}, - "
        f"Tenant: {request['tenant_id']}, - "
        f"Data: {request['data']}"
    )
