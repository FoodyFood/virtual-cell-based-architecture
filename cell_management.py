'''
Contains a class that represents a cell as well as a manager that would otherwise
be part of the control plane, it manages adding cells and determining cell health.
'''

class Cell():
    '''
    This represents a single cell
    '''

    def __init__(self, cell_id: int):
        self.cell_id: int = cell_id
        self.health: str = "Healthy"

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
                f"Unhandled Request ID: {request['request_id']}, - "
                f"Tenant: {request['tenant_id']}, - "
                f"Cell: {self.cell_id} Data: {request['data']}"
            )

        return(
            f"Handled Request ID: {request['request_id']} "
            f"Tenant: {request['tenant_id']} "
            f"Cell: {self.cell_id} Data: {request['data']}"
        )


class CellManager():
    '''
    Manages the current cells, part of the control plane.
    '''
    list_of_cells: list[Cell] = []

    def add_cell(self):
        '''
        Adds a new cell to the list of cells, also assigns the cell and id number
        '''

        cell: Cell = Cell(cell_id=len(self.list_of_cells))
        self.list_of_cells.append(cell)

    def get_list_of_cells(self):
        '''
        This returns the complete list of cells, regardless of health status
        '''

        return self.list_of_cells

    def get_list_of_healthy_cell_ids(self):
        '''
        This will return a list of only the healthy cell ids
        '''

        list_of_healthy_cell_ids: list = []
        for cell in self.list_of_cells:
            if cell.get_cell_health() == "Healthy":
                list_of_healthy_cell_ids.append(cell.get_cell_id())
        return list_of_healthy_cell_ids

    def get_list_of_unhealthy_cell_ids(self):
        '''
        This will return a list of only the unhealthy cell ids
        '''

        list_of_unhealthy_cell_ids: list = []
        for cell in self.list_of_cells:
            if cell.get_cell_health() == "Unhealthy":
                list_of_unhealthy_cell_ids.append(cell.get_cell_id())
        return list_of_unhealthy_cell_ids

    def get_cell_handler(self, cell_id: int):
        '''
        Returns the request handler of the cell, likely a load balancer in the real world
        '''

        for cell in self.list_of_cells:
            if cell.get_cell_id() == cell_id:
                return cell.request_handler

        return None

cell_manager: CellManager = CellManager()
