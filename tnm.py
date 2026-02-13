import tkinter as tk
from tkinter import ttk


class TimeBasedMaze:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабиринт времени")

        self.rows = 20
        self.cols = 20
        self.cell_size = 28

        self.player_pos = [1, 1]
        self.exit_pos = [18, 18]

        self.current_time = 12

        self.base_maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.time_gates = {
            (2, 3): {"day": 0, "night": 1},
            (3, 6): {"day": 0, "night": 1},
            (5, 10): {"day": 0, "night": 1},
            (7, 15): {"day": 0, "night": 1},
            (9, 5): {"day": 0, "night": 1},
            (11, 12): {"day": 0, "night": 1},
            (13, 8): {"day": 0, "night": 1},
            (15, 17): {"day": 0, "night": 1},
            (17, 10): {"day": 0, "night": 1},
            (1, 7): {"day": 1, "night": 0},
            (4, 13): {"day": 1, "night": 0},
            (6, 16): {"day": 1, "night": 0},
            (8, 2): {"day": 1, "night": 0},
            (10, 9): {"day": 1, "night": 0},
            (12, 5): {"day": 1, "night": 0},
            (14, 14): {"day": 1, "night": 0},
            (16, 11): {"day": 1, "night": 0},
            (18, 16): {"day": 1, "night": 0},
        }

        self.maze = self.update_maze_by_time()
        self.setup_ui()
        self.draw_maze()
        self.root.bind("<KeyPress>", self.key_pressed)

    def update_maze_by_time(self):
        maze = [row[:] for row in self.base_maze]
        is_day = 6 <= self.current_time < 18
        for (r, c), states in self.time_gates.items():
            if is_day:
                maze[r][c] = states["day"]
            else:
                maze[r][c] = states["night"]
        return maze

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.time_label = ttk.Label(
            top_frame,
            text=self.get_time_text(),
            font=("Arial", 14, "bold")
        )
        self.time_label.grid(row=0, column=0, padx=(0, 20))
        ttk.Button(
            top_frame,
            text="День",
            command=lambda: self.set_time(12),
            width=10
        ).grid(row=0, column=1, padx=5)
        ttk.Button(
            top_frame,
            text="Ночь",
            command=lambda: self.set_time(0),
            width=10
        ).grid(row=0, column=2, padx=5)
        maze_frame = ttk.Frame(main_frame)
        maze_frame.grid(row=1, column=0, pady=(10, 0))
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        self.canvas = tk.Canvas(
            maze_frame,
            width=canvas_width,
            height=canvas_height,
            bg="white",
            highlightthickness=1,
            highlightbackground="black"
        )
        self.canvas.grid(row=0, column=0)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def get_time_text(self):
        if 6 <= self.current_time < 18:
            return f"Время: {self.current_time}:00 (День)"
        else:
            return f"Время: {self.current_time}:00 (Ночь)"

    def draw_maze(self):
        self.canvas.delete("all")
        is_day = 6 <= self.current_time < 18
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                if self.maze[r][c] == 1:
                    color = "#2c3e50"
                elif (r, c) in self.time_gates:
                    if is_day:
                        color = "#f39c12" if self.maze[r][c] == 0 else "#2c3e50"
                    else:
                        color = "#8e44ad" if self.maze[r][c] == 0 else "#2c3e50"
                else:
                    color = "#ecf0f1"
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#7f8c8d",
                    width=1
                )
                if (r, c) in self.time_gates:
                    if is_day and self.maze[r][c] == 0:
                        self.canvas.create_text(
                            x1 + self.cell_size / 2,
                            y1 + self.cell_size / 2,
                            text="☀",
                            font=("Arial", 12)
                        )
                    elif not is_day and self.maze[r][c] == 0:
                        self.canvas.create_text(
                            x1 + self.cell_size / 2,
                            y1 + self.cell_size / 2,
                            text="☾",
                            font=("Arial", 12)
                        )
        exit_x1 = self.exit_pos[1] * self.cell_size
        exit_y1 = self.exit_pos[0] * self.cell_size
        exit_x2 = exit_x1 + self.cell_size
        exit_y2 = exit_y1 + self.cell_size
        self.canvas.create_rectangle(
            exit_x1, exit_y1, exit_x2, exit_y2,
            fill="#27ae60",
            outline="#2ecc71",
            width=2
        )
        self.canvas.create_text(
            exit_x1 + self.cell_size / 2,
            exit_y1 + self.cell_size / 2,
            text="Выход",
            fill="white",
            font=("Arial", 9, "bold")
        )
        player_x1 = self.player_pos[1] * self.cell_size + self.cell_size / 4
        player_y1 = self.player_pos[0] * self.cell_size + self.cell_size / 4
        player_x2 = player_x1 + self.cell_size / 2
        player_y2 = player_y1 + self.cell_size / 2
        self.canvas.create_oval(
            player_x1, player_y1, player_x2, player_y2,
            fill="#e74c3c",
            outline="#c0392b",
            width=2
        )
        if self.player_pos == self.exit_pos:
            self.show_victory()

    def show_victory(self):
        self.canvas.create_rectangle(
            0, 0,
            self.cols * self.cell_size,
            self.rows * self.cell_size,
            fill="black",
            stipple="gray50"
        )
        self.canvas.create_text(
            self.cols * self.cell_size / 2,
            self.rows * self.cell_size / 2,
            text="ПОБЕДА!",
            fill="#e74c3c",
            font=("Arial", 32, "bold")
        )

    def set_time(self, hour):
        self.current_time = hour
        self.time_label.config(text=self.get_time_text())
        self.update_maze_and_redraw()

    def update_maze_and_redraw(self):
        self.maze = self.update_maze_by_time()
        self.draw_maze()

    def key_pressed(self, event):
        if self.player_pos == self.exit_pos:
            return
        new_pos = self.player_pos[:]
        key = event.keysym.lower()
        if key in ['up', 'w']:
            new_pos[0] -= 1
        elif key in ['down', 's']:
            new_pos[0] += 1
        elif key in ['left', 'a']:
            new_pos[1] -= 1
        elif key in ['right', 'd']:
            new_pos[1] += 1
        else:
            return
        if (0 <= new_pos[0] < self.rows and
                0 <= new_pos[1] < self.cols and
                self.maze[new_pos[0]][new_pos[1]] == 0):
            self.player_pos = new_pos
            self.draw_maze()


def main():
    root = tk.Tk()
    root.title("Лабиринт времени")
    root.geometry("600x650")
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    game = TimeBasedMaze(root)
    root.mainloop()


if __name__ == "__main__":
    main()