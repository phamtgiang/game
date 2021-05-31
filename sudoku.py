import numpy
import random
from board import Board
from population import Population
from candidate import Candidate
from tournament import Tournament
from crossover import Crossover
random.seed()

class Sudoku(object):
    # Xu li bai toan sudoku

    def __init__(self):
        self.board = None
        return
    
    def load(self, path):
        # Doc file lay output
        with open(path, "r") as f:
            values = numpy.loadtxt(f).reshape((9, 9)).astype(int)
            print(values)
            self.board = Board(values)
        return

    def generateSudoku(self):
        while True:
            m = numpy.zeros((9, 9), int)
            rg = numpy.arange(1, 10)
            m[0, :] = numpy.random.choice(rg, 9, replace=False)
            # Tao ngau nhien mot ket qua
            try:
                for r in range(1, 9):
                    for c in range(9):
                        columnRest = numpy.setdiff1d(rg, m[:r, c])
                        rowRest = numpy.setdiff1d(rg, m[r, :c])
                        avb1 = numpy.intersect1d(columnRest, rowRest)
                        subRow, subColumn = r//3, c//3
                        avb2 = numpy.setdiff1d(numpy.arange(0, 9+1), m[subRow*3:(subRow+1)*3, subColumn*3:(subColumn+1)*3].ravel())
                        avb = numpy.intersect1d(avb1, avb2)
                        m[r, c] = numpy.random.choice(avb, size=1)
                break
            except ValueError:
                pass
        mm = m.copy()
        difficulty = random.uniform(0.5, 0.8)
        #Loai bo ngau nhien mot so o
        mm[numpy.random.choice([True, False], size=m.shape, p=[difficulty, 1- difficulty])] = 0
        print("Initial state: \n", mm)
        self.board = Board(mm)



    def save(self, path, solution):
        # Luu ket qua
        with open(path, "w") as f:
            numpy.savetxt(f, solution.values.reshape(9*9), fmt='%d')
        return

    def solve(self):
            numberOfCandidate = 1000 #So luong candidate trong quan the
            numberOfElite = int(0.05*numberOfCandidate)   #Lay 5% gen uu tu moi lan generate
            maxGeneration = 1000  #So generate toi da
            numberOfMutation = 0  
            
            # Mutation parameters.
            phi = 0
            sigma = 1
            mutationRate = 0.3
        
            # Tao population ban dau
            self.population = Population()
            self.population.seed(numberOfCandidate, self.board)
        
            stale = 0
            for generation in range(0, maxGeneration):
            
                print("Generation %d" % generation)
                
                # Kiem tra ket qua
                bestFitness = 0.0
                for c in range(0, numberOfCandidate):
                    fitness = self.population.candidates[c].fitness
                    if(fitness == 162):
                        print("Solution found at generation %d:" % generation)
                        print(self.population.candidates[c].values)
                        return self.population.candidates[c]

                    # Tim finess tot nhat
                    if(fitness > bestFitness):
                        bestFitness = fitness

                print("Best fitness = %f" % bestFitness)

                # Tao population moi
                nextPopulation = []

                # Lua chon nhung giong tot de bao ton cho lan nhan giong sau
                self.population.sort()
                elites = []
                for e in range(0, numberOfElite):
                    elite = Candidate()
                    elite.values = numpy.copy(self.population.candidates[e].values)
                    elites.append(elite)

                # tao cac candidate con lai
                for count in range(numberOfElite, numberOfCandidate, 2):
                    # chon parent tu tournament
                    t = Tournament()
                    parent1 = t.compete(self.population.candidates)
                    parent2 = t.compete(self.population.candidates)
                    
                    ## Cross-over.
                    cc = Crossover()
                    child1, child2 = cc.crossover(parent1, parent2, 1.0)
                    child1.updateFitness()
                    child2.updateFitness()
                    # Mutate child1.
                    oldFitness = child1.fitness
                    success = child1.mutate(mutationRate, self.board)
                    child1.updateFitness()
                    if(success):
                        numberOfMutation += 1
                    
                    # Mutate child2.
                    oldFitness = child2.fitness
                    
                    success = child2.mutate(mutationRate, self.board)
                    child2.updateFitness()
                    if(success):
                        numberOfMutation += 1
                        
                        if(child2.fitness > oldFitness):  # Tinh ti le dot bien tao ra con moi thanh cong
                            phi = phi + 1
                    
                    # Nap nhung ca the tot vao quan the
                    nextPopulation.append(child1)
                    nextPopulation.append(child2)

                # Nap nhung ca the tot vao quan the
                for e in range(0, numberOfElite):
                    nextPopulation.append(elites[e])
                    
                # Cap nhat lai quan the
                self.population.candidates = nextPopulation
                self.population.updateFitness()
                
                # Calculate new adaptive mutation rate (based on Rechenberg's 1/5 success rule). This is to stop too much mutation as the fitness progresses towards unity.
                # Thay doi mutationRate de phu hop hon
                if(numberOfMutation == 0):
                    phi = 0  # Tranh chia cho khong
                else:
                    phi = phi / numberOfMutation
                
                if(phi > 0.2):
                    sigma = sigma/0.998
                elif(phi < 0.2):
                    sigma = sigma*0.998

                mutationRate = abs(numpy.random.normal(loc=0.0, scale=sigma, size=None))
                numberOfMutation = 0
                phi = 0

                # Kiem tra stale
                self.population.sort()
                if(self.population.candidates[0].fitness != self.population.candidates[1].fitness):
                    stale = 0
                else:
                    stale += 1

                # Re-seed the population neu hai candidate duoc chon lun co cung chi so fitness 
                if(stale >= 100):
                    print("The population has gone stale. Re-seeding...")
                    self.population.seed(numberOfCandidate, self.board)
                    stale = 0
                    sigma = 1
                    phi = 0
                    numberOfMutation = 0
                    mutationRate = 0.06
            
            print("No solution found.")
            return None