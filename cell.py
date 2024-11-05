'''
Contains a class that represents a cell, it has the ability to handle a request
and also to provide cell health.
'''

class Cell():
    '''
    This represents a single cell
    '''

    def __init__(self, cell_router, cell_id: int):
        self.cell_id: int = cell_id
        self.health: str = "Healthy"
        
        cell_router.register_cell(cell_id=cell_id, request_handler=self.request_handler)

    def get_cell_id(self):
        '''
        Returns the integer that identifies the cell
        '''

        return self.cell_id

    def get_cell_health(self):
        '''
        If the cell is healthy, returns 'Healthy
        If the cell is unhealthy, returns 'Unhealthy'
        '''

        return self.health

    def request_handler(self, request: dict) -> str:
        '''
        This is the ingress of a cell, it could be an ALB in the real world.

        If the order is for 5 bags of chips, it is a black swan request and will kill the cell

        Returns a string indicating that the request was either handled or not
        '''

        if request['data'].startswith('5'):
            print(f"Health - Cell {self.cell_id} - Unhealthy")
            self.health = "Unhealthy"
            return (
                f"CELL FAILURE - "
                f"Unhandled Request ID: {request['request_id']}, - "
                f"Tenant: {request['tenant_id']}, - "
                f"Cell: {self.cell_id} Data: {request['data']}"
            )

        return(
            f"Handled Request ID: {request['request_id']} "
            f"Tenant: {request['tenant_id']} "
            f"Cell: {self.cell_id} Data: {request['data']}"
        )