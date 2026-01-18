
import random
import pygame

WIDTH, HEIGHT = 900, 600
NUM_DOTS = 30
DOT_RADIUS = 4
MAX_SPEED = 180
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
    #- Then multiply it by a random speed (between ~30% and 100% of max_speed).
    
    v = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
    # Edge Case if = 0
    if v.length_squared() == 0:
        v = pygame.Vector2(1, 0)
     # Not all dots move at the same speed
    v = v.normalize() * random.uniform(max_speed * 0.3, max_speed)
    return v

def clamp_length(v: pygame.Vector2, max_len: float) -> pygame.Vector2:
    if v.length_squared() > max_len * max_len:
        return v.normalize() * max_len
    return v

def steer_towards(current_vel: pygame.Vector2, desired_vel: pygame.Vector2, max_force: float) -> pygame.Vector2:
    # Steering
    steer = desired_vel - current_vel
    return clamp_length(steer, max_force)

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
        for d in dots:
            d["pos"] += d["vel"] * dt
            bounce_off_walls(d["pos"], d["vel"], WIDTH, HEIGHT, DOT_RADIUS)
 

            

        if d["pos"].x <= DOT_RADIUS:
            d["pos"].x = DOT_RADIUS
            d["vel"].x *= -1  
        elif d["pos"].x >= WIDTH - DOT_RADIUS:
            d["pos"].x = WIDTH - DOT_RADIUS
            d["vel"].x *= -1  

        if d["pos"].y <= DOT_RADIUS:
            d["pos"].y = DOT_RADIUS
            d["vel"].y *= -1  
        elif d["pos"].y >= HEIGHT - DOT_RADIUS:
            d["pos"].y = HEIGHT - DOT_RADIUS
            d["vel"].y *= -1  


        # Render game
        screen.fill(BG)
        # Draw dots
        for d in dots:
            pygame.draw.circle(screen, DOT, (int(d["pos"].x), int(d["pos"].y)), DOT_RADIUS)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
