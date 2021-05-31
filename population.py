import numpy
import random
from candidate import Candidate
class Population(object):
    """ Tap hop cac candidate tham gia trong quan the"""

    def __init__(self):
        self.candidates = []
        return
    """Sinh candidate voi bang co de cho"""
    def seed(self, numberOfCandidates, board):
        self.candidates = []
        
        # Xac dinh cac gia tri hop le ma moi o tren ban co co the lay
        helper = Candidate()
        helper.values = [[[] for j in range(0, 9)] for i in range(0, 9)]
        
        for row in range(0, 9):
            for column in range(0, 9):
                for value in range(1, 10): 
                    if((board.values[row][column] == 0) and not (board.isColumnDuplicate(column, value) or board.isBlockDuplicate(row, column, value) or board.isRowDuplicate(row, value))):
                        # gia tri da co tren hang tren cot hoac tren box
                        helper.values[row][column].append(value)
                    elif(board.values[row][column] != 0):
                        # gia tri o tren board de cho
                        helper.values[row][column].append(board.values[row][column])
                        break
        # Sinh population      
        for p in range(0, numberOfCandidates):
            g = Candidate()
            for i in range(0, 9): # row
                row = numpy.zeros(9)
                # Dien vao ban
                for j in range(0, 9): # column
                    # Neu gia tri de cho thi khong thay doi
                    if(board.values[i][j] != 0):
                        row[j] = board.values[i][j]
                    # Neu gia tri chua co thi insert vao bang
                    elif(board.values[i][j] == 0):
                        row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j])-1)]

                # Neu khong hop le thi insert lai
                while(len(list(set(row))) != 9):
                    for j in range(0, 9):
                        if(board.values[i][j] == 0):
                            row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j])-1)]

                g.values[i] = row

            self.candidates.append(g)
        
        # Tinh fitness cho toan quan the
        self.updateFitness()
        
        print("Seeding complete.")
        
        return
        
    def updateFitness(self):
        """ Cap nhat finess cho toan quan the """
        for candidate in self.candidates:
            candidate.updateFitness()
        return
        
    def sort(self):
        """ Sort the population dua tren fitness. """
        self.candidates.sort(key=self.sortFitness)
        return

    def sortFitness(self, x):
        return x.fitness

