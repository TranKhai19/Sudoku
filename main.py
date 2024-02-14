import tkinter as tk
import random

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.geometry("400x450")
        
        self.board_frame = tk.Frame(root, bg="black", width=400, height=400)
        self.board_frame.pack_propagate(False)
        self.board_frame.pack()
        
        self.generate_button = tk.Button(root, text="Generate Puzzle", command=self.generate_puzzle)
        self.generate_button.pack()
        
        self.play_button = tk.Button(root, text="Play", command=self.play)
        self.play_button.pack()
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()
        
        self.board = [[tk.StringVar() for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        
        self.puzzle = None
        self.generated = False
        
    def generate_puzzle(self):
        self.puzzle = generate_sudoku()
        self.generated = True
        self.update_board()
    
    def update_board(self):
        for i in range(9):
            for j in range(9):
                if self.generated and self.puzzle[i][j] != 0:
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(self.puzzle[i][j]))
                    self.entries[i][j].config(state="disabled")
                else:
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].config(state="normal")
    
    def play(self):
        if not self.generated:
            return
        
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value:
                    self.puzzle[i][j] = int(value)
        
        if solve_sudoku(self.puzzle):
            self.update_board()
            if all(0 not in row for row in self.puzzle):
                self.game_over()
        else:
            tk.messagebox.showinfo("Invalid Move", "This puzzle cannot be solved with current inputs.")
    
    def reset(self):
        self.generated = False
        self.puzzle = None
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(state="normal")
    
    def game_over(self):
        tk.messagebox.showinfo("Congratulations", "You solved the puzzle!")

def generate_sudoku():
    # Create an empty 9x9 grid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill the grid with a valid Sudoku solution
    solve_sudoku(grid)
    
    # Remove some numbers to create the puzzle
    remove_numbers(grid)
    
    return grid

def solve_sudoku(grid):
    # Find an empty cell (0) in the grid
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return True  # All cells filled, puzzle solved
    
    row, col = empty_cell
    
    # Try different numbers in the cell
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            
            # Recursively try to solve the puzzle
            if solve_sudoku(grid):
                return True
            
            # Backtrack if the current move leads to a dead end
            grid[row][col] = 0
            
    return False

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def is_valid_move(grid, row, col, num):
    # Check if the number is not in the same row or column
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    
    # Check if the number is not in the same 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    
    return True

def remove_numbers(grid, difficulty=0.5):
    # Remove some numbers based on difficulty level
    for i in range(9):
        for j in range(9):
            if random.random() < difficulty:
                grid[i][j] = 0

def main():
    root = tk.Tk()
    game = SudokuGame(root)
    
    for i in range(9):
        for j in range(9):
            game.entries[i][j] = tk.StringVar()
            game.entries[i][j] = tk.Entry(game.board_frame, textvariable=game.entries[i][j], width=3)
            game.entries[i][j].grid(row=i, column=j)
    
    root.mainloop()

if __name__ == "__main__":
    main()
