'''
The thinnest possible layer, the cell router, this sits between the real world
and your cells, it takes an inbound request and determines which cell it should
be routed to.
'''

class CellRouter():
    '''
    This routes a request to a cell based on a map of tenants and cells.
    '''

    def __init__(self):
        self.list_of_cells: list = []
        self.list_of_tenants: list = []
        self.list_of_unhealthy_cells: list[int] = []

    def register_cell(self, cell_id: int, request_handler):
        '''
        When a new cell is provisioned, it registers with the router
        '''

        self.list_of_cells.append((cell_id, request_handler))
        print(f"Cell registered with router - Cell ID: {cell_id} - Request Handler: {request_handler}")

    def register_tenant(self, tenant_id: str, cell_ids: list[int]):
        '''
        When a new tenant is provisioned, it registers with the router
        '''

        self.list_of_tenants.append((tenant_id, cell_ids))
        print(f"Tenant registered with router - Tenant ID: {tenant_id} - Cell IDs {cell_ids}")

    def route_request(self, request: dict):
        '''
        This routes a request to a cell based on cell-tenant affinity, it is the ingress 
        to the system as a whole, 'the thinnest possible layer'.
        '''

        # Get the list of all current healthy cells
        list_of_healthy_cells: list = []
        for cell in self.list_of_cells:
            print(cell)
            for unhealthy_cell in self.list_of_unhealthy_cells:
                print(cell[0], unhealthy_cell[0])
                if cell[0] != unhealthy_cell[0]:
                    list_of_healthy_cells.append(cell)
                    print(cell, list_of_healthy_cells)

        # Get the list of cells the tenant is assigned
        tenants_cell_ids: list[int] = []
        for tenant in self.list_of_tenants:
            if tenant[0] == request['tenant_id']:
                tenants_cell_ids = tenant[1]

        # Try find a healthy cell to handle the request
        response: str = ""
        for cell_id in tenants_cell_ids:
            for healthy_cell in list_of_healthy_cells:
                if cell_id == healthy_cell[0]:
                    response = healthy_cell[1](request=request)
                    # If the response is bad, we add the cel to the unhealthy cells list
                    if response.startswith("CELL FAULIRE"):
                        self.list_of_unhealthy_cells.append(healthy_cell[0])
                    return response


        # If there were no healthy cells to handle the request, return a routing error
        return(
            "ROUTER FAILURE - No healthy cells found, - "
            f"Unhandled Request ID: {request['request_id']}, - "
            f"Tenant: {request['tenant_id']}, - "
            f"Data: {request['data']}"
        )
