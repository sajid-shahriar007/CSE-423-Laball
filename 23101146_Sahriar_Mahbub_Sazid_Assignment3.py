from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import random


width, height = 1024, 768  


grid_size = 8  
cell_size = 2.5  


player_pos = [0.0, 0.0]     
player_angle = 0.0
bullets = []  
enemies = [[random.uniform(-15, 15), random.uniform(-15, 15)] for _ in range(8)]  
player_health = 10  
is_game_over = False


camera_mode = 0 
camera_distance = 15.0  
camera_height = 20.0  
camera_angle_off = 0.0

spawn_timer = 0
spawn_interval = 80  

player_score = 0
missed_bullets = 0

cheat_mode     = False
auto_follow    = False

cheat_cooldown = 0
CHEAT_COOLDOWN_FRAMES = 20  

max_enemies = 12  

def init():
    glClearColor(0.1, 0.1, 0.2, 1.0)  
    glEnable(GL_DEPTH_TEST)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h, 1, 100)
    glMatrixMode(GL_MODELVIEW)

def draw_grid():
    for i in range(-grid_size, grid_size):
        for j in range(-grid_size, grid_size):
            glColor3f(0.8, 0.8, 1.0) if (i + j) % 2 == 0 else glColor3f(0.7, 0.4, 1.0)  
            glBegin(GL_QUADS)
            glVertex3f(i * cell_size, 0, j * cell_size)
            glVertex3f((i + 1) * cell_size, 0, j * cell_size)
            glVertex3f((i + 1) * cell_size, 0, (j + 1) * cell_size)
            glVertex3f(i * cell_size, 0, (j + 1) * cell_size)
            glEnd()

def draw_boundaries():
    glColor3f(0.2, 0.8, 0.2)  
    wall_height = 6  
    length = grid_size * 2 * cell_size

    def draw_wall(x1, z1, x2, z2):
        glBegin(GL_QUADS)
        glVertex3f(x1, 0, z1)
        glVertex3f(x2, 0, z2)
        glVertex3f(x2, wall_height, z2)
        glVertex3f(x1, wall_height, z1)
        glEnd()

    draw_wall(-length/2, -length/2, length/2, -length/2)
    draw_wall(-length/2, length/2, length/2, length/2)
    draw_wall(-length/2, -length/2, -length/2, length/2)
    draw_wall(length/2, -length/2, length/2, length/2)

def draw_bullets():
    glColor3f(1.0, 0.8, 0.0)  
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet[0], 1.0, bullet[1])
        glutSolidSphere(0.15, 10, 10)  
        glPopMatrix()

def draw_health():
    glColor3f(1, 1, 1)
    def draw_text(x, y, text):
        glWindowPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    draw_text(15, height - 25, f"Health: {player_health}")
    draw_text(15, height - 50, f"Score: {player_score}")
    draw_text(15, height - 75, f"Missed: {missed_bullets}")


def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], 0.0, player_pos[1])
    glRotatef(player_angle, 0.0, 1.0, 0.0)

    if is_game_over:
        glRotatef(90, 0.0, 0.0, 1.0)

    glTranslatef(0.0, 1.5, 0.0)

    # Head
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1) 
    glTranslatef(0.0, 1.25, 0.0)  
    glutSolidSphere(0.5, 20, 20)
    glPopMatrix()

    # Body
    glPushMatrix()
    glColor3f(0.2, 0.8, 0.2)  
    glScalef(1.0, 2.0, 0.5)
    glutSolidCube(1.0)
    glPopMatrix()

    # Arms
    for j in (-0.75, 0.75):
        glPushMatrix()
        glColor3f(1.0, 0.9, 0.7)  
        glTranslatef(j, 1.0, 0.0)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.2, 0.2, 1.0, 12, 12)
        glPopMatrix()

    # Legs
    for j in (-0.3, 0.3):
        glPushMatrix()
        glColor3f(0.1, 0.1, 0.8)  
        glTranslatef(j, -1.0, 0.0)
        glScalef(0.3, 1.5, 0.3)
        glutSolidCube(1.0)
        glPopMatrix()

    # Gun
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)  
    glTranslatef(0.0, 0.5, 1.0)
    glRotatef(180.0, 0.0, 1.0, 0.0)
    glScalef(0.2, 0.2, 1.0)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()

