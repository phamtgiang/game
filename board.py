import numpy
class Board():
    # Ban co va mot so tac vu kiem tra tren ban co
    def __init__(self, values):
        self.values = values
        return

        
    def isRowDuplicate(self, row, value):
        """ Kiem tra trong hang, value co trung voi cac gia tri da cho hay khong""" 
        for column in range(0, 9):
            if(self.values[row][column] == value):
               return True
        return False

    def isColumnDuplicate(self, column, value):
        """ Kiem tra trong cot, value co trung voi cac gia tri da cho hay khong"""
        for row in range(0, 9):
            if(self.values[row][column] == value):
               return True
        return False

    def isBlockDuplicate(self, row, column, value):
        """ Kiem tra trong block, value co trung voi cac gia tri da cho hay khong"""
        i = 3*(int(row/3))
        j = 3*(int(column/3))

        if((self.values[i][j] == value)
           or (self.values[i][j+1] == value)
           or (self.values[i][j+2] == value)
           or (self.values[i+1][j] == value)
           or (self.values[i+1][j+1] == value)
           or (self.values[i+1][j+2] == value)
           or (self.values[i+2][j] == value)
           or (self.values[i+2][j+1] == value)
           or (self.values[i+2][j+2] == value)):
            return True
        else:
            return False