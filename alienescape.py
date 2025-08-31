from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys
import math
import time

def draw_simple_text(x, y, text, r, g, b):
    """Draw text using simple patterns - more readable"""
    glColor3f(r, g, b)
    
    char_patterns = {
        'S': [(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(2,0),(1,0)],
        'C': [(0,0),(0,1),(0,2),(1,2),(2,2)],
        'O': [(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(2,0),(1,0)],
        'R': [(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(1,1),(2,0)],
        'E': [(0,0),(0,1),(0,2),(1,2),(1,1),(1,0),(2,2),(2,0)],
        'L': [(0,0),(0,1),(0,2),(1,0),(2,0)],
        'V': [(0,2),(0,1),(1,0),(2,1),(2,2)],
        'I': [(0,0),(0,1),(0,2),(1,0),(1,2)],
        'W': [(0,2),(0,1),(0,0),(1,0),(2,0),(2,1),(2,2)],
        'A': [(0,0),(0,1),(0,2),(1,2),(1,1),(2,2),(2,1),(2,0)],
        'G': [(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(1,1),(2,0)],
        'M': [(0,0),(0,1),(0,2),(1,2),(2,0),(2,1),(2,2)],
        'T': [(0,2),(1,2),(2,2),(1,1),(1,0)],
        'U': [(0,2),(0,1),(0,0),(1,0),(2,0),(2,1),(2,2)],
        'H': [(0,0),(0,1),(0,2),(1,1),(2,0),(2,1),(2,2)],
        'N': [(0,0),(0,1),(0,2),(1,1),(2,0),(2,1),(2,2)],
        'K': [(0,0),(0,1),(0,2),(1,1),(2,2),(2,0)],
        'X': [(0,0),(0,2),(1,1),(2,0),(2,2)],
        'P': [(0,0),(0,1),(0,2),(1,2),(1,1),(2,2),(2,1)],
        ':': [(1,1)],
        '/': [(0,0),(1,1),(2,2)],
        ' ': []  # Space - no pattern
    }
    
    char_spacing = 4
    pixel_size = 2
    
    for i, char in enumerate(text.upper()):
        char_x = x + i * (char_spacing * pixel_size + 2)
        pattern = char_patterns.get(char, [(1,1)])  # Default to dot for unknown chars
        
        for px, py in pattern:
            glBegin(GL_QUADS)
            glVertex2f(char_x + px * pixel_size, y + py * pixel_size)
            glVertex2f(char_x + (px + 1) * pixel_size, y + py * pixel_size)
            glVertex2f(char_x + (px + 1) * pixel_size, y + (py + 1) * pixel_size)
            glVertex2f(char_x + px * pixel_size, y + (py + 1) * pixel_size)
            glEnd()

def draw_number(x, y, number, r, g, b):
    """Draw numbers using simple patterns"""
    glColor3f(r, g, b)
    
    # Number patterns
    number_patterns = {
        '0': [(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)],
        '1': [(1,0),(1,1),(1,2),(0,1)],
        '2': [(0,2),(1,2),(2,2),(2,1),(1,1),(0,1),(0,0),(1,0),(2,0)],
        '3': [(0,2),(1,2),(2,2),(2,1),(1,1),(2,0),(1,0),(0,0)],
        '4': [(0,2),(0,1),(1,1),(2,1),(2,2),(2,0)],
        '5': [(2,2),(1,2),(0,2),(0,1),(1,1),(2,1),(2,0),(1,0),(0,0)],
        '6': [(0,0),(0,1),(0,2),(1,0),(1,1),(2,0),(2,1)],
        '7': [(0,2),(1,2),(2,2),(2,1),(1,0)],
        '8': [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)],
        '9': [(0,2),(0,1),(1,2),(1,1),(2,2),(2,1),(2,0)]
    }
    
    char_spacing = 4
    pixel_size = 2
    text = str(number)
    
    for i, char in enumerate(text):
        char_x = x + i * (char_spacing * pixel_size + 2)
        pattern = number_patterns.get(char, [(1,1)])
        
        for px, py in pattern:
            glBegin(GL_QUADS)
            glVertex2f(char_x + px * pixel_size, y + py * pixel_size)
            glVertex2f(char_x + (px + 1) * pixel_size, y + py * pixel_size)
            glVertex2f(char_x + (px + 1) * pixel_size, y + (py + 1) * pixel_size)
            glVertex2f(char_x + px * pixel_size, y + (py + 1) * pixel_size)
            glEnd()

def draw_text(x, y, text, r=1.0, g=1.0, b=1.0):
    """Draw text using simple rectangles - fallback method"""
    if any(char.isdigit() for char in text) and ':' in text:
        parts = text.split(':')
        if len(parts) == 2:
            draw_simple_text(x, y, parts[0] + ':', r, g, b)
            text_width = len(parts[0] + ':') * 10
            draw_number(x + text_width, y, parts[1].strip(), r, g, b)
            return
    
    draw_simple_text(x, y, text, r, g, b)

def create_screen_shake(intensity=0.05, duration=200):
    """Create screen shake effect"""
    global screen_shake, screen_shake_duration
    screen_shake = intensity
    screen_shake_duration = duration

def create_particle_explosion(x, y, z, color=(1.0, 0.5, 0.0)):
    """Create explosion particle effect"""
    global particle_effects
    particle_effects.append(ParticleEffect(x, y, z, "explosion", color))

def create_coin_effect(x, y, z):
    """Create coin collection effect"""
    global particle_effects
    particle_effects.append(ParticleEffect(x, y, z, "coin", (1.0, 1.0, 0.0)))


GRID_LENGTH = 11
BULLET_SPEED = 0.15
ALIEN_SPEED = 0.003
NUM_ALIENS = 3
time_counter = 0
bullets_missed = 0
combo_count = 0
combo_multiplier = 1
DOUBLE_BULLET = False
power_ups = []
kill_times = []
last_mouse_x = 400
mouse_deltas = []
is_moving = False
last_shot_time = 0
game_difficulty = 1
wave_number = 1
aliens_killed_this_wave = 0
wave_bonus = 0
health_regen_timer = 0
sprint_stamina = 100
is_sprinting = False
muzzle_flash_timer = 0
screen_shake = 0
screen_shake_duration = 0
ambient_sound_timer = 0
particle_effects = []
sprint_draining = False
spawn_timer = 0

# Scoreboard system
high_scores = []
show_scoreboard = False
player_name = "PLAYER"
max_high_scores = 10

def load_high_scores():
    """Load high scores from file"""
    global high_scores
    try:
        with open('high_scores.txt', 'r') as f:
            high_scores = []
            for line in f:
                if line.strip():
                    try:
                        name, score, level, wave = line.strip().split(',')
                        high_scores.append({
                            'name': name,
                            'score': int(float(score)),
                            'level': int(float(level)),
                            'wave': int(float(wave))
                        })
                    except (ValueError, IndexError) as e:
                        print(f"Skipping invalid high score entry: {line.strip()} - Error: {e}")
                        continue
    except FileNotFoundError:
        high_scores = []

def save_high_scores():
    """Save high scores to file"""
    global high_scores
    with open('high_scores.txt', 'w') as f:
        for entry in high_scores[:max_high_scores]:
            f.write(f"{entry['name']},{entry['score']},{entry['level']},{entry['wave']}\n")

def add_high_score(name, score, level, wave):
    """Add a new high score"""
    global high_scores
    new_entry = {
        'name': name,
        'score': score,
        'level': level,
        'wave': wave
    }
    high_scores.append(new_entry)
    high_scores.sort(key=lambda x: x['score'], reverse=True)
    high_scores = high_scores[:max_high_scores]
    save_high_scores()
    return high_scores.index(new_entry) < max_high_scores

def is_high_score(score):
    """Check if score qualifies for high score table"""
    if len(high_scores) < max_high_scores:
        return True
    if not high_scores:
        return True
    return score > min(high_scores, key=lambda x: x['score'])['score']

def draw_scoreboard():
    return


class ParticleEffect:
    def __init__(self, x, y, z, effect_type="explosion"):
        self.x = x
        self.y = y
        self.z = z
        self.type = effect_type
        self.life = 1.0
        self.particles = []
        
        if effect_type == "explosion":
            for _ in range(15):
                self.particles.append({
                    'x': x, 'y': y, 'z': z,
                    'vx': random.uniform(-0.3, 0.3),
                    'vy': random.uniform(0.1, 0.5),
                    'vz': random.uniform(-0.3, 0.3),
                    'life': random.uniform(0.5, 1.0),
                    'size': random.uniform(0.02, 0.08)
                })
        elif effect_type == "coin_collect":
            for _ in range(8):
                self.particles.append({
                    'x': x, 'y': y, 'z': z,
                    'vx': random.uniform(-0.1, 0.1),
                    'vy': random.uniform(0.2, 0.4),
                    'vz': random.uniform(-0.1, 0.1),
                    'life': random.uniform(0.3, 0.6),
                    'size': random.uniform(0.03, 0.06)
                })
    
    def update(self, dt):
        dt = dt / 1000.0
        self.life -= dt * 2
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['z'] += particle['vz'] * dt
            particle['vy'] -= 2.0 * dt  # gravity
            particle['life'] -= dt * 2
        self.particles = [p for p in self.particles if p['life'] > 0]
    
    def is_dead(self):
        return self.life <= 0 and len(self.particles) == 0
        
    def draw(self):
        if self.type == "explosion":
            glColor3f(1.0, 0.5, 0.0)
        elif self.type == "coin_collect":
            glColor3f(1.0, 1.0, 0.0)
            
        for particle in self.particles:
            alpha = particle['life']
            glPushMatrix()
            glTranslatef(particle['x'], particle['y'], particle['z'])
            glScalef(particle['size'], particle['size'], particle['size'])
            glutSolidSphere(1.0, 6, 6)
            glPopMatrix()


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]
        self.generate_maze()
        self.exit_pos = self.get_random_path()
        self.teleport_pos1, self.teleport_pos2 = self.generate_teleport_positions()
        self.coins = []
        self.generate_coins(10)
        self.aliens = []
        self.generate_aliens(NUM_ALIENS)
        self.mini_map_enabled = True
        self.ambient_objects = []
        self.generate_ambient_objects()

    def generate_maze(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = 1
        self.recursive_backtrack(1, 1)

    def recursive_backtrack(self, x, y):
        self.grid[y][x] = 0
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny][nx] == 1:
                self.grid[y + dy//2][x + dx//2] = 0
                self.recursive_backtrack(nx, ny)

    def get_random_path(self, exclude_positions=None):
        exclude_positions = exclude_positions or []
        while True:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            world_x, world_z = x + 0.5, y + 0.5
            if self.grid[y][x] == 0 and (world_x, world_z) not in exclude_positions:
                return world_x, world_z

    def generate_coins(self, count):
        exclude = [self.exit_pos, self.teleport_pos1, self.teleport_pos2]
        for _ in range(count):
            x, z = self.get_random_path(exclude)
            self.coins.append((x, z))
            exclude.append((x, z))

    def generate_teleport_positions(self):
        pos1 = self.get_random_path([self.exit_pos])
        pos2 = self.get_random_path([self.exit_pos, pos1])
        return pos1, pos2

    def generate_aliens(self, count):
        exclude = [self.exit_pos, self.teleport_pos1, self.teleport_pos2] + self.coins
        for _ in range(count):
            x, z = self.get_random_path(exclude)
            self.aliens.append(Alien(x, z))
    
    def spawn_aliens(self, count):
        """Spawn new aliens for wave progression"""
        exclude = [self.exit_pos, self.teleport_pos1, self.teleport_pos2] + self.coins
        for _ in range(count):
            x, z = self.get_random_path(exclude)
            self.aliens.append(Alien(x, z))

    def generate_ambient_objects(self):
        # Generate decorative objects in the maze
        for _ in range(random.randint(3, 8)):
            x, z = self.get_random_path(self.coins + [self.exit_pos, self.teleport_pos1, self.teleport_pos2])
            obj_type = random.choice(["crystal", "pillar", "debris"])
            self.ambient_objects.append({'x': x, 'z': z, 'type': obj_type, 'rotation': random.uniform(0, 360)})

    def remove_coin(self, x, z):
        for i, (coin_x, coin_z) in enumerate(self.coins):
            if math.sqrt((x - coin_x)**2 + (z - coin_z)**2) < 0.5:
                self.coins.pop(i)
                return True
        return False


class Alien:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.y = 0.5
        self.scale = 0.4
        self.last_hit_time = 0
        self.health = 2 + game_difficulty
        self.max_health = self.health
        self.aggression = random.uniform(0.8, 1.2)
        self.alien_type = random.choice(["scout", "warrior", "hunter"])
        self.special_timer = 0

    def move(self, maze, human):
        dx, dz = human.x - self.x, human.z - self.z
        dist = math.sqrt(dx**2 + dz**2)
        if dist > 0:
            speed_modifier = self.aggression * (1 + game_difficulty * 0.2)
            if self.alien_type == "scout":
                speed_modifier *= 1.3
            elif self.alien_type == "hunter" and dist < 3:
                speed_modifier *= 1.5
                
            new_x = self.x + (dx / dist) * ALIEN_SPEED * speed_modifier
            new_z = self.z + (dz / dist) * ALIEN_SPEED * speed_modifier
            grid_x, grid_z = int(new_x), int(new_z)
            if 0 <= grid_x < maze.width and 0 <= grid_z < maze.height and maze.grid[grid_z][grid_x] == 0:
                self.x, self.z = new_x, new_z

    def draw(self, time_counter):
        glPushMatrix()
        glTranslatef(
            self.x + 0.1 * math.sin(time_counter * 2),
            self.y,
            self.z + 0.1 * math.cos(time_counter * 2)
        )
        glScalef(self.scale, self.scale, self.scale)
        
        # Different colors for different alien types
        if self.alien_type == "scout":
            glColor3f(0.1, 0.8, 0.1)  # Bright green
        elif self.alien_type == "warrior":
            glColor3f(0.8, 0.1, 0.1)  # Red
        else:  # hunter
            glColor3f(0.6, 0.1, 0.6)  # Purple
            
        gluSphere(gluNewQuadric(), 0.5, 20, 20)
        
        # Health bar
        if self.health < self.max_health:
            glPushMatrix()
            glTranslatef(0, 1.2, 0)
            glScalef(0.8, 0.1, 0.1)
            glColor3f(1.0, 0.0, 0.0)
            glutSolidCube(1.0)
            health_ratio = self.health / self.max_health
            glTranslatef(-0.5 + health_ratio * 0.5, 0, 0.1)
            glScalef(health_ratio, 1.0, 1.0)
            glColor3f(0.0, 1.0, 0.0)
            glutSolidCube(1.0)
            glPopMatrix()
        
        # Original alien body parts with type variations
        if self.alien_type == "warrior":
            # Larger arms for warrior
            arm_scale = 1.3
            arm_length = 0.8
        else:
            arm_scale = 1.0
            arm_length = 0.6
            
        glPushMatrix()
        glTranslatef(0.4, 0, 0)
        glRotatef(45 + 20 * math.sin(time_counter * 2), 0, 0, 1)
        glColor3f(0.2, 0.7, 0.2)
        gluCylinder(gluNewQuadric(), 0.1 * arm_scale, 0.05, arm_length, 8, 8)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-0.4, 0, 0)
        glRotatef(-45 + 20 * math.cos(time_counter * 2), 0, 0, 1)
        gluCylinder(gluNewQuadric(), 0.1 * arm_scale, 0.05, arm_length, 8, 8)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 0.4, 0)
        glRotatef(30 + 20 * math.sin(time_counter * 2.5), 0, 0, 1)
        gluCylinder(gluNewQuadric(), 0.1 * arm_scale, 0.05, arm_length, 8, 8)
        glPopMatrix()
        
        # Eyes with type-specific glow
        eye_color = [1, 0, 0] if self.alien_type == "hunter" else [1, 0.5, 0]
        glPushMatrix()
        glTranslatef(0.2, 0.2, 0.6)
        glColor3f(*eye_color)
        gluSphere(gluNewQuadric(), 0.1, 10, 10)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-0.2, 0.2, 0.6)
        gluSphere(gluNewQuadric(), 0.1, 10, 10)
        glPopMatrix()
        glPopMatrix()

