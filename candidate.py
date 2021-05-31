import numpy
import random
from board import Board
class Candidate(object):
    """ Cac candidate tham gia trong population"""
    def __init__(self):
        self.values = numpy.zeros((9, 9), dtype=int)
        self.fitness = None
        return

    def updateFitness(self):
        """ Ham danh gia dua theo tieu chi so o khac nhau tren mot hang hoac 
            tren mot cot hoac tren mot block"""
        # max la 162 diem
        columnCount = numpy.zeros(9)
        blockCount = numpy.zeros(9)
        columnSum = 0
        blockSum = 0
        #Duyet tren moi cot
        for i in range(0, 9):  
            for j in range(0, 9):  
                columnCount[self.values[j][i]-1] = 1  

            columnSum += sum(columnCount)
            columnCount = numpy.zeros(9)


        # Duyet tren moi block
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                blockCount[self.values[i][j]-1] = 1
                blockCount[self.values[i][j+1]-1] = 1
                blockCount[self.values[i][j+2]-1] = 1
                
                blockCount[self.values[i+1][j]-1] = 1
                blockCount[self.values[i+1][j+1]-1] = 1
                blockCount[self.values[i+1][j+2]-1] = 1
                
                blockCount[self.values[i+2][j]-1] = 1
                blockCount[self.values[i+2][j+1]-1] = 1
                blockCount[self.values[i+2][j+2]-1] = 1

                blockSum += sum(blockCount)
                blockCount = numpy.zeros(9)

        # Tinh finess
        
        self.fitness = blockSum + columnSum
        return
        
    def mutate(self, mutationRate, board):
        """ Dot bien ca the bang cach chon mot dong bat ki va chon hai gia tri bat ki va swap hai gia tri voi nhau"""
        # Sinh
        r = random.uniform(0, 1.1)
        while(r > 1): 
            r = random.uniform(0, 1.1)
    
        success = False
        if (r < mutationRate):  # Mutate.
            while(not success):
                row1 = random.randint(0, 8)
                row2 = random.randint(0, 8)
                row2 = row1
                
                from_column = random.randint(0, 8)
                to_column = random.randint(0, 8)
                while(from_column == to_column):
                    from_column = random.randint(0, 8)
                    to_column = random.randint(0, 8)   

                # Kiem tra gia tri co la diem co dinh tren ban co khong
                if(board.values[row1][from_column] == 0 and board.values[row1][to_column] == 0):
                    # kiem tra co sai luat khong
                    if(not board.isColumnDuplicate(to_column, self.values[row1][from_column])
                       and not board.isColumnDuplicate(from_column, self.values[row2][to_column])
                       and not board.isBlockDuplicate(row2, to_column, self.values[row1][from_column])
                       and not board.isBlockDuplicate(row1, from_column, self.values[row2][to_column])):
                    
                        # Swap values.
                        temp = self.values[row2][to_column]
                        self.values[row2][to_column] = self.values[row1][from_column]
                        self.values[row1][from_column] = temp
                        success = True
        return success