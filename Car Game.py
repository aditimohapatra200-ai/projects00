import pygame
import random
import os

# --- Initialization ---
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Road Settings
ROAD_WIDTH = 400 # Narrower road
ROAD_X = (SCREEN_WIDTH - ROAD_WIDTH) // 2
LANE_WIDTH = ROAD_WIDTH // 3

GRASS_COLOR = (34, 139, 34)    # Forest Green
ROAD_COLOR = (50, 50, 50)      # Dark Asphalt
LINE_COLOR = (255, 255, 255)   # White

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 90
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 90
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
GRAY = (100, 100, 100)

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Realistic 3-Lane Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30, bold=True)
large_font = pygame.font.SysFont("Arial", 60, bold=True)

# --- High Score Functions ---
HIGHSCORE_FILE = "highscore.txt"

def get_high_score():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(new_score):
    current_high = get_high_score()
    if new_score > current_high:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(new_score))
        return True
    return False

# --- Game Variables ---
lane_centers = [
    ROAD_X + LANE_WIDTH // 2,
    ROAD_X + LANE_WIDTH + LANE_WIDTH // 2,
    ROAD_X + (LANE_WIDTH * 2) + LANE_WIDTH // 2
]

def reset_game():
    return {
        'player_lane': 1,
        'score': 0,
        'speed': 5,
        'obstacles': [],
        'game_over': False,
        'road_offset': 0 # For animation
    }

game_state = reset_game()
high_score = get_high_score()

# --- Drawing Functions ---