class Bullet:
    def __init__(self, x, y, z, angle):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle

    def move(self):
        rad = math.radians(self.angle)
        self.x += BULLET_SPEED * math.sin(rad)
        self.z += BULLET_SPEED * math.cos(rad)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(1, 0.5, 0)
        glScalef(0.1, 0.3, 0.1)
        gluSphere(gluNewQuadric(), 0.1, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(self.x, self.y - 0.05, self.z)
        glColor4f(1, 0.5, 0, 0.5)
        gluSphere(gluNewQuadric(), 0.05, 8, 8)
        glPopMatrix()

class Camera:
    def __init__(self):
        self.x = 5.5
        self.y = 15.0
        self.z = 5.5
        self.top_down = False

    def apply(self, human=None):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 800/600, 0.1, 800)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if self.top_down and human:
            self.x = human.x
            self.y = human.y + 10
            self.z = human.z
            look_x = human.x
            look_y = human.y
            look_z = human.z
            gluLookAt(self.x, self.y, self.z, look_x, look_y, look_z, 0, 0, 1)
        else:
            rad = math.radians(human.rotation)
            eye_x = human.x - 3 * math.sin(rad)
            eye_y = human.y + 2.5
            eye_z = human.z - 3 * math.cos(rad)
            look_x = human.x
            look_y = human.y + 1.7
            look_z = human.z
            gluLookAt(eye_x, eye_y, eye_z, look_x, look_y, look_z, 0, 1, 0)

    def toggle_top_down(self):
        self.top_down = not self.top_down
        print(f"Top-down mode: {self.top_down}")

