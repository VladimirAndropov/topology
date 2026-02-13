import pygame
import sys
import math
import numpy as np
from itertools import product

# ---------- НАСТРОЙКИ ----------
WINDOW_W, WINDOW_H = 1100, 800
BG = (12, 12, 18)
EDGE_COLOR = (180, 200, 255)
VERT_COLOR = (255, 220, 100)
HIGHLIGHT = (255, 120, 120)
FPS = 60
SCALE_2D = 220.0
CAM_Z = 8.0
AUTO_TOGGLE_SPEED = 0.3

# ---------- ПОСТРОЕНИЕ ТЕССЕРАКТА ----------
def tesseract_vertices(scale=1.0):
    verts = []
    for coords in product([-1.0, 1.0], repeat=4):
        verts.append(np.array(coords, dtype=float) * scale)
    return verts

def tesseract_edges():
    verts = list(product([-1,1], repeat=4))
    index = {v:i for i,v in enumerate(verts)}
    edges = []
    for v in verts:
        i = index[v]
        for axis in range(4):
            w = list(v)
            w[axis] *= -1
            j = index[tuple(w)]
            if (j,i) not in edges:
                edges.append((i,j))
    return edges

# ---------- МАТРИЦЫ ВРАЩЕНИЯ И ПРОЕКЦИИ ----------
def rotation_matrix_4d(i, j, theta):
    R = np.eye(4)
    c = math.cos(theta)
    s = math.sin(theta)
    R[i,i] = c
    R[j,j] = c
    R[i,j] = -s
    R[j,i] = s
    return R

def combined_rotation_4d(thetas):
    R = np.eye(4)
    mapping = {
        'xw': (0,3),
        'yw': (1,3),
        'zw': (2,3),
        'xy': (0,1),
        'xz': (0,2),
        'yz': (1,2),
    }
    order = ['xw','yw','zw','xy','xz','yz']
    for key in order:
        ang = thetas.get(key, 0.0)
        if abs(ang) > 1e-9:
            i,j = mapping[key]
            R = rotation_matrix_4d(i,j,ang) @ R
    return R

def proj4_to_3_linear():
    P = np.zeros((3,4))
    P[0,0] = 1.0
    P[1,1] = 1.0
    P[2,2] = 1.0
    return P

def unfold_offset_map(verts_4d, t):
    offsets = []
    u_w = np.array([2.6, 0.0, 0.0])
    u_x = np.array([0.0, 1.2, 0.0])
    u_y = np.array([0.0, 0.0, 1.2])
    u_z = np.array([0.0, -0.9, 0.9])
    for v in verts_4d:
        x,y,z,w = v
        off = (w*u_w + x*u_x + y*u_y + z*u_z) * 0.7
        offsets.append(off * t)
    return offsets

def project_3d_to_2d(pt3):
    x,y,z = pt3
    denom = (CAM_Z - z)
    if abs(denom) < 1e-6:
        denom = 1e-6
    f = CAM_Z / denom
    sx = x * f * SCALE_2D + WINDOW_W/2
    sy = -y * f * SCALE_2D + WINDOW_H/2
    return np.array([sx, sy]), f

# ---------- ГЕОМЕТРИЯ ----------
verts4 = tesseract_vertices(scale=1.0)
edges = tesseract_edges()

# ---------- ОСНОВНОЙ ЦИКЛ ----------
def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pygame.time.Clock()

    ang = {'xw':0.4, 'yw':0.2, 'zw':0.05, 'xy':0.0, 'xz':0.0, 'yz':0.0}
    ang_vel = {'xw':0.9, 'yw':0.6, 'zw':0.25, 'xy':0.2, 'xz':0.15, 'yz':0.18}

    t = 0.0
    auto = True
    direction = 1.0
    paused = False

    P = proj4_to_3_linear()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                elif ev.key == pygame.K_SPACE:
                    paused = not paused
                elif ev.key == pygame.K_LEFT:
                    auto = False
                    t = max(0.0, t - 0.05)
                elif ev.key == pygame.K_RIGHT:
                    auto = False
                    t = min(1.0, t + 0.05)
                elif ev.key == pygame.K_a:
                    auto = not auto

        if not paused:
            for k in ang:
                ang[k] += ang_vel[k] * dt * 0.6

            if auto:
                t += direction * AUTO_TOGGLE_SPEED * dt
                if t > 1.0:
                    t = 1.0
                    direction = -direction
                elif t < 0.0:
                    t = 0.0
                    direction = -direction

        R4 = combined_rotation_4d(ang)
        offsets = unfold_offset_map(verts4, t)

        screen.fill(BG)

        pts2 = []
        pts3 = []
        for i,v in enumerate(verts4):
            v4 = v.reshape((4,1))
            v_rot = (R4 @ v4).flatten()
            base3 = (P @ v_rot).flatten()
            final3 = base3 + offsets[i]
            xy, depth = project_3d_to_2d(final3)
            pts2.append((xy, depth))
            pts3.append(final3)

        edge_draw_list = []
        for a,b in edges:
            da = pts2[a][1]
            db = pts2[b][1]
            avg = (da + db) / 2.0
            edge_draw_list.append((avg, a, b))
        edge_draw_list.sort()

        for avg, a, b in edge_draw_list:
            pa = pts2[a][0]
            pb = pts2[b][0]
            lw = int(max(1.0, ((pts2[a][1] + pts2[b][1]) / 2.0) * 3.2))
            pygame.draw.aaline(screen, EDGE_COLOR, pa, pb)
            if lw > 1:
                pygame.draw.line(screen, EDGE_COLOR, pa, pb, lw)

        vert_order = sorted([(pts2[i][1], i) for i in range(len(pts2))])
        for depth, i in vert_order:
            xy = pts2[i][0]
            r = int(max(3, depth * 6.0))
            color = VERT_COLOR if depth < 2.8 else (220,180,90)
            pygame.draw.circle(screen, color, (int(xy[0]), int(xy[1])), r)

        hv = pts2[0][0]
        pygame.draw.circle(screen, HIGHLIGHT, (int(hv[0]), int(hv[1])), 5)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run()