def draw_road():
    # 1. Draw Grass (Background)
    screen.fill(GRASS_COLOR)
    
    # Add some grass details (lighter patches)
    for _ in range(20):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        pygame.draw.circle(screen, (40, 160, 40), (x, y), random.randint(5, 15))

    # 2. Draw Main Road
    pygame.draw.rect(screen, ROAD_COLOR, (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    
    # 3. Draw Road Borders (Kerbs)
    # Red and White kerbs
    kerb_height = 40
    num_kerbs = SCREEN_HEIGHT // kerb_height + 2
    
    offset = game_state['road_offset'] % (kerb_height * 2)
    
    for i in range(num_kerbs):
        y = i * kerb_height - offset
        color = RED if i % 2 == 0 else WHITE
        
        # Left Kerb
        pygame.draw.rect(screen, color, (ROAD_X - 10, y, 10, kerb_height))
        # Right Kerb
        pygame.draw.rect(screen, color, (ROAD_X + ROAD_WIDTH, y, 10, kerb_height))

    # 4. Draw Lane Lines (Dashed)
    line_width = 5
    line_length = 40
    gap_length = 40
    
    offset = game_state['road_offset'] % (line_length + gap_length)
    
    # Lane 1 Divider
    for y in range(-line_length, SCREEN_HEIGHT, line_length + gap_length):
        pygame.draw.line(screen, LINE_COLOR, (ROAD_X + LANE_WIDTH, y + offset), (ROAD_X + LANE_WIDTH, y + offset + line_length), line_width)
        
    # Lane 2 Divider
    for y in range(-line_length, SCREEN_HEIGHT, line_length + gap_length):
        pygame.draw.line(screen, LINE_COLOR, (ROAD_X + LANE_WIDTH * 2, y + offset), (ROAD_X + LANE_WIDTH * 2, y + offset + line_length), line_width)

def draw_realistic_car(x, y, color, is_player=True):
    # Shadow
    s = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(s, (0,0,0, 100), (5, 5, PLAYER_WIDTH, PLAYER_HEIGHT), border_radius=10)
    screen.blit(s, (x, y))
    
    # Car Body
    pygame.draw.rect(screen, color, (x, y, PLAYER_WIDTH, PLAYER_HEIGHT), border_radius=10)
    
    # Hood/Trunk shading (darker bottom part)
    pygame.draw.rect(screen, (0, 0, 0, 50), (x, y + 60, PLAYER_WIDTH, 30), border_radius=10)

    # Windshield
    pygame.draw.rect(screen, (50, 50, 50), (x + 5, y + 20, PLAYER_WIDTH - 10, 15), border_radius=3)
    
    # Rear Window
    pygame.draw.rect(screen, (50, 50, 50), (x + 5, y + 55, PLAYER_WIDTH - 10, 10), border_radius=3)

    # Headlights (if player) or Tail lights (if obstacle)
    if is_player:
        # Headlights (Yellow/White)
        pygame.draw.rect(screen, (255, 255, 200), (x + 3, y + 2, 10, 5), border_radius=2)
        pygame.draw.rect(screen, (255, 255, 200), (x + PLAYER_WIDTH - 13, y + 2, 10, 5), border_radius=2)
    else:
        # Tail lights (Red)
        pygame.draw.rect(screen, (255, 0, 0), (x + 3, y + PLAYER_HEIGHT - 7, 10, 5), border_radius=2)
        pygame.draw.rect(screen, (255, 0, 0), (x + PLAYER_WIDTH - 13, y + PLAYER_HEIGHT - 7, 10, 5), border_radius=2)

def draw_obstacles(obstacles):
    for obs in obstacles:
        x = lane_centers[obs['lane']] - OBSTACLE_WIDTH // 2
        y = obs['y']
        
        # Draw car facing the same way (so we see tail lights)
        # Random colors for enemy cars
        car_color = random.choice([(200, 50, 50), (50, 200, 50), (200, 200, 50), (100, 100, 200)])
        
        draw_realistic_car(x, y, car_color, is_player=False)

def draw_text(text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

# --- Main Game Loop ---
running = True

while running:
    clock.tick(FPS)
    
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if not game_state['game_over']:
                if event.key == pygame.K_LEFT and game_state['player_lane'] > 0:
                    game_state['player_lane'] -= 1
                elif event.key == pygame.K_RIGHT and game_state['player_lane'] < 2:
                    game_state['player_lane'] += 1
            else:
                if event.key == pygame.K_SPACE:
                    game_state = reset_game()
                    high_score = get_high_score()

    # 2. Game Logic
    if not game_state['game_over']:
        # Animate Road
        game_state['road_offset'] += game_state['speed']
        
        # Spawn Obstacles
        if random.randint(0, 100) < 2: 
            lane = random.randint(0, 2)
            can_spawn = True
            for obs in game_state['obstacles']:
                if obs['lane'] == lane and obs['y'] < 150:
                    can_spawn = False
            
            if can_spawn:
                game_state['obstacles'].append({'lane': lane, 'y': -OBSTACLE_HEIGHT})

        # Move Obstacles
        for obs in game_state['obstacles']:
            obs['y'] += game_state['speed']

        # Remove off-screen obstacles
        game_state['obstacles'] = [obs for obs in game_state['obstacles'] if obs['y'] < SCREEN_HEIGHT]
        game_state['score'] += 1 
        
        # Increase difficulty
        if game_state['score'] % 500 == 0 and game_state['speed'] < 15:
            game_state['speed'] += 0.5

        # Collision Detection
        player_rect = pygame.Rect(
            lane_centers[game_state['player_lane']] - PLAYER_WIDTH // 2 + 5, # slight hitbox adjustment
            SCREEN_HEIGHT - PLAYER_HEIGHT - 20 + 5,
            PLAYER_WIDTH - 10, 
            PLAYER_HEIGHT - 10
        )
        
        for obs in game_state['obstacles']:
            obs_rect = pygame.Rect(
                lane_centers[obs['lane']] - OBSTACLE_WIDTH // 2 + 5,
                obs['y'] + 5,
                OBSTACLE_WIDTH - 10,
                OBSTACLE_HEIGHT - 10
            )
            
            if player_rect.colliderect(obs_rect):
                game_state['game_over'] = True
                save_high_score(game_state['score'])

    # 3. Drawing
    draw_road()+
    draw_obstacles(game_state['obstacles'])
    
    # Draw Player (Blue Car)
    player_x = lane_centers[game_state['player_lane']] - PLAYER_WIDTH // 2
    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
    draw_realistic_car(player_x, player_y, BLUE, is_player=True)

    # UI
    draw_text(f"Score: {game_state['score']}", font, WHITE, 10, 10)
    draw_text(f"High Score: {high_score}", font, YELLOW, 10, 50)

    if game_state['game_over']:
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(150)
        s.fill(BLACK)
        screen.blit(s, (0,0))
        
        draw_text("GAME OVER", large_font, RED, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50, center=True)
        draw_text(f"Final Score: {game_state['score']}", font, WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10, center=True)
        draw_text("Press SPACE to Restart", font, YELLOW, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60, center=True)

    pygame.display.update()

pygame.quit()