class Human:
    def __init__(self, maze):
        self.x, self.z = maze.get_random_path([maze.exit_pos, maze.teleport_pos1, maze.teleport_pos2] + maze.coins)
        self.y = 0.0
        self.score = 0
        self.rotation = 0
        self.head_tilt = 0
        self.body_lean = 0
        self.lives = 5
        self.max_lives = 5
        self.coin_count = 0
        self.enemy_kills = 0
        self.has_gun = True
        self.bullets = []
        self.game_over = False
        self.game_won = False
        self.crosshair_enabled = True
        self.weapon_heat = 0
        self.max_weapon_heat = 100
        self.shield_energy = 100
        self.max_shield = 100
        self.experience = 0
        self.level = 1

    def draw(self, time_counter, top_down=False):
        global muzzle_flash_timer, screen_shake
        
        glPushMatrix()
        
        # Apply screen shake
        if screen_shake > 0:
            shake_x = random.uniform(-screen_shake, screen_shake) * 0.02
            shake_z = random.uniform(-screen_shake, screen_shake) * 0.02
            glTranslatef(shake_x, 0, shake_z)
            
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rotation, 0, 1, 0)
        glRotatef(self.body_lean, 0, 0, 1)
        
        # Apply overall scale reduction to make character smaller
        glScalef(0.6, 0.6, 0.6)  # Make character 60% of original size
        
        # Body with health-based color
        health_ratio = self.lives / self.max_lives
        glPushMatrix()
        glTranslatef(0, 1.2, 0)
        glScalef(0.3, 0.6, 0.2)
        glColor3f(0.0, 0.5 * health_ratio, 1.0)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Improved weapon logo
        glPushMatrix()
        glTranslatef(0, 1.2, 0.11)
        glScalef(0.1, 0.1, 1.0)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(0, 0.5)
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glEnd()
        glPopMatrix()
        
        # Head with smooth movement
        bob_y = is_moving and 0.05 * math.sin(time_counter * 2) or 0
        glPushMatrix()
        glTranslatef(0, 1.7, bob_y)
        glRotatef(self.head_tilt, 1, 0, 0)
        glColor3f(1.0, 0.8, 0.6)
        glutSolidSphere(0.2, 20, 20)
        
        # Eyes with dynamic glow
        glPushMatrix()
        glTranslatef(0, 0, 0.2)
        glow = 0.8 + 0.2 * math.sin(time_counter * 3)
        glColor3f(1.0 * glow, 0.0, 0.0)
        glutSolidSphere(0.05, 10, 10)
        glPopMatrix()
        glPopMatrix()
        
        # Animated legs
        leg_swing = is_moving and 20 * math.sin(time_counter * 4) or 0
        glPushMatrix()
        glTranslatef(-0.1, 0.6, 0)
        glRotatef(leg_swing, 1, 0, 0)
        glScalef(0.1, 0.6, 0.1)
        glColor3f(0.3, 0.2, 0.1)
        glutSolidCube(1.0)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.1, 0.6, 0)
        glRotatef(-leg_swing, 1, 0, 0)
        glScalef(0.1, 0.6, 0.1)
        glColor3f(0.3, 0.2, 0.1)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Enhanced arms
        arm_swing = is_moving and 20 * math.sin(time_counter * 4) or 0
        glPushMatrix()
        glTranslatef(-0.25, 1.3, 0)
        glRotatef(45 + self.body_lean, 0, 0, 1)
        glRotatef(arm_swing, 0, 1, 0)
        glScalef(0.1, 0.4, 0.1)
        glColor3f(1.0, 0.8, 0.6)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Weapon arm with recoil effect
        recoil_offset = (time_counter - last_shot_time < 0.1) and -0.05 or 0
        glPushMatrix()
        glTranslatef(0.25, 1.1, recoil_offset)
        glRotatef(-45 - self.body_lean, 0, 0, 1)
        glRotatef(-arm_swing, 0, 1, 0)
        glScalef(0.1, 0.4, 0.1)
        glColor3f(1.0, 0.8, 0.6)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Enhanced weapon with heat effects
        glPushMatrix()
        glTranslatef(0.25, 1.1, 0.25)
        glRotatef(90, 1, 0, 0)
        
        # Weapon heat coloring
        heat_ratio = self.weapon_heat / self.max_weapon_heat
        weapon_r = 0.5 + heat_ratio * 0.5
        weapon_g = 0.5 - heat_ratio * 0.3
        glColor3f(weapon_r, weapon_g, 0.5)
        gluCylinder(gluNewQuadric(), 0.05, 0.05, 0.3, 8, 8)
        
        # Muzzle flash effect
        if muzzle_flash_timer > 0:
            glPushMatrix()
            glTranslatef(0, 0, 0.3)
            flash_size = muzzle_flash_timer * 0.3
            glScalef(flash_size, flash_size, flash_size)
            glColor3f(1.0, 1.0, 0.5)
            glutSolidSphere(1.0, 8, 8)
            glPopMatrix()
            
        glPopMatrix()
        glPopMatrix()

    def move(self, dx, dz, maze):
        # Move relative to character's rotation
        speed = 0.1
        
        # Convert rotation to radians
        rad = math.radians(self.rotation)
        
        forward_x = math.sin(rad) * dz * speed
        forward_z = math.cos(rad) * dz * speed
        
        right_x = math.cos(rad) * dx * speed
        right_z = -math.sin(rad) * dx * speed
        
        new_x = self.x + forward_x + right_x
        new_z = self.z + forward_z + right_z
        
        grid_x = int(new_x)
        grid_z = int(new_z)
        if 0 <= grid_x < maze.width and 0 <= grid_z < maze.height and maze.grid[grid_z][grid_x] == 0:
            self.x, self.z = new_x, new_z

    def rotate_player(self, angle):
        self.rotation = (self.rotation + angle) % 360

    def tilt_head(self, angle):
        self.head_tilt = max(-60, min(60, self.head_tilt + angle))

    def lean_body(self, angle):
        self.body_lean = max(-15, min(15, self.body_lean + angle))
        return self.body_lean

    def check_collisions(self, maze, time_counter):
        global DOUBLE_BULLET, power_ups, bullets_missed, particle_effects, health_regen_timer
        
        if maze.remove_coin(self.x, self.z):
            self.score += 10
            self.coin_count += 1
            self.experience += 5
            
            # Add coin collection effect
            particle_effects.append(ParticleEffect(self.x, self.y + 1, self.z, "coin_collect"))
            
            print(f"Score: {self.score}, Coins: {self.coin_count}, XP: {self.experience}")
            if self.coin_count >= 10:
                self.lives = min(self.max_lives, self.lives + 1)
                self.coin_count = 0
                print(f"Extra life gained! Lives: {self.lives}")
                
        # Level up system
        xp_needed = self.level * 100
        if self.experience >= xp_needed:
            self.level += 1
            self.experience -= xp_needed
            self.max_lives += 1
            self.lives = min(self.lives + 1, self.max_lives)
            print(f"Level Up! Now level {self.level}")
            
        for alien in maze.aliens[:]:
            if math.sqrt((self.x - alien.x)**2 + (self.z - alien.z)**2) < 0.5 and time_counter - alien.last_hit_time > 1:
                damage = 1
                if self.shield_energy > 0:
                    self.shield_energy -= 30
                    damage = 0.5
                    
                self.lives -= damage
                print(f"Hit by alien! Lives left: {self.lives}, Shield: {self.shield_energy}")
                alien.last_hit_time = time_counter
                health_regen_timer = time_counter + 3  # Start regen after 3 seconds
                maze.aliens.remove(alien)
                maze.generate_aliens(1)
                break
                
        # Health regeneration
        if time_counter > health_regen_timer and self.lives < self.max_lives:
            if int(time_counter * 2) % 10 == 0:  # Slow regen
                self.lives = min(self.max_lives, self.lives + 0.1)
                
        # Shield regeneration
        if self.shield_energy < self.max_shield:
            self.shield_energy = min(self.max_shield, self.shield_energy + 0.2)
            
        exit_x, exit_z = maze.exit_pos
        if self.enemy_kills >= 15 and math.sqrt((self.x - exit_x)**2 + (self.z - exit_z)**2) < 0.5:
            self.game_won = True
            print("Game Cleared!")
            
        new_power_ups = []
        for power_up in power_ups:
            px, py, pz, type = power_up
            dist = math.sqrt((px - self.x)**2 + (pz - self.z)**2)
            if dist < 0.5:
                if type == "double":
                    DOUBLE_BULLET = time_counter
                    print("Double Bullet Activated!")
                continue
            new_power_ups.append(power_up)
        power_ups = new_power_ups
        
        if self.lives <= 0 or bullets_missed >= 15:
            if not self.game_over:
                self.game_over = True
                print("Game Over!")

    def try_teleport(self, maze):
        pos1_x, pos1_z = maze.teleport_pos1
        pos2_x, pos2_z = maze.teleport_pos2
        if math.sqrt((self.x - pos1_x)**2 + (self.z - pos1_z)**2) < 0.5:
            self.x, self.z = pos2_x, pos2_z
            print("Teleported to spot 2!")
            return True
        elif math.sqrt((self.x - pos2_x)**2 + (self.z - pos2_z)**2) < 0.5:
            self.x, self.z = pos1_x, pos1_z
            print("Teleported to spot 1!")
            return True
        return False

    def shoot(self, maze, camera):
        global last_shot_time, muzzle_flash_timer, screen_shake
        
        if not self.has_gun or self.weapon_heat >= self.max_weapon_heat:
            return
            
        # Add weapon heat
        self.weapon_heat = min(self.max_weapon_heat, self.weapon_heat + 15)
        
        rad = math.radians(self.rotation)
        bx = self.x + 0.25 * math.sin(rad)
        bz = self.z + 0.25 * math.cos(rad)
        by = self.y + 1.1
        
        self.bullets.append(Bullet(bx, by, bz, self.rotation))
        
        if DOUBLE_BULLET:
            self.bullets.append(Bullet(bx + 0.15 * math.cos(rad), by, bz - 0.15 * math.sin(rad), self.rotation))
            
        # Visual effects
        muzzle_flash_timer = 0.1
        screen_shake = 3
        last_shot_time = time_counter

    def update_bullets(self, maze):
        global bullets_missed, combo_count, combo_multiplier, enemy_kills, kill_times, power_ups, particle_effects, wave_number, aliens_killed_this_wave, game_difficulty
        
        # Cool down weapon
        if self.weapon_heat > 0:
            self.weapon_heat = max(0, self.weapon_heat - 0.5)
            
        new_bullets = []
        for bullet in self.bullets:
            old_x, old_z = bullet.x, bullet.z
            bullet.move()
            new_x, new_z = bullet.x, bullet.z
            hit_wall = False
            steps = int(math.ceil(max(abs(new_x - old_x), abs(new_z - old_z)) / 0.05)) or 1
            for i in range(steps + 1):
                t = i / steps
                x = old_x + t * (new_x - old_x)
                z = old_z + t * (new_z - old_z)
                grid_x, grid_z = int(x), int(z)
                if 0 <= grid_x < maze.width and 0 <= grid_z < maze.height:
                    if maze.grid[grid_z][grid_x] == 1:
                        hit_wall = True
                        break
                else:
                    bullets_missed += 1
                    combo_count = 0
                    combo_multiplier = 1
                    print(f"Bullets Missed: {bullets_missed}")
                    hit_wall = True
                    break
            if hit_wall:
                continue
                
            hit = False
            for i, alien in enumerate(maze.aliens[:]):
                if math.sqrt((bullet.x - alien.x)**2 + (bullet.z - alien.z)**2) < 0.3:
                    # Damage alien instead of instant kill
                    alien.health -= 1
                    
                    if alien.health <= 0:
                        # Add explosion effect
                        particle_effects.append(ParticleEffect(alien.x, alien.y, alien.z, "explosion"))
                        
                        score_bonus = 10 * combo_multiplier * game_difficulty
                        self.score += score_bonus
                        self.experience += 10 * game_difficulty
                        combo_count += 1
                        
                        if combo_count >= 3:
                            combo_multiplier = min(5, combo_multiplier + 1)
                            
                        self.enemy_kills += 1
                        aliens_killed_this_wave += 1
                        kill_times.append(time_counter)
                        
                        print(f"Alien killed! Score: {self.score}, Kills: {self.enemy_kills}, Wave: {wave_number}")
                        
                        # Wave progression
                        if aliens_killed_this_wave >= 5 + wave_number * 2:
                            wave_number += 1
                            game_difficulty += 0.5
                            aliens_killed_this_wave = 0
                            print(f"Wave {wave_number} begins! Difficulty increased.")
                            
                        if self.enemy_kills % 5 == 0:
                            x, z = maze.get_random_path(maze.coins + [maze.exit_pos, maze.teleport_pos1, maze.teleport_pos2])
                            power_ups.append([x, 0.5, z, "double"])
                            print("Double Bullet Power-Up Spawned!")
                            
                        maze.aliens.pop(i)
                        maze.generate_aliens(1)
                        
                    hit = True
                    break
                    
            if not hit:
                new_bullets.append(bullet)
                
        self.bullets = new_bullets
        kill_times[:] = [t for t in kill_times if time_counter - t <= 10]
        
        if len(kill_times) >= 3:
            self.enemy_kills += 1
            self.score += 50
            kill_times.clear()
            print("Bonus Kill Point Awarded!")

