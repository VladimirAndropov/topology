import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import math

class FourDTicTacToeSpaced:
    def __init__(self, root):
        self.root = root
        self.root.title("4D Крестики-Нолики")
        self.board = np.zeros((3, 3, 3, 3), dtype=int)
        self.current_player = 1
        self.move_history = []
        self.current_w = 0
        self.cube_size = 450
        self.node_radius = 7
        self.vertical_spacing_factor = 1.8
        self.player_colors = {
            1: "#2196F3",
            2: "#FF5252"
        }
        self.y_layer_colors = {
            0: "#BBDEFB",
            1: "#C8E6C9",
            2: "#FFECB3"
        }
        self.w_button_colors = {
            0: "#4CAF50",
            1: "#2196F3",
            2: "#FF9800"
        }
        self.symbols = {0: "", 1: "X", 2: "O"}
        self.create_minimal_interface()
        self.calculate_3d_coordinates()
        self.draw_cube()

    def calculate_3d_coordinates(self):
        self.nodes_3d = []
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    nx = (x - 1) / 1.0
                    ny = (1 - y) * self.vertical_spacing_factor / 1.0
                    nz = (z - 1) / 1.0
                    self.nodes_3d.append({
                        'x': nx,
                        'y': ny,
                        'z': nz,
                        'grid': (x, y, z)
                    })
        self.edges = []
        for z in range(3):
            for y in range(3):
                for x in range(2):
                    idx1 = z * 9 + y * 3 + x
                    idx2 = z * 9 + y * 3 + x + 1
                    self.edges.append((idx1, idx2))
        for z in range(3):
            for x in range(3):
                for y in range(2):
                    idx1 = z * 9 + y * 3 + x
                    idx2 = z * 9 + (y + 1) * 3 + x
                    self.edges.append((idx1, idx2))
        for y in range(3):
            for x in range(3):
                for z in range(2):
                    idx1 = z * 9 + y * 3 + x
                    idx2 = (z + 1) * 9 + y * 3 + x
                    self.edges.append((idx1, idx2))

    def project_3d_to_2d(self, x, y, z):
        angle_x = math.radians(20)
        angle_y = math.radians(45)
        rotated_x = x * math.cos(angle_y) - z * math.sin(angle_y)
        rotated_z = x * math.sin(angle_y) + z * math.cos(angle_y)
        rotated_y = y * math.cos(angle_x) - rotated_z * math.sin(angle_x)
        scale = self.cube_size / (4 * self.vertical_spacing_factor * 0.7)
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 800
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        screen_x = center_x + rotated_x * scale
        screen_y = center_y - rotated_y * scale
        return screen_x, screen_y

    def create_minimal_interface(self):
        main_container = tk.Frame(self.root, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True)
        top_frame = tk.Frame(main_container, bg="#FFFFFF", height=70)
        top_frame.pack(fill=tk.X, pady=(0, 2))
        top_frame.pack_propagate(False)
        left_panel = tk.Frame(top_frame, bg="#FFFFFF")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=15)
        self.player_label = tk.Label(
            left_panel,
            text="Ход: X",
            font=("Arial", 20, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        self.player_label.pack(pady=10)
        self.stats_label = tk.Label(
            left_panel,
            text="Ходов: 0",
            font=("Arial", 11),
            bg="#FFFFFF",
            fg="#666666"
        )
        self.stats_label.pack()
        center_panel = tk.Frame(top_frame, bg="#FFFFFF")
        center_panel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=50)
        self.w_buttons = []
        w_button_frame = tk.Frame(center_panel, bg="#FFFFFF")
        w_button_frame.pack(expand=True)
        for w in range(3):
            btn = tk.Button(
                w_button_frame,
                text=f"Слой W={w}",
                font=("Arial", 14, "bold"),
                width=10,
                height=2,
                bg=self.w_button_colors[w] if w == 0 else "#E0E0E0",
                fg="white" if w == 0 else "#666666",
                activebackground=self.w_button_colors[w],
                activeforeground="white",
                relief="flat",
                command=lambda w_val=w: self.change_w_slice(w_val)
            )
            btn.pack(side=tk.LEFT, padx=10)
            self.w_buttons.append(btn)
        right_panel = tk.Frame(top_frame, bg="#FFFFFF")
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=15)
        control_frame = tk.Frame(right_panel, bg="#FFFFFF")
        control_frame.pack(pady=10)
        tk.Button(
            control_frame,
            text="Новая игра",
            command=self.reset_game,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            width=12,
            height=1,
            relief="flat"
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            control_frame,
            text="Отменить ход",
            command=self.undo_move,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            width=12,
            height=1,
            relief="flat"
        ).pack(side=tk.LEFT, padx=5)
        canvas_container = tk.Frame(main_container, bg="#FAFAFA")
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.canvas = tk.Canvas(
            canvas_container,
            bg="#FAFAFA",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        status_frame = tk.Frame(main_container, bg="#E8EAF6", height=30)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        status_frame.pack_propagate(False)
        self.status_label = tk.Label(
            status_frame,
            text="Выберите слой W и кликните на узел куба",
            font=("Arial", 10),
            bg="#E8EAF6",
            fg="#333333"
        )
        self.status_label.pack(pady=5)

    def on_canvas_resize(self, event):
        if hasattr(self, 'nodes_3d'):
            self.draw_cube()

    def draw_cube(self):
        self.canvas.delete("all")
        self.node_positions = []
        for i, node in enumerate(self.nodes_3d):
            x, y = self.project_3d_to_2d(node['x'], node['y'], node['z'])
            self.node_positions.append((x, y))
            grid_x, grid_y, grid_z = node['grid']
            cell_value = self.board[self.current_w, grid_z, grid_y, grid_x]
            layer_color = self.y_layer_colors[grid_y]
            if cell_value == 0:
                fill_color = layer_color
                outline_color = "#BDBDBD"
                outline_width = 1
            else:
                fill_color = self.player_colors[cell_value]
                outline_color = layer_color
                outline_width = 2
            node_id = self.canvas.create_oval(
                x - self.node_radius, y - self.node_radius,
                x + self.node_radius, y + self.node_radius,
                fill=fill_color,
                outline=outline_color,
                width=outline_width,
                tags=f"node_{i}"
            )
            if cell_value != 0:
                self.canvas.create_text(
                    x, y,
                    text=self.symbols[cell_value],
                    font=("Arial", 16, "bold"),
                    fill="white",
                    tags=f"symbol_{i}"
                )
            self.canvas.tag_bind(f"node_{i}", "<Button-1>",
                                 lambda e, x=grid_x, y=grid_y, z=grid_z: self.make_move(x, y, z))
            self.canvas.tag_bind(f"node_{i}", "<Enter>",
                                 lambda e, node_id=node_id: self.canvas.itemconfig(node_id, width=3))
            self.canvas.tag_bind(f"node_{i}", "<Leave>",
                                 lambda e, node_id=node_id, outline_width=outline_width:
                                 self.canvas.itemconfig(node_id, width=outline_width))
        for edge in self.edges:
            x1, y1 = self.node_positions[edge[0]]
            x2, y2 = self.node_positions[edge[1]]
            node1 = self.nodes_3d[edge[0]]
            node2 = self.nodes_3d[edge[1]]
            grid_y1 = node1['grid'][1]
            grid_y2 = node2['grid'][1]
            if grid_y1 != grid_y2:
                edge_color = self.y_layer_colors[max(grid_y1, grid_y2)]
            else:
                edge_color = self.y_layer_colors[grid_y1]
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=edge_color,
                width=1,
                tags="edge"
            )
        if self.move_history:
            self.highlight_last_move()
        self.update_stats()

    def change_w_slice(self, w):
        self.current_w = w
        for i, btn in enumerate(self.w_buttons):
            if i == w:
                btn.config(
                    bg=self.w_button_colors[i],
                    fg="white",
                    relief="sunken"
                )
            else:
                btn.config(
                    bg="#E0E0E0",
                    fg="#666666",
                    relief="flat"
                )
        self.draw_cube()
        self.status_label.config(
            text=f"Текущий слой: W={w}. Кликните на узел куба для хода."
        )

    def make_move(self, x, y, z):
        if self.board[self.current_w, z, y, x] == 0:
            self.board[self.current_w, z, y, x] = self.current_player
            self.move_history.append((self.current_w, z, y, x, self.current_player))
            self.draw_cube()
            if self.check_win(self.current_w, z, y, x):
                winner = "X" if self.current_player == 1 else "O"
                self.show_win_message(winner)
                return
            if np.all(self.board != 0):
                messagebox.showinfo("Ничья!", "Все ячейки заполнены!")
                return
            self.current_player = 3 - self.current_player
            self.player_label.config(
                text=f"Ход: {'X' if self.current_player == 1 else 'O'}",
                fg="#2196F3" if self.current_player == 1 else "#FF5252"
            )
            self.status_label.config(
                text=f"Ход сделан в W={self.current_w}, Z={z}, Y={y}, X={x}. Ход игрока {'X' if self.current_player == 1 else 'O'}."
            )

    def highlight_last_move(self):
        if self.move_history:
            last_w, last_z, last_y, last_x, _ = self.move_history[-1]
            for i, node in enumerate(self.nodes_3d):
                grid_x, grid_y, grid_z = node['grid']
                if (grid_x == last_x and grid_y == last_y and grid_z == last_z and
                        self.current_w == last_w):
                    x, y = self.node_positions[i]
                    self.canvas.create_oval(
                        x - self.node_radius - 4, y - self.node_radius - 4,
                        x + self.node_radius + 4, y + self.node_radius + 4,
                        outline="#FFC107",
                        width=3,
                        tags="last_move"
                    )
                    break

    def update_stats(self):
        total_moves = len(self.move_history)
        x_count = np.sum(self.board == 1)
        o_count = np.sum(self.board == 2)
        self.stats_label.config(
            text=f"Ходов: {total_moves} | X: {x_count} | O: {o_count}"
        )

    def check_win(self, w, z, y, x):
        player = self.board[w, z, y, x]
        directions_3d = [
            [(0, 0, 1), (0, 0, -1)],
            [(0, 1, 0), (0, -1, 0)],
            [(1, 0, 0), (-1, 0, 0)],
            [(0, 1, 1), (0, -1, -1)],
            [(0, 1, -1), (0, -1, 1)],
            [(1, 0, 1), (-1, 0, -1)],
            [(1, 0, -1), (-1, 0, 1)],
            [(1, 1, 0), (-1, -1, 0)],
            [(1, -1, 0), (-1, 1, 0)],
            [(1, 1, 1), (-1, -1, -1)],
            [(1, 1, -1), (-1, -1, 1)],
            [(1, -1, 1), (-1, 1, -1)],
            [(-1, 1, 1), (1, -1, -1)],
        ]
        for dir1, dir2 in directions_3d:
            count = 1
            dz1, dy1, dx1 = dir1
            for i in range(1, 3):
                nz, ny, nx = z + i * dz1, y + i * dy1, x + i * dx1
                if 0 <= nz < 3 and 0 <= ny < 3 and 0 <= nx < 3:
                    if self.board[w, nz, ny, nx] == player:
                        count += 1
                    else:
                        break
                else:
                    break
            dz2, dy2, dx2 = dir2
            for i in range(1, 3):
                nz, ny, nx = z + i * dz2, y + i * dy2, x + i * dx2
                if 0 <= nz < 3 and 0 <= ny < 3 and 0 <= nx < 3:
                    if self.board[w, nz, ny, nx] == player:
                        count += 1
                    else:
                        break
                else:
                    break
            if count >= 3:
                return True
        count_w = 1
        for i in range(1, 3):
            nw = w + i
            if 0 <= nw < 3:
                if self.board[nw, z, y, x] == player:
                    count_w += 1
                else:
                    break
            else:
                break
        for i in range(1, 3):
            nw = w - i
            if 0 <= nw < 3:
                if self.board[nw, z, y, x] == player:
                    count_w += 1
                else:
                    break
            else:
                break
        if count_w >= 3:
            return True
        diag_directions = [
            [(1, 1, 0, 0), (-1, -1, 0, 0)],
            [(1, 0, 1, 0), (-1, 0, -1, 0)],
            [(1, 0, 0, 1), (-1, 0, 0, -1)],
            [(1, 1, 1, 0), (-1, -1, -1, 0)],
            [(1, 1, 0, 1), (-1, -1, 0, -1)],
            [(1, 0, 1, 1), (-1, 0, -1, -1)],
            [(1, 1, 1, 1), (-1, -1, -1, -1)],
        ]
        for dir1, dir2 in diag_directions:
            count = 1
            dw1, dz1, dy1, dx1 = dir1
            for i in range(1, 3):
                nw, nz, ny, nx = w + i * dw1, z + i * dz1, y + i * dy1, x + i * dx1
                if all(0 <= coord < 3 for coord in [nw, nz, ny, nx]):
                    if self.board[nw, nz, ny, nx] == player:
                        count += 1
                    else:
                        break
                else:
                    break
            dw2, dz2, dy2, dx2 = dir2
            for i in range(1, 3):
                nw, nz, ny, nx = w + i * dw2, z + i * dz2, y + i * dy2, x + i * dx2
                if all(0 <= coord < 3 for coord in [nw, nz, ny, nx]):
                    if self.board[nw, nz, ny, nx] == player:
                        count += 1
                    else:
                        break
                else:
                    break
            if count >= 3:
                return True
        return False

    def show_win_message(self, winner):
        player_num = 1 if winner == "X" else 2
        win_color = "#4CAF50" if winner == "X" else "#FF5722"
        for i, node in enumerate(self.nodes_3d):
            grid_x, grid_y, grid_z = node['grid']
            if self.board[self.current_w, grid_z, grid_y, grid_x] == player_num:
                x, y = self.node_positions[i]
                self.canvas.create_oval(
                    x - self.node_radius - 6, y - self.node_radius - 6,
                    x + self.node_radius + 6, y + self.node_radius + 6,
                    outline=win_color,
                    width=4,
                    tags="winner"
                )
        messagebox.showinfo(
            "Победа!",
            f"Игрок {winner} победил в 4D пространстве!"
        )
        self.status_label.config(
            text=f"Игрок {winner} победил! Начните новую игру.",
            fg=win_color
        )

    def reset_game(self):
        self.board = np.zeros((3, 3, 3, 3), dtype=int)
        self.current_player = 1
        self.move_history = []
        self.current_w = 0
        self.player_label.config(
            text="Ход: X",
            fg="#333333"
        )
        for i, btn in enumerate(self.w_buttons):
            if i == 0:
                btn.config(
                    bg=self.w_button_colors[i],
                    fg="white",
                    relief="sunken"
                )
            else:
                btn.config(
                    bg="#E0E0E0",
                    fg="#666666",
                    relief="flat"
                )
        self.draw_cube()
        self.status_label.config(
            text="Новая игра начата. Выберите слой W и сделайте ход.",
            fg="#333333"
        )

    def undo_move(self):
        if self.move_history:
            w, z, y, x, player = self.move_history.pop()
            self.board[w, z, y, x] = 0
            self.current_player = player
            if w != self.current_w:
                self.change_w_slice(w)
            else:
                self.draw_cube()
            self.player_label.config(
                text=f"Ход: {'X' if self.current_player == 1 else 'O'}",
                fg="#2196F3" if self.current_player == 1 else "#FF5252"
            )
            self.status_label.config(
                text=f"Ход отменен. Возврат к W={w}, Z={z}, Y={y}, X={x}."
            )

def main():
    root = tk.Tk()
    root.geometry("1000x900")
    root.configure(bg="#F5F5F5")
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1000
    window_height = 900
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    game = FourDTicTacToeSpaced(root)
    root.mainloop()


if __name__ == "__main__":
    main()