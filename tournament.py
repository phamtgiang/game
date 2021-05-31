import candidate
import random
class Tournament(object):
    """Sinh Xac suat lua chon giong tot hay giong xau, giong tot co co hoi cao hon de re-produce 
           nhung giong xau van co co hoi de re-produce"""

    def __init__(self):
        return
        
    def compete(self, candidates):
        """ Chon ngau nhien 2 candidate tu population va so sanh voi nhau"""
        c1 = candidates[random.randint(0, len(candidates)-1)]
        c2 = candidates[random.randint(0, len(candidates)-1)]
        f1 = c1.fitness
        f2 = c2.fitness

        # Xac dinh candidate co fitness lon hon
        if(f1 > f2):
            fittest = c1
            weakest = c2
        else:
            fittest = c2
            weakest = c1
        
        selectionRate = 0.85
        #Sinh ngau nhien mot so thuc trong khoang tu 0 den 1 neu lon hon selectionRate thi chon fittest
        #va nguoc lai. Ti le candidate co fitness cao hon se co ti le duoc chon cao hon
        r = random.uniform(0, 1)
        if(r < selectionRate):
            return fittest
        else:
            return weakest