def draw_crosshair():
    """Draw crosshair in center of screen"""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glColor3f(1.0, 0.0, 0.0)
    glLineWidth(2.0)
    
    glBegin(GL_LINES)
    # Horizontal line
    glVertex2f(390, 300)
    glVertex2f(410, 300)
    # Vertical line
    glVertex2f(400, 290)
    glVertex2f(400, 310)
    glEnd()
    
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_minimap(maze, human):
    """Draw minimap in corner - adjusted position to avoid scoreboard"""
    if not maze.mini_map_enabled:
        return
        
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    
    # Move minimap to top right, away from scoreboard
    glColor4f(0.0, 0.0, 0.0, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(650, 470)
    glVertex2f(780, 470)
    glVertex2f(780, 590)
    glVertex2f(650, 590)
    glEnd()
    
    # Draw maze walls
    scale = 120.0 / max(maze.width, maze.height)
    offset_x, offset_y = 650, 470
    
    glColor3f(0.0, 0.0, 1.0)
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x] == 1:
                px, py = offset_x + x * scale, offset_y + y * scale
                glBegin(GL_QUADS)
                glVertex2f(px, py)
                glVertex2f(px + scale, py)
                glVertex2f(px + scale, py + scale)
                glVertex2f(px, py + scale)
                glEnd()
    
    # Draw player
    px = offset_x + human.x * scale
    py = offset_y + human.z * scale
    glColor3f(0.0, 1.0, 0.0)
    glPointSize(6.0)
    glBegin(GL_POINTS)
    glVertex2f(px, py)
    glEnd()
    
    # Draw enemies
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(4.0)
    glBegin(GL_POINTS)
    for alien in maze.aliens:
        ax = offset_x + alien.x * scale
        ay = offset_y + alien.z * scale
        glVertex2f(ax, ay)
    glEnd()
    
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_hud(human):
    """Draw enhanced HUD"""
    global sprint_stamina, wave_number, game_difficulty
    
    # Health bar
    glColor3f(1.0, 0.0, 0.0)
    health_ratio = human.lives / human.max_lives
    health_text = f"Health: {int(human.lives)}/{int(human.max_lives)}"
    draw_text(10, 580, health_text, 1.0, 0.0, 0.0)
    
    # Health bar visual
    glWindowPos2i(10, 560)
    for i in range(int(human.max_lives)):
        if i < int(human.lives):
            draw_text(10 + i * 20, 560, "♥", 1.0, 0.0, 0.0)
        else:
            draw_text(10 + i * 20, 560, "♡", 0.3, 0.0, 0.0)
    
    # Shield bar
    shield_ratio = human.shield_energy / human.max_shield
    shield_text = f"Shield: {int(human.shield_energy)}"
    draw_text(10, 540, shield_text, 0.0, 0.5, 1.0)
    
    # Sprint stamina
    stamina_text = f"Stamina: {int(sprint_stamina)}"
    draw_text(10, 520, stamina_text, 0.0, 1.0, 0.0)
    
    # Weapon heat
    heat_ratio = human.weapon_heat / human.max_weapon_heat
    heat_text = f"Heat: {int(human.weapon_heat)}"
    color = (1.0, 1.0 - heat_ratio, 0.0)
    draw_text(10, 500, heat_text, *color)
    
    # Score and stats
    status = f"Score: {human.score} | Level: {human.level} | XP: {human.experience}"
    draw_text(10, 70, status, 1.0, 1.0, 1.0)
    
    wave_text = f"Wave: {wave_number} | Difficulty: {game_difficulty:.1f}"
    draw_text(10, 50, wave_text, 1.0, 0.8, 0.0)
    
    stats = f"Coins: {human.coin_count} | Kills: {human.enemy_kills}/15"
    draw_text(10, 30, stats, 1.0, 1.0, 1.0)
    
    if human.has_gun:
        draw_text(10, 10, "Weapon: Plasma Rifle", 0.8, 0.8, 0.8)
    
    # Controls hint - simplified
    draw_text(600, 30, "WASD: Move, Mouse: Look", 0.6, 0.6, 0.8)
    
    if DOUBLE_BULLET:
        remaining = max(0, DOUBLE_BULLET + 10 - time_counter)
        draw_text(400, 550, f"Double Bullet: {remaining:.1f}s", 1.0, 0.0, 0.0)
    
    if combo_multiplier > 1:
        draw_text(400, 520, f"Combo: x{combo_multiplier}", 1.0, 1.0, 0.0)

