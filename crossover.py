from candidate import Candidate
import numpy
import random
class Crossover(object):
    # Lai tao con tu hai cha me

    def __init__(self):
        return
    
    def crossover(self, parent1, parent2, crossoverRate):
        """ Tao hai con moi tu hai cha me """
        child1 = Candidate()
        child2 = Candidate()
        
        # Tao copy tu gen cha me gan vao hai con
        child1.values = numpy.copy(parent1.values)
        child2.values = numpy.copy(parent2.values)

        r = random.uniform(0, 1)

        if (r < crossoverRate):
            # Chon diem cat
            #Diem cat dau tu 0-9
            #Diem cat cuoi tu 1-9
            crossoverPoint1 = random.randint(0, 8)
            crossoverPoint2 = random.randint(1, 9)
            while(crossoverPoint1 == crossoverPoint2):
                crossoverPoint1 = random.randint(0, 8)
                crossoverPoint2 = random.randint(1, 9)
            #Neu diem cat dau lon hon diem cat cuoi thi swap lai
            if(crossoverPoint1 > crossoverPoint2):
                temp = crossoverPoint1
                crossoverPoint1 = crossoverPoint2
                crossoverPoint2 = temp
            # Giao cheo cac dong cua hai con voi nhau
            for i in range(crossoverPoint1, crossoverPoint2):
                child1.values[i], child2.values[i] = self.crossoverRows(child1.values[i], child2.values[i])
        return child1, child2

    def crossoverRows(self, row1, row2): 
        # Khoi tao dong con gom 9 phan tu trong mang
        # Day gia tri cua hai con sau khi giao cheo
        childRow1 = numpy.zeros(9)
        childRow2 = numpy.zeros(9)
        #Cac gia tri chua su dung de giao cheo trong hang gia tri ban dau tu 1-9
        remaining = list(range(1, 10))
        cycle = 0
        
        while((0 in childRow1) and (0 in childRow2)):  # Neu cac dong chua hoan thanh giao cheo
            if(cycle % 2 == 0):  # Chu ki chan
                # Gan gia tri khong su dung tiep theo
                index = self.findUnused(row1, remaining)
                start = row1[index]
                # Remove gia tri trong remaining sau khi su dung xong
                remaining.remove(row1[index])
                childRow1[index] = row1[index]
                childRow2[index] = row2[index]
                next = row2[index]
                
                while(next != start):  # Neu chu trinh chua xong
                    index = self.findValue(row1, next)
                    childRow1[index] = row1[index]
                    remaining.remove(row1[index])
                    childRow2[index] = row2[index]
                    next = row2[index]
                cycle += 1

            else:  # Chu ki le thi giao cheo nguoc lai
                index = self.findUnused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                childRow1[index] = row2[index]
                childRow2[index] = row1[index]
                next = row2[index]
                
                while(next != start):  # Neu chu trinh chua xong
                    index = self.findValue(row1, next)
                    childRow1[index] = row2[index]
                    remaining.remove(row1[index])
                    childRow2[index] = row1[index]
                    next = row2[index]
                cycle += 1
            
        return childRow1, childRow2  
    #Tim kiem dong chua su dung
    def findUnused(self, parentRow, remaining):
        for i in range(0, len(parentRow)):
            if(parentRow[i] in remaining):
                return i
    # Tim kiem gia tri trong mot hang
    def findValue(self, parentRow, value):
        for i in range(0, len(parentRow)):
            if(parentRow[i] == value):
                return i