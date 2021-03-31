from mazelib import Maze
from mazelib.generate.Prims import Prims
import matplotlib.pyplot as plt

"""
Kullanilmiyor eger daha zor labirentler gerekirse diye
"""

def generate_maze(arg):
    pass

# grid ile maze ayni sey olmaya bilir
def showPNG(grid):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == "__main__":
    maze = Maze()
    maze.generator = Prims(5, 5)
    maze.generate()
    print(maze)