def draw_permanent_scoreboard(human):
    """Draw permanent scoreboard on screen with text"""
    # Set up 2D rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    
    # Scoreboard background
    glColor4f(0.0, 0.0, 0.0, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(580, 10)
    glVertex2f(790, 10)
    glVertex2f(790, 140)
    glVertex2f(580, 140)
    glEnd()
    
    # Border
    glLineWidth(2.0)
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(580, 10)
    glVertex2f(790, 10)
    glVertex2f(790, 140)
    glVertex2f(580, 140)
    glEnd()
    
    # Display current game stats with text
    draw_text(590, 120, "GAME STATUS", 1.0, 1.0, 0.0)
    
    # Score
    draw_text(590, 105, f"Score: {human.score}", 0.0, 1.0, 0.0)
    
    # Lives
    draw_text(590, 90, f"Lives: {int(human.lives)}/{int(human.max_lives)}", 1.0, 0.0, 0.0)
    
    # Level
    draw_text(590, 75, f"Level: {human.level}", 0.0, 0.5, 1.0)
    
    # Wave
    draw_text(590, 60, f"Wave: {wave_number}", 1.0, 0.5, 0.0)
    
    # Experience
    draw_text(590, 45, f"XP: {human.experience}", 0.5, 1.0, 0.5)
    
    # Kills
    draw_text(590, 30, f"Kills: {human.enemy_kills}/15", 1.0, 0.0, 0.5)
    
    # Coins
    draw_text(590, 15, f"Coins: {human.coin_count}", 1.0, 1.0, 0.0)
    
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_ambient_objects(maze):
    """Draw decorative objects"""
    for obj in maze.ambient_objects:
        glPushMatrix()
        glTranslatef(obj['x'], 0.3, obj['z'])
        glRotatef(obj['rotation'], 0, 1, 0)
        
        if obj['type'] == "crystal":
            glColor3f(0.5, 0.8, 1.0)
            glScalef(0.3, 0.8, 0.3)
            glutSolidOctahedron()
        elif obj['type'] == "pillar":
            glColor3f(0.4, 0.4, 0.4)
            gluCylinder(gluNewQuadric(), 0.15, 0.15, 0.8, 8, 8)
        elif obj['type'] == "debris":
            glColor3f(0.3, 0.3, 0.3)
            glScalef(0.4, 0.2, 0.4)
            glutSolidCube(1.0)
            
        glPopMatrix()

keys_pressed = {
    b'w': False, b's': False, b'a': False, b'd': False,
    b'f': False, b't': False, b'r': False, b'p': False
}
maze = None
camera = None
human = None

def draw_space_environment():
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    for _ in range(1000):
        x = random.uniform(-50, 50)
        y = random.uniform(-50, 50)
        z = random.uniform(-50, 50)
        glVertex3f(x, y, z)
    glEnd()
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(20, 10, 20)
    glColor3f(1.0, 0.3, 0.3)
    glutSolidSphere(5.0, 20, 20)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-15, 8, -25)
    glColor3f(0.3, 0.3, 1.0)
    glutSolidSphere(4.0, 20, 20)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 12, -30)
    glColor3f(1.0, 0.8, 0.4)
    glutSolidSphere(3.0, 20, 20)
    glPushMatrix()
    glRotatef(30, 1, 0, 0)
    glColor4f(0.8, 0.8, 0.8, 0.5)
    glBegin(GL_QUAD_STRIP)
    for i in range(36):
        angle = math.radians(i * 10)
        inner = 4.0
        outer = 6.0
        glVertex3f(inner * math.cos(angle), 0, inner * math.sin(angle))
        glVertex3f(outer * math.cos(angle), 0, outer * math.sin(angle))
    glEnd()
    glPopMatrix()
    glPopMatrix()

