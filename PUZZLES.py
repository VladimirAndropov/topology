import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State, callback_context, ALL
import uuid

# === Логика головоломки (без изменений) ===
def create_puzzle():
    arr = np.arange(1, 17).reshape((2, 2, 2, 2))
    arr[1, 1, 1, 1] = 0
    return arr.copy()

def find_empty(puzzle):
    return tuple(np.argwhere(puzzle == 0)[0])

def get_neighbors(pos):
    neighbors = []
    pos = np.array(pos)
    for dim in range(4):
        for delta in (-1, 1):
            new_pos = pos.copy()
            new_pos[dim] += delta
            if 0 <= new_pos[dim] <= 1:
                neighbors.append(tuple(new_pos))
    return neighbors

def can_move(puzzle, tile_pos):
    empty = find_empty(puzzle)
    return tile_pos in get_neighbors(empty)

def move_tile(puzzle, tile_pos):
    empty = find_empty(puzzle)
    if tile_pos in get_neighbors(empty):
        puzzle[tile_pos], puzzle[empty] = puzzle[empty], puzzle[tile_pos]
        return True
    return False

def is_solved(puzzle):
    return np.array_equal(puzzle, create_puzzle())

def project_4d_to_3d():
    coords_4d, coords_3d = [], []
    for w in range(2):
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    coords_4d.append((w, x, y, z))
                    X, Y, Z = x, y, z + 0.4 * w
                    coords_3d.append((X, Y, Z))
    return np.array(coords_4d), np.array(coords_3d)

def plot_puzzle(puzzle):
    coords_4d, coords_3d = project_4d_to_3d()
    labels, colors = [], []
    for c4 in coords_4d:
        val = puzzle[tuple(c4)]
        labels.append("" if val == 0 else str(val))
        colors.append(0 if val == 0 else val)

    x, y, z = coords_3d[:, 0], coords_3d[:, 1], coords_3d[:, 2]

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers+text',
        marker=dict(
            size=30,
            color=colors,
            colorscale='Viridis',
            cmin=1,
            cmax=15,
            line=dict(width=2, color='black'),
            showscale=False
        ),
        text=labels,
        textfont=dict(size=12, color='black'),
        hoverinfo='text',
        hovertext=[f"w={c[0]}, x={c[1]}, y={c[2]}, z={c[3]} → {puzzle[tuple(c)] or 'пусто'}" for c in coords_4d]
    ))

    # Рёбра гиперкуба
    idx_map = {tuple(c): i for i, c in enumerate(coords_4d)}
    edges = []
    for i, c in enumerate(coords_4d):
        for dim in range(4):
            neighbor = list(c)
            neighbor[dim] = 1 - neighbor[dim]
            neighbor = tuple(neighbor)
            if neighbor in idx_map and i < idx_map[neighbor]:
                edges.append((i, idx_map[neighbor]))

    ex, ey, ez = [], [], []
    for i, j in edges:
        ex += [x[i], x[j], None]
        ey += [y[i], y[j], None]
        ez += [z[i], z[j], None]

    fig.add_trace(go.Scatter3d(
        x=ex, y=ey, z=ez,
        mode='lines',
        line=dict(color='lightgray', width=1),
        hoverinfo='skip'
    ))

    fig.update_layout(
        title="4D-15 Puzzle (веб-версия)",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z (смещение по W)',
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=500
    )
    return fig

# === Инициализация Dash ===
app = Dash(__name__)
app.title = "4D-15 Puzzle"

# Глобальное состояние (в продакшене — через dcc.Store, но для простоты используем мутабельный объект)
class GameState:
    def __init__(self):
        self.puzzle = create_puzzle()
        self.moves = 0
        self.solved = False
        self.session_id = str(uuid.uuid4())

game = GameState()

# === Мутация: перемешиваем один раз при старте ===
np.random.seed(42)
for _ in range(120):
    empty = find_empty(game.puzzle)
    neighbors = get_neighbors(empty)
    nxt = neighbors[np.random.randint(len(neighbors))]
    game.puzzle[empty], game.puzzle[nxt] = game.puzzle[nxt], game.puzzle[empty]

