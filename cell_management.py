'''
Contains a class that represents a cell as well as a manager that would otherwise
be part of the control plane, it manages adding cells and determining cell health.
'''

from random import sample

from cell import Cell

class CellManager():
    '''
    Manages the current cells, part of the control plane.
    '''

    def __init__(self, cell_router):
        self.list_of_cells: list[Cell] = []
        self.cell_router = cell_router

    def add_cell(self):
        '''
        Adds a new cell to the list of cells, also assigns the cell and id number
        '''

        cell: Cell = Cell(cell_router=self.cell_router, cell_id=len(self.list_of_cells))
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

    def assign_cells_to_new_tenant(self):
        '''
        This will assign some cells from the pool to new a new tenant
        '''

        return sample(self.get_list_of_healthy_cell_ids(), 2)