def draw_power_up(x, y, z, type):
    glPushMatrix()
    glTranslatef(x, y, z + 0.1 * math.sin(time_counter * 2))
    glRotatef(time_counter * 100, 0, 0, 1)
    glow = 0.8 + 0.2 * math.sin(time_counter * 3)
    if type == "double":
        glColor3f(glow, 0, 0)
    glutSolidCube(0.4)
    glPopMatrix()

def draw_maze():
    global screen_shake, screen_shake_duration
    
    if screen_shake_duration > 0:
        glTranslatef(
            random.uniform(-screen_shake, screen_shake),
            random.uniform(-screen_shake, screen_shake),
            0
        )
        screen_shake_duration -= 16
        if screen_shake_duration <= 0:
            screen_shake = 0
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera.apply(human)
    draw_space_environment()
    
    glBegin(GL_QUADS)
    glColor3f(0.7, 0.7, 0.7)
    glVertex3f(0, 0, 0)
    glVertex3f(maze.width, 0, 0)
    glVertex3f(maze.width, 0, maze.height)
    glVertex3f(0, 0, maze.height)
    glEnd()
    
    glBegin(GL_QUADS)
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x] == 1:
                base_color = 0.2 + 0.3 * math.sin((x + y) * 0.5)
                glColor3f(0.0, 0.0, base_color)
                
                # Front face
                glVertex3f(x, 0, y)
                glVertex3f(x + 1, 0, y)
                glVertex3f(x + 1, 1, y)
                glVertex3f(x, 1, y)
                
                # Back face
                glVertex3f(x, 0, y + 1)
                glVertex3f(x + 1, 0, y + 1)
                glVertex3f(x + 1, 1, y + 1)
                glVertex3f(x, 1, y + 1)
                
                # Left face
                glVertex3f(x, 0, y)
                glVertex3f(x, 0, y + 1)
                glVertex3f(x, 1, y + 1)
                glVertex3f(x, 1, y)
                
                # Right face
                glVertex3f(x + 1, 0, y)
                glVertex3f(x + 1, 0, y + 1)
                glVertex3f(x + 1, 1, y + 1)
                glVertex3f(x + 1, 1, y)
                
                # Top face
                glVertex3f(x, 1, y)
                glVertex3f(x + 1, 1, y)
                glVertex3f(x + 1, 1, y + 1)
                glVertex3f(x, 1, y + 1)
    glEnd()
    
    # Draw ambient decorative objects
    draw_ambient_objects(maze)
    
    # Draw coins with enhanced visuals
    for x, z in maze.coins:
        glPushMatrix()
        glTranslatef(x, 0.5 + 0.1 * math.sin(time_counter * 0.1), z)
        glRotatef(time_counter * 2, 0, 1, 0)
        glColor3f(1.0, 0.8, 0.0)
        glutSolidSphere(0.2, 12, 12)
        glPopMatrix()
    
    # Draw exit portal
    exit_x, exit_z = maze.exit_pos
    glPushMatrix()
    glTranslatef(exit_x, 0.1, exit_z)
    glRotatef(time_counter, 0, 1, 0)
    glColor3f(0.0, 1.0, 0.2)
    glutSolidCube(0.8)
    glPopMatrix()
    
    # Draw teleporters with pulsing effect
    pulse = 0.5 + 0.3 * math.sin(time_counter * 0.05)
    for x, z in [maze.teleport_pos1, maze.teleport_pos2]:
        glPushMatrix()
        glTranslatef(x, 0.1, z)
        glColor3f(pulse, 0.0, 1.0)
        glutSolidCube(0.6)
        glPopMatrix()
    
    # Draw game entities
    for alien in maze.aliens:
        alien.draw(time_counter)
    
    for bullet in human.bullets:
        bullet.draw()
    
    for power_up in power_ups:
        draw_power_up(*power_up[:3], power_up[3])
    
    # Draw particle effects
    for effect in particle_effects:
        effect.update(16)
        effect.draw()
    
    human.draw(time_counter, camera.top_down)
    
    # Draw UI elements
    draw_hud(human)
    draw_permanent_scoreboard(human)
    draw_minimap(maze, human)
    
    if not camera.top_down:
        draw_crosshair()
    
    if human.game_over:
        draw_text(300, 400, "Game Over! Press 'r' to reset or Esc to quit.", 1.0, 0.0, 0.0)
        draw_text(350, 370, f"Final Score: {human.score}", 1.0, 0.0, 0.0)
        
        if is_high_score(human.score):
            draw_text(280, 340, "NEW HIGH SCORE! Well done!", 1.0, 1.0, 0.0)
            if not hasattr(human, 'score_saved'):
                add_high_score(player_name, human.score, human.level, wave_number)
                human.score_saved = True
                
    elif human.game_won:
        draw_text(300, 400, "Game Cleared! Press 'r' to reset or Esc to quit.", 0.0, 1.0, 0.0)
        draw_text(350, 370, f"Final Score: {human.score}", 0.0, 1.0, 0.0)
        
        if is_high_score(human.score):
            draw_text(280, 340, "NEW HIGH SCORE! Excellent!", 1.0, 1.0, 0.0)
            if not hasattr(human, 'score_saved'):
                add_high_score(player_name, human.score, human.level, wave_number)
                human.score_saved = True
    
    glutSwapBuffers()