# === Layout ===
app.layout = html.Div([
    html.H1("🎮 4D-15 Puzzle", style={'textAlign': 'center'}),
    html.Div(id='status', style={'textAlign': 'center', 'fontSize': 20, 'marginBottom': 20}),
    html.Div([
        html.Div([
            dcc.Graph(id='puzzle-graph', style={'height': '500px'})
        ], style={'width': '65%', 'display': 'inline-block'}),
        html.Div([
            html.H3("Доступные ходы:", id='moves-title'),
            html.Div(id='move-buttons', style={'marginTop': 20})
        ], style={'width': '34%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': 20})
    ], style={'padding': '20px'}),
    html.Div([
        html.Button("🔄 Новая игра", id='reset', n_clicks=0, style={'margin': '0 auto', 'display': 'block'})
    ], style={'textAlign': 'center', 'marginTop': 20})
])

# === Callbacks ===
@app.callback(
    [Output('puzzle-graph', 'figure'),
     Output('move-buttons', 'children'),
     Output('status', 'children'),
     Output('moves-title', 'children')],
    Input('reset', 'n_clicks'),
    Input({'type': 'move-btn', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=False
)
def update_game(reset_clicks, move_clicks_list):
    ctx = callback_context
    triggered_id = ctx.triggered_id  # ← ЭТА СТРОКА ОБЯЗАТЕЛЬНА!

    # === Сброс игры ===
    if triggered_id == 'reset':
        new_puzzle = create_puzzle()
        # Перемешиваем легальными ходами
        np.random.seed()
        for _ in range(120):
            empty = find_empty(new_puzzle)
            neighbors = get_neighbors(empty)
            nxt = neighbors[np.random.randint(len(neighbors))]
            new_puzzle[empty], new_puzzle[nxt] = new_puzzle[nxt], new_puzzle[empty]
        game.puzzle = new_puzzle
        game.moves = 0
        game.solved = False

    # === Обработка хода ===
    elif isinstance(triggered_id, dict) and triggered_id.get('type') == 'move-btn':
        import ast
        try:
            # Получаем строку вида "[1, 0, 1, 1]"
            index_str = triggered_id['index']
            tile_list = ast.literal_eval(index_str)  # → [1, 0, 1, 1]
            tile = tuple(tile_list)                  # → (1, 0, 1, 1)

            # Проверка корректности
            if len(tile) == 4 and all(isinstance(x, int) for x in tile):
                if can_move(game.puzzle, tile):
                    move_tile(game.puzzle, tile)
                    game.moves += 1
                    print(f"✅ Успешный ход: {tile}")
                else:
                    print(f"❌ Невозможный ход: {tile} не сосед пустой ячейки")
            else:
                print(f"⚠️ Некорректные координаты: {tile}")
        except Exception as e:
            print(f"💥 Ошибка парсинга: {e}")
            print(f"   Получено: {triggered_id.get('index')}")

    # === Обновление интерфейса ===
    solved = is_solved(game.puzzle)
    status = "🎉 Победа!" if solved else f"Ходов: {game.moves}"
    title = "Доступные ходы:" if not solved else "Игра решена!"

    # Генерация кнопок
    buttons = []
    if not solved:
        empty = find_empty(game.puzzle)
        for tile in get_neighbors(empty):
            val = game.puzzle[tile]
            clean_tile = [int(x) for x in tile]  # ← Гарантируем обычные int
            buttons.append(
                html.Button(
                    f"Move {clean_tile} → {val}",
                    id={'type': 'move-btn', 'index': str(clean_tile)},
                    n_clicks=0,
                    style={'display': 'block', 'margin': '5px', 'padding': '10px', 'width': '100%'}
                )
            )
    else:
        buttons = [html.P("🏆 Победа! Нажмите 'Новая игра', чтобы начать снова.")]

    return plot_puzzle(game.puzzle), buttons, status, title

def handle_move(n_clicks_list):
    if not any(n_clicks_list):
        return 0

    ctx = callback_context
    prop_id = ctx.triggered[0]['prop_id']
    # Извлекаем tile из id
    tile_str = prop_id.split('index":"')[1].split('"')[0]
    tile = eval(tile_str)  # безопасно, т.к. только (0/1,0/1,0/1,0/1)

    if can_move(game.puzzle, tile):
        move_tile(game.puzzle, tile)
        game.moves += 1

    return 0  # dummy

# === Запуск ===
if __name__ == '__main__':
    app.run(debug=True)