def draw_enemies():
    for i in enemies:
        glPushMatrix()
        glTranslatef(i[0], 0.5, i[1])  

        glPushMatrix()
        glColor3f(0.9, 0.1, 0.1) 
        glutSolidSphere(0.5, 20, 20)
        glPopMatrix()


        glPushMatrix()
        glColor3f(0.9, 0.7, 0.7)  
        glTranslatef(0.0, 0.6, 0.0)  
        glutSolidSphere(0.3, 20, 20)
        glPopMatrix()

        glPopMatrix()


def is_player_hit(enemy, threshold=1.2):  
    dx = player_pos[0] - enemy[0]
    dz = player_pos[1] - enemy[1]
    return math.hypot(dx, dz) < threshold

def check_collision(b, e, threshold=1.2): 
    dx = b[0] - e[0]
    dz = b[1] - e[1]
    return math.hypot(dx, dz) < threshold

def update(value):
    global bullets, enemies, player_health, is_game_over, spawn_timer
    global player_score, missed_bullets, player_angle
    global cheat_mode, cheat_cooldown  
    global max_enemies  

    if is_game_over:
        return  

    if cheat_mode:
        player_angle = (player_angle + 2) % 360  

        
        if cheat_cooldown == 0:
            for e in enemies:
                dx = e[0] - player_pos[0]
                dz = e[1] - player_pos[1]
                angle_to_e = (math.degrees(math.atan2(dx, dz)) + 360) % 360
                diff = ((angle_to_e - player_angle + 180) % 360) - 180
                if abs(diff) < 8: 
                    rad = math.radians(player_angle)
                    bx = player_pos[0] + math.sin(rad)
                    bz = player_pos[1] + math.cos(rad)
                    bullets.append([bx, bz, player_angle])
                    print("Player bullet fired")  
                    cheat_cooldown = 4  
                    break  
    if cheat_cooldown > 0:
        cheat_cooldown -= 1

 
    bullet_speed = 0.3  
    enemy_speed = 0.008  

    for b in bullets:
        rad = math.radians(b[2])
        b[0] += bullet_speed * math.sin(rad)
        b[1] += bullet_speed * math.cos(rad)


    for e in enemies:
        dx = player_pos[0] - e[0]
        dz = player_pos[1] - e[1]
        dist = math.hypot(dx, dz)
        if dist > 0.001:
            e[0] += enemy_speed * dx / dist
            e[1] += enemy_speed * dz / dist

   
    new_enemies = []
    for e in enemies:
        if any(check_collision(b, e) for b in bullets):
            player_score += 2  
            print(f"Enemy hit! Score now {player_score}")
        else:
            new_enemies.append(e)
    enemies = new_enemies

   
    out_of_bounds = [b for b in bullets if abs(b[0]) >= 60 or abs(b[1]) >= 60]  
    missed_bullets += len(out_of_bounds)
    if len(out_of_bounds) > 0:
        print(f"Bullet missed: {missed_bullets}") 
    bullets[:] = [b for b in bullets if abs(b[0]) < 60 and abs(b[1]) < 60]


    for e in enemies[:]:
        if is_player_hit(e):
            player_health -= 1
            enemies.remove(e)
            print(f"Player hit! Health now {player_health}")
            break

    if player_health <= 0:
        is_game_over = True
        print("GAME OVER")  


    if len(enemies) < max_enemies:
        
        enemies.append([random.uniform(-15, 15), random.uniform(-15, 15)])  

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    rad = math.radians(player_angle + camera_angle_off)

    if camera_mode == 0:
        
        cam_x = player_pos[0] - camera_distance * math.sin(rad)
        cam_z = player_pos[1] - camera_distance * math.cos(rad)
        cam_y = camera_height  
        gluLookAt(cam_x, cam_y, cam_z,
                  player_pos[0], 1.0, player_pos[1],
                  0, 1, 0)
    else:
        
        eye_offset = 0.6  
        forward_offset = 0.8  

        cam_x = player_pos[0] + forward_offset * math.sin(rad)
        cam_z = player_pos[1] + forward_offset * math.cos(rad)
        cam_y = 1.5 + eye_offset

        
        if cheat_mode and auto_follow and enemies:
            
            e = min(enemies, key=lambda e: (e[0]-player_pos[0])**2 + (e[1]-player_pos[1])**2)
            dx, dz = e[0] - player_pos[0], e[1] - player_pos[1]
            rad_e = math.atan2(dx, dz)
            look_x = player_pos[0] + math.sin(rad_e)
            look_z = player_pos[1] + math.cos(rad_e)
            look_y = cam_y
        else:
            
            look_x = cam_x + math.sin(rad)
            look_z = cam_z + math.cos(rad)
            look_y = cam_y  

        gluLookAt(cam_x, cam_y, cam_z,
                  look_x, look_y, look_z,
                  0, 1, 0)

    draw_grid()
    draw_boundaries()
    draw_player()
    draw_bullets()
    draw_enemies()
    draw_health()

    glutSwapBuffers()
    