def keyboard(key, x, y):
    global maze, human, camera, time_counter, bullets_missed, combo_count, combo_multiplier, DOUBLE_BULLET, power_ups, last_mouse_x, mouse_deltas, kill_times, is_moving, show_scoreboard, is_sprinting
    
    if key == b'\x1b':
        sys.exit()
    elif key == b'r':
        show_scoreboard = False
        maze = Maze(11, 11)
        human = Human(maze)
        camera = Camera()
        time_counter = 0
        bullets_missed = 0
        combo_count = 0
        combo_multiplier = 1
        DOUBLE_BULLET = False
        power_ups = []
        kill_times = []
        last_mouse_x = 400
        mouse_deltas = []
        is_moving = False
        glutSetCursor(GLUT_CURSOR_INHERIT)
        glutPostRedisplay()
    elif key == b'f' and not human.game_over and not human.game_won and not show_scoreboard:
        camera.toggle_top_down()
        glutPostRedisplay()
    elif key == b't' and not human.game_over and not human.game_won and not show_scoreboard:
        human.try_teleport(maze)
        glutPostRedisplay()
    elif key == b'm' and not human.game_over and not human.game_won and not show_scoreboard:
        maze.mini_map_enabled = not maze.mini_map_enabled
        glutPostRedisplay()
    
    if not human.game_over and not human.game_won and not show_scoreboard:
        if key == b'w':
            human.move(0, 1, maze)
            is_moving = True
        elif key == b's':
            human.move(0, -1, maze)
            is_moving = True
        elif key == b'a':
            human.move(1, 0, maze)
            is_moving = True
        elif key == b'd':
            human.move(-1, 0, maze)
            is_moving = True
        glutPostRedisplay()

