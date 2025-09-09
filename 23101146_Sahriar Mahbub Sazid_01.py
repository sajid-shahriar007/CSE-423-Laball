#Task 1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

width, height = 500, 300

bg_current = [0.0, 0.0, 0.1] 
bg_target = [0.9, 0.9, 0.9]   
bg_transition_speed = 0.02
transition_progress = 0.0

drops = []
drop_velocity = 15
horizontal_bend = 0.0

def point_size(a, b, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(a, b)
    glEnd()

def create_building():
     
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)
    glVertex2d(-800, 0)
    glVertex2d(800, 0)
    glVertex2d(0, 600)
    glEnd()

     
    glBegin(GL_TRIANGLES)
    glColor3f(0.6, 0.6, 0.6)
    glVertex2d(-700, 0)
    glVertex2d(-700, -500)
    glVertex2d(700, -500)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2d(-700, 0)
    glVertex2d(-700, 0)
    glVertex2d(700, -500)
    glEnd()


    
    glBegin(GL_TRIANGLES)
    glColor3f(0.3, 0.1, 0.0)
    glVertex2f(-50, -500)
    glVertex2f(-50, -300)
    glVertex2f(50, -500)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(50, -300)
    glVertex2f(-50, -300)
    glVertex2f(50, -500)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2d(-450, -300)
    glVertex2d(-450, -150)
    glVertex2d(-325, -300)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2d(-325, -300)
    glVertex2d(-450, -150)
    glVertex2d(-325, -150)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2d(450, -300)
    glVertex2d(450, -150)
    glVertex2d(325, -300)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2d(325, -300)
    glVertex2d(450, -150)
    glVertex2d(325, -150)
    glEnd()

def generate_raindrop():

    x_pos = random.uniform(-1900, 1900)
    y_pos = 1080
    drops.append([x_pos, y_pos])

def draw_raindrops():
    global drops, horizontal_bend
    glColor3f(0.7, 0.7, 1.0)
    glLineWidth(2)
    for d in drops:
        glBegin(GL_LINES)
        glVertex2f(d[0], d[1])
        glVertex2f(d[0], d[1] - 10)
        glEnd()
        d[1] -= drop_velocity
        d[0] += horizontal_bend 
        if d[1] < -1080:
            drops.remove(d)

def bg_transition():
    global bg_current, bg_target, transition_progress, bg_transition_speed
    for i in range(3):
        bg_current[i] += (bg_target[i] - bg_current[i]) * bg_transition_speed

def handle_keyboard(key, x, y):
    global transition_progress, bg_target
    if key == b'c':  
        if bg_target == [0.0, 0.0, 0.1]:
            bg_target = [0.9, 0.9, 0.9]
        else:
            bg_target = [0.0, 0.0, 0.1]
    elif key == b'a': 
        global horizontal_bend
        horizontal_bend = max(horizontal_bend - 1, -30)
    elif key == b'd': 
        horizontal_bend = min(horizontal_bend + 1, 30)
    bg_transition()    
    glutPostRedisplay()
    

def handle_special_keys(key, x, y):
    global horizontal_bend
    if key == GLUT_KEY_LEFT:
        horizontal_bend -= 1.0
        print("Left shift")
        if horizontal_bend < -30:
            horizontal_bend = -30
    elif key == GLUT_KEY_RIGHT:
        horizontal_bend += 1.0
        print("Right shift")
        if horizontal_bend > 30:
            horizontal_bend = 30
    glutPostRedisplay()

def display():
    glClearColor(*bg_current, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    create_building()
    draw_raindrops()

    glutSwapBuffers()

def update():
    generate_raindrop()
    bg_transition()
    glutPostRedisplay()

def main():
    global width, height
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(0,0)
    glutCreateWindow(b"A House in Rainfall")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1900, 1900, -1080, 1080)
    glClearColor(0, 0, 0, 0)

    glutDisplayFunc(display)
    glutIdleFunc(update)
    glutKeyboardFunc(handle_keyboard)
    glutSpecialFunc(handle_special_keys)

    glutMainLoop()

if __name__ == "__main__":
    main()




#Task 2

# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random
# import sys


# WIDTH = 1280
# HEIGHT = 720

# particles = []
# stopped = False
# blink_frame = 0


# class Particle:
#     def __init__(self, x_ord, y_ord):
#         self.x = x_ord
#         self.y = y_ord
#         self.vel_x = random.choice([-1, 1]) * random.uniform(0.1, 0.3)
#         self.vel_y = random.choice([-1, 1]) * random.uniform(0.1, 0.3)
#         self.color = (random.random(), random.random(), random.random())
#         self.is_blinking = False
#         self.is_visible = True


# def setup_view():
#     glClearColor(0.0, 0.0, 0.0, 1.0)
#     gluOrtho2D(0, WIDTH, 0, HEIGHT)
#     glPointSize(15)


# def render():
#     glClear(GL_COLOR_BUFFER_BIT)
#     for p in particles:
#         if p.is_visible:
#             glColor3fv(p.color)
#             glBegin(GL_POINTS)
#             glVertex2f(p.x, p.y)
#             glEnd()
#     glutSwapBuffers()


# def update_scene():
#     global blink_frame

#     if not stopped:
#         for p in particles:
#             p.x += p.vel_x
#             p.y += p.vel_y

#             if p.x <= 0 or p.x >= WIDTH:
#                 p.vel_x *= -1
#             if p.y <= 0 or p.y >= HEIGHT:
#                 p.vel_y *= -1

        
#         if blink_frame % 20 == 0:
#             for p in particles:
#                 if p.is_blinking:
#                     p.is_visible = not p.is_visible

#         blink_frame += 1

#     glutPostRedisplay()


# def on_mouse_click(button, state, x, y):
#     if state == GLUT_DOWN:
#         flipped_y = HEIGHT - y

#         if button == GLUT_RIGHT_BUTTON:
#             particles.append(Particle(x, flipped_y))
#             print(f"[+] Particle added at ({x}, {flipped_y})")

#         elif button == GLUT_LEFT_BUTTON:
#             any_blinking = any(p.is_blinking for p in particles)
#             for p in particles:
#                 p.is_blinking = not any_blinking
#                 if not p.is_blinking:
#                     p.is_visible = True
#             print(f"[~] Blinking {'enabled' if not any_blinking else 'disabled'} for all particles")


# def on_key_press(key, x, y):
#     global stopped
#     if key == b'\x1b': 
#         print("[x] Exiting")
#         sys.exit()
#     elif key == b' ':
#         stopped = not stopped
#         print(f"[||] {'Paused' if stopped else 'Resumed'}")


# def on_special_key(key, x, y):
#     if key == GLUT_KEY_UP:
#         for p in particles:
#             p.vel_x *= 1.1
#             p.vel_y *= 1.1
#         print("[↑] Increased speed")
#     elif key == GLUT_KEY_DOWN:
#         for p in particles:
#             p.vel_x *= 0.9
#             p.vel_y *= 0.9
#         print("[↓] Decreased speed")


# def main():
#     glutInit(sys.argv)
#     glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
#     glutInitWindowSize(WIDTH, HEIGHT)
#     glutCreateWindow(b"The Amazing Box")
#     setup_view()
#     glutDisplayFunc(render)
#     glutIdleFunc(update_scene)
#     glutMouseFunc(on_mouse_click)
#     glutKeyboardFunc(on_key_press)
#     glutSpecialFunc(on_special_key)
#     glutMainLoop()


# if __name__ == '__main__':
#     main()