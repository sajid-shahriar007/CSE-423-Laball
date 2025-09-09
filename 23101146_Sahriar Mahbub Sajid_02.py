from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


basket_left_inner, basket_left_outer, basket_right_inner, basket_right_outer = 5, 25, 200, 220
basket_bottom, basket_top = 10, 30


paused = False
restart_flag = False
game_over = False
score = 0


gem_position = [random.randint(60, 440), 480]
gem_color = [random.uniform(0.5, 1.0) for _ in range(3)]

fall_speed = 0.0
game_start_time = time.time()


def draw_pixel(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def find_zone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) > abs(dy):
        if dx > 0 and dy > 0: return 0
        elif dx < 0 and dy > 0: return 3
        elif dx < 0 and dy < 0: return 4
        else: return 7
    else:
        if dx > 0 and dy > 0: return 1
        elif dx < 0 and dy > 0: return 2
        elif dx < 0 and dy < 0: return 5
        else: return 6

def transform_zone_coords(zone, x, y):
    return [
        (x, y), (y, x), (-y, x), (-x, y),
        (-x, -y), (-y, -x), (-y, x), (x, -y)
    ][zone]

def inverse_transform_zone(zone, x, y):
    return [
        (x, y), (y, x), (-y, -x), (-x, y),
        (-x, -y), (-y, -x), (y, -x), (x, -y)
    ][zone]

def draw_line(zone, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    d = 2 * dy - dx
    E = 2 * dy
    NE = 2 * (dy - dx)
    x, y = x0, y0
    while x <= x1:
        rx, ry = inverse_transform_zone(zone, x, y)
        draw_pixel(rx, ry)
        if d <= 0:
            d += E
        else:
            y += 1
            d += NE
        x += 1

def draw_symmetric(x0, y0, x1, y1):
    zone = find_zone(x0, y0, x1, y1)
    ax, ay = transform_zone_coords(zone, x0, y0)
    bx, by = transform_zone_coords(zone, x1, y1)
    draw_line(zone, ax, ay, bx, by)


def draw_basket():
    glColor3f(1, 0, 0) if game_over else glColor3f(1, 1, 1)
    draw_symmetric(basket_left_outer, basket_bottom, basket_right_inner, basket_bottom)
    draw_symmetric(basket_left_inner, basket_top, basket_left_outer, basket_bottom)
    draw_symmetric(basket_right_inner, basket_bottom, basket_right_outer, basket_top)
    draw_symmetric(basket_left_inner, basket_top, basket_right_outer, basket_top)

def move_basket(key, x, y):
    global basket_left_inner, basket_left_outer, basket_right_inner, basket_right_outer
    if not paused and not game_over:
        if key == GLUT_KEY_RIGHT and basket_right_outer < 480:
            basket_left_inner += 12
            basket_left_outer += 12
            basket_right_inner += 12
            basket_right_outer += 12
            print("Right Key Pressed")
        elif key == GLUT_KEY_LEFT and basket_left_inner > 0:
            basket_left_inner -= 12
            basket_left_outer -= 12
            basket_right_inner -= 12
            basket_right_outer -= 12
            print("Left Key Pressed")
    glutPostRedisplay()

def check_gem_catch(gx, gy):
    global score, game_over, gem_position, gem_color
    if basket_left_outer < gx < basket_right_inner and basket_bottom < gy < basket_top:
        score += 1
        print(f"Score: {score}")
        gem_position = [random.randint(60, 440), 480]
        gem_color = [random.uniform(0.5, 1.0) for _ in range(3)]
    elif gy < 0:
        print(f"Game Over! Total Score: {score}")
        game_over = True


def draw_gem(gx, gy):
    check_gem_catch(gx, gy)
    glColor3f(*gem_color)
    draw_symmetric(gx, gy + 10, gx + 14, gy)
    draw_symmetric(gx + 14, gy, gx, gy - 10)
    draw_symmetric(gx, gy - 10, gx - 14, gy)
    draw_symmetric(gx - 14, gy, gx, gy + 10)



def draw_restart_btn():
    glColor3f(0, 1, 1)
    draw_symmetric(40, 430, 90, 430)
    draw_symmetric(65, 435, 40, 430)
    draw_symmetric(65, 425, 40, 430)

def draw_exit_btn():
    glColor3f(1, 0, 0)
    draw_symmetric(420, 420, 470, 470)
    draw_symmetric(420, 470, 470, 420)

def draw_play_btn():
    glColor3f(1, 1, 0)
    draw_symmetric(250, 470, 250, 420)
    draw_symmetric(255, 470, 255, 420)

def draw_pause_btn():
    glColor3f(1, 1, 0)
    draw_symmetric(250, 470, 250, 420)
    draw_symmetric(250, 470, 270, 445)
    draw_symmetric(250, 420, 270, 445)

def mouse_click(button, state, x, y):
    global paused, basket_left_inner, basket_left_outer, basket_right_inner, basket_right_outer
    global score, restart_flag, game_over, gem_position, game_start_time
    y = 500 - y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 250 <= x <= 270 and 420 <= y <= 470:
            paused = not paused
            print("Paused"if paused else"Resumed")
        elif 420 <= x <= 470 and 420 <= y <= 470:
            print(f"Goodbye! Total Score: {score}")
            game_over = True
        elif 40 <= x <= 90 and 425 <= y <= 435:
            basket_left_inner, basket_left_outer, basket_right_inner, basket_right_outer = 40, 70, 180, 210
            score = 0
            gem_position = [random.randint(60, 440), 480]
            game_over = False
            paused = False
            game_start_time = time.time()
            print("Restarting Game")
    glutPostRedisplay()


def update_game():
    global gem_position, fall_speed
    if not paused and not game_over:
        fall_speed = 0.2 + (time.time() - game_start_time) / 15
        gem_position[1] -= fall_speed
    glutPostRedisplay()

def setup_projection():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def render_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    draw_basket()
    draw_restart_btn()
    draw_exit_btn()
    draw_gem(*gem_position)
    draw_pause_btn() if paused else draw_play_btn()
    if game_over:
        glutLeaveMainLoop()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Gem Catcher")
glutDisplayFunc(render_scene)
glutSpecialFunc(move_basket)
glutMouseFunc(mouse_click)
glutIdleFunc(update_game)
glutMainLoop()