def keyboard_up(key, x, y):
    global is_moving
    if key in (b'w', b's', b'a', b'd'):
        is_moving = False
        glutPostRedisplay()

def mouse(button, state, x, y):
    global show_scoreboard
    if human.game_over or human.game_won or show_scoreboard:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and human.has_gun:
        human.shoot(maze, camera)
        glutPostRedisplay()

def motionListener(x, y):
    global last_mouse_x, mouse_deltas, show_scoreboard
    if human.game_over or human.game_won or show_scoreboard:
        return
    dx = x - last_mouse_x
    mouse_deltas.append(dx)
    if len(mouse_deltas) > 3:
        mouse_deltas.pop(0)
    avg_dx = sum(mouse_deltas) / len(mouse_deltas)
    rotation = max(-10, min(10, -avg_dx * 0.6))
    human.rotate_player(rotation)
    last_mouse_x = x
    glutPostRedisplay()

def update(value):
    global time_counter, DOUBLE_BULLET, human, particle_effects, muzzle_flash_timer
    
    if human.game_over or human.game_won:
        glutPostRedisplay()
        glutTimerFunc(16, update, 0)
        return
    
    dt = 16  # Frame time in milliseconds
    time_counter += 0.02
    
    # Update visual timers
    if muzzle_flash_timer > 0:
        muzzle_flash_timer -= dt / 1000.0
        
    # Update power-up timers
    if DOUBLE_BULLET and time_counter > DOUBLE_BULLET + 10:
        DOUBLE_BULLET = False
    
    # Update weapon heat
    if human.weapon_heat > 0:
        human.weapon_heat -= 30 * (dt / 1000.0)
        human.weapon_heat = max(0, human.weapon_heat)
    
    # Update shield regeneration
    if human.shield_energy < human.max_shield:
        human.shield_energy += 5 * (dt / 1000.0)
        human.shield_energy = min(human.max_shield, human.shield_energy)
    
    # Update aliens
    for alien in maze.aliens:
        alien.move(maze, human)
    
    # Update human systems
    human.check_collisions(maze, time_counter)
    human.update_bullets(maze)
    
    # Update particle effects
    for effect in particle_effects[:]:
        effect.update(dt)
        if effect.is_dead():
            particle_effects.remove(effect)
    
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def main():
    global maze, camera, human
    
    # Initialize scoreboard system
    load_high_scores()
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"3D Maze Alien Shooter - Enhanced")
    glClearColor(0.0, 0.0, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(90, 800/600, 0.1, 800)
    glMatrixMode(GL_MODELVIEW)
    maze = Maze(11, 11)
    camera = Camera()
    human = Human(maze)
    glutDisplayFunc(draw_maze)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutMouseFunc(mouse)
    glutPassiveMotionFunc(motionListener)
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()