def reset_game():
    global player_pos, player_health, enemies, bullets, is_game_over
    global camera_height, player_score, missed_bullets, spawn_timer

    player_pos = [0.0, 0.0]
    player_health = 5  
    bullets.clear()
    enemies = [[random.uniform(-15, 15), random.uniform(-15, 15)] for _ in range(8)]  
    player_score = 0
    missed_bullets = 0
    spawn_timer = 0
    is_game_over = False
    camera_height = 20.0  

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)  

def keyboard(key, x, y):
    global player_pos, player_angle, cheat_mode, auto_follow

    speed = 0.7  
    angle_rad = math.radians(player_angle)

    if key == b'w': 
        player_pos[0] += speed * math.sin(angle_rad)
        player_pos[1] += speed * math.cos(angle_rad)
    elif key == b's':  
        player_pos[0] -= speed * math.sin(angle_rad)
        player_pos[1] -= speed * math.cos(angle_rad)
    elif key == b'a':  
        player_angle += 7  
    elif key == b'd':  
        player_angle -= 7  
        
    elif key == b'r':  
        reset_game()
    elif key == b'c':  
        cheat_mode = not cheat_mode
        print(f"Cheat mode {'enabled' if cheat_mode else 'disabled'}")
    elif key == b'v' and cheat_mode: 
        auto_follow = not auto_follow
        print(f"Auto-follow {'enabled' if auto_follow else 'disabled'}")

    glutPostRedisplay()

def mouse(button, state, x, y):
    global bullets, camera_mode
    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON and not is_game_over:
            rad = math.radians(player_angle)
            bx = player_pos[0] + math.sin(rad)
            bz = player_pos[1] + math.cos(rad)
            bullets.append([bx, bz, player_angle])
            print("Player bullet fired")
        elif button == GLUT_RIGHT_BUTTON:
            camera_mode = 1 - camera_mode
            print("Camera toggled:", "First Person" if camera_mode else "Third Person")

        glutPostRedisplay() 

def specialKeyListener(key, x, y):
    global camera_height, camera_angle_off

    if key == GLUT_KEY_UP:
        camera_height += 1.0
    elif key == GLUT_KEY_DOWN:
        camera_height = max(1.0, camera_height - 1.0)
    elif key == GLUT_KEY_LEFT:
        camera_angle_off -= 5.0
    elif key == GLUT_KEY_RIGHT:
        camera_angle_off += 5.0

    glutPostRedisplay()           

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Bullet Frenzy")
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutSpecialFunc(specialKeyListener)
    glutTimerFunc(16, update, 0)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()