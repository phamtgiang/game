from sudoku import Sudoku
import sys

if __name__ == '__main__':
    s = Sudoku()
    
    if(len(sys.argv) == 2):
        s.load(sys.argv[1])
    else:
        s.generateSudoku()
    
    s.solve()