
import random
import pygame

WIDTH, HEIGHT = 900, 600
NUM_DOTS = 30
DOT_RADIUS = 4
MAX_SPEED = 200
VISION_RADIUS = 70
SEPARATION_RADIUS = 25

W_COH = 0.8
W_ALI = 1.0
W_SEP = 1.4

MAX_FORCE = 120  # steering strength limit


BG = (15, 15, 20)
DOT = (220, 220, 235)

def random_velocity(max_speed: float) -> pygame.Vector2:
     
    #Create a random 2D velocity vector (direction + magnitude).
    #- We start with a random direction.
    #- Then normalize it to length 1 (unit vector).
    #- Then multiply it by a random speed (between ~50% and 100% of max_speed).
    
    v = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
    # Edge Case if = 0
    if v.length_squared() == 0:
        v = pygame.Vector2(1, 0)
     # Not all dots move at the same speed
    v = v.normalize() * random.uniform(max_speed * 0.5, max_speed)
    return v

def clamp_length(v: pygame.Vector2, max_len: float) -> pygame.Vector2:
    if v.length_squared() > max_len * max_len:
        return v.normalize() * max_len
    return v

def steer_towards(current_vel: pygame.Vector2, desired_vel: pygame.Vector2, max_force: float) -> pygame.Vector2:
    # Steering
    steer = desired_vel - current_vel
    return clamp_length(steer, max_force)

def boids_acceleration(i: int, dots: list) -> pygame.Vector2:
    me = dots[i]
    pos = me["pos"]
    vel = me["vel"]

    # Accumulators
    align_sum = pygame.Vector2(0, 0)
    cohesion_sum = pygame.Vector2(0, 0)
    separation_sum = pygame.Vector2(0, 0)
    count = 0
    sep_count = 0

    for j, other in enumerate(dots):
        if j == i:
            continue

        offset = other["pos"] - pos
        dist2 = offset.length_squared()
        if dist2 == 0:
            continue

        # Neighbour within vision radius
        if dist2 < VISION_RADIUS * VISION_RADIUS:
            count += 1
            align_sum += other["vel"]
            cohesion_sum += other["pos"]

            
            if dist2 < SEPARATION_RADIUS * SEPARATION_RADIUS:
                sep_count += 1
                separation_sum -= offset / dist2  

    acc = pygame.Vector2(0, 0)
    #Adding Cohesion, Alignment and Separation
    if count > 0:
        # Alignment: match average velocity direction
        avg_vel = align_sum / count
        if avg_vel.length_squared() > 0:
            desired = avg_vel.normalize() * MAX_SPEED
            acc += W_ALI * steer_towards(vel, desired, MAX_FORCE)

        # Cohesion: go toward average position
        center = cohesion_sum / count
        desired_dir = center - pos
        if desired_dir.length_squared() > 0:
            desired = desired_dir.normalize() * MAX_SPEED
            acc += W_COH * steer_towards(vel, desired, MAX_FORCE)

    if sep_count > 0:
        # Separation: steer away from close neighbours
        if separation_sum.length_squared() > 0:
            desired = separation_sum.normalize() * MAX_SPEED
            acc += W_SEP * steer_towards(vel, desired, MAX_FORCE)
            
    return acc


def bounce_off_walls(pos: pygame.Vector2, vel: pygame.Vector2, w: int, h: int, r: int):
    # Left wall
    if pos.x < r:
        pos.x = r
        vel.x = abs(vel.x)          
    # Right wall
    elif pos.x > w - r:
        pos.x = w - r
        vel.x = -abs(vel.x)        

    # Top wall
    if pos.y < r:
        pos.y = r
        vel.y = abs(vel.y)         
    # Bottom wall
    elif pos.y > h - r:
        pos.y = h - r
        vel.y = -abs(vel.y)         

def draw_boid_arrow(screen, pos: pygame.Vector2, vel: pygame.Vector2, color, size=10):
    # If velocity is zero, gives it a default position
    if vel.length_squared() == 0:
        vel = pygame.Vector2(1, 0)

    # Calculates angle to velocity direction
    angle = pygame.Vector2(1, 0).angle_to(vel)  

    # Define triangle points
    local_points = [
        pygame.Vector2(size, 0),        
        pygame.Vector2(-size * 0.6,  size * 0.4),  
        pygame.Vector2(-size * 0.6, -size * 0.4),  
    ]

    # Rotates triangle to face the direction its going
    points = [(pos + p.rotate(angle)) for p in local_points]  

    pygame.draw.polygon(screen, color, points)  


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("30 Moving Dots (Basic Setup)")
    clock = pygame.time.Clock()

    # 'dots' will be a list of dictionaries.
    # Each dictionary stores a dot's position and velocity as 2D vectors.
    dots = []
    for _ in range(NUM_DOTS):
        pos = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        vel = random_velocity(MAX_SPEED)
        #store dots case
        dots.append({"pos": pos, "vel": vel})
    # Main Loop
    running = True
    while running:
        # clock.tick(60) tries to cap the loop at ~60 FPS.
        dt = clock.tick(60) / 1000.0  
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Physics game
        for i, d in enumerate(dots):
            a = boids_acceleration(i, dots)

            # Euler integration
            d["vel"] += a * dt
            d["vel"] = clamp_length(d["vel"], MAX_SPEED)
            d["pos"] += d["vel"] * dt

            bounce_off_walls(d["pos"], d["vel"], WIDTH, HEIGHT, DOT_RADIUS)
 
        # Render game
        screen.fill(BG)
        # Draw arrows
        for d in dots:
            draw_boid_arrow(screen, d["pos"], d["vel"], DOT, size=12)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
