import pygame
import random
import math
import os

pygame.init()

# Set up screen
screen = pygame.display.set_mode((1280, 1080))
clock = pygame.time.Clock()
running = True

# Get the current script's directory
current_dir = os.path.dirname(__file__)

# Load images with transparency
rat_image_path = os.path.join(current_dir, "Rat-isolated-on-transparent-background-PNG.png")
cheese_image_path = os.path.join(current_dir, "Piece-of-swiss-cheese-isolated-on-transparent-background-PNG.png")
buff_rat_image_path = os.path.join(current_dir, "buff_rat_image.png")

rat_image = pygame.image.load(rat_image_path).convert_alpha()
cheese_image = pygame.image.load(cheese_image_path).convert_alpha()
buff_rat_image = pygame.image.load(buff_rat_image_path).convert_alpha()

# Set image dimensions
image_width = 100
image_height = 100
xpos, ypos = 1280 / 2, 1080 / 2
rat_image = pygame.transform.scale(rat_image, (image_width, image_height))
cheese_image = pygame.transform.scale(cheese_image, (image_width, image_height))
buff_rat_image = pygame.transform.scale(buff_rat_image, (image_width, image_height))

# Set other variables
hitbox_offset = 10
rat_speed = 5
enemy_rat_min_distance = 25  # Minimum distance between enemy rats
min_player_distance = 500  # Minimum distance between player and enemy rats

# Load sound effect
pickup_sound_path = os.path.join(current_dir, "retro-video-game-coin-pickup-38299.mp3")
pygame.mixer.init()
pickup_sound = pygame.mixer.Sound(pickup_sound_path)
death_sound =  pygame.mixer.Sound(os.path.join(current_dir, "mixkit-sad-game-over-trombone-471.wav"))

def generate_new_cheese_position():
    while True:
        new_x = random.randint(0, 1280 - image_width)
        new_y = random.randint(0, 1080 - image_height)
        if math.sqrt((new_x - xpos) ** 2 + (new_y - ypos) ** 2) > 200:
            return new_x, new_y

def draw_game_over_screen(score, high_score):
    screen.fill((255, 255, 255))
    pygame.font.init()
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (480, 300))

    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (550, 400))

    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(high_score_text, (520, 450))

    restart_text = font.render("Press 'R' to restart", True, (0, 0, 0))
    screen.blit(restart_text, (520, 500))

    pygame.display.flip()

def reset_game():
    global xpos, ypos, cheese_x, cheese_y, enemy_rat_list, score, enemy_rat_spawn_time
    xpos, ypos = 1280 / 2, 1080 / 2
    cheese_x, cheese_y = generate_new_cheese_position()
    enemy_rat_list = []
    score = 0
    # Set enemy_rat_spawn_time to a value higher than the initial time
    enemy_rat_spawn_time = pygame.time.get_ticks()   # Reset spawn time (initially set to 30 seconds)

cheese_x, cheese_y = generate_new_cheese_position()

# Set enemy_rat_spawn_time to a value higher than the initial time
enemy_rat_spawn_time = pygame.time.get_ticks()  # Initial spawn time after 30 seconds
enemy_rat_list = []  # List to store enemy rats

def draw_game_over_screen(score, high_score):
    screen.fill((255, 255, 255))
    pygame.font.init()
    font = pygame.font.SysFont(None, 72)
    
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (480, 300))
    
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (550, 400))

    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(high_score_text, (520, 450))

    restart_text = font.render("Press 'R' to restart", True, (0, 0, 0))
    screen.blit(restart_text, (520, 500))

    pygame.display.flip()

    pygame.time.delay(2000)  # Add a delay to display the Game Over screen for 2000 milliseconds (2 seconds)

score = 0
high_score = 0
game_state = "playing"  # "playing" or "game_over"
game_over_time = 0

score_box = pygame.Rect(0, 0, 1280, 40)

class EnemyRat:
    def __init__(self):
        self.x = random.randint(0, 1280 - image_width)
        self.y = random.randint(0, 1080 - image_height)
        self.speed_percentage = 25  # Starting speed at 25% of player speed

    def move_towards_player(self):
        angle = math.atan2(ypos - self.y, xpos - self.x)
        self.x += (rat_speed * (self.speed_percentage / 100)) * math.cos(angle)
        self.y += (rat_speed * (self.speed_percentage / 100)) * math.sin(angle)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_state == "game_over":
                reset_game()
                game_state = "playing"

    keys = pygame.key.get_pressed()
    
    if game_state == "playing":
        if keys[pygame.K_LEFT] or keys[ord('a')]:
            xpos -= rat_speed
            if xpos < 0:
                xpos = 0
        if keys[pygame.K_RIGHT] or keys[ord('d')]:
            xpos += rat_speed
            if xpos > 1280 - image_width:
                xpos = 1280 - image_width
        if keys[pygame.K_UP] or keys[ord('w')]:
            ypos -= rat_speed
            if ypos < 40:
                ypos = 40
        if keys[pygame.K_DOWN] or keys[ord('s')]:
            ypos += rat_speed
            if ypos > 1080 - image_height:
                ypos = 1080 - image_height

        # Check if it's time to spawn a new enemy rat
        current_time = pygame.time.get_ticks()
        if current_time >= enemy_rat_spawn_time:
            enemy_rat_spawn_time = current_time + 7500  # Spawn a new enemy rat every 15 seconds
            new_enemy_rat = EnemyRat()
            
            # Increase the speed of the new rat compared to the last rat
            if enemy_rat_list:
                new_enemy_rat.speed_percentage = min(100, enemy_rat_list[-1].speed_percentage + 5)

            # Ensure new enemy rat maintains a minimum distance from other enemy rats
            too_close = any(math.sqrt((new_enemy_rat.x - other.x) ** 2 +
                                      (new_enemy_rat.y - other.y) ** 2) < enemy_rat_min_distance
                            for other in enemy_rat_list)

            # Ensure new enemy rat spawns at least 500 pixels away from the player
            player_distance = math.sqrt((new_enemy_rat.x - xpos) ** 2 + (new_enemy_rat.y - ypos) ** 2)
            
            if not too_close and player_distance > min_player_distance:
                enemy_rat_list.append(new_enemy_rat)

        cheese_hitbox = pygame.Rect(cheese_x + hitbox_offset, cheese_y + hitbox_offset,
                                    image_width - 2 * hitbox_offset, image_height - 2 * hitbox_offset)
        rat_hitbox = pygame.Rect(xpos, ypos, image_width, image_height)

        for enemy_rat in enemy_rat_list:
            enemy_rat_hitbox = pygame.Rect(enemy_rat.x, enemy_rat.y, image_width, image_height)
            if rat_hitbox.colliderect(enemy_rat_hitbox):
                # Handle collision with enemy rat (You can modify this part according to your game logic)
                death_sound.play()
                game_state = "game_over"
                game_over_time = pygame.time.get_ticks()
                if score > high_score:
                    high_score = score

                draw_game_over_screen(score, high_score)

                # Reset the game when 'R' is pressed
                reset_game()

                continue

            # Move the enemy rat towards the player at its individual speed
            enemy_rat.move_towards_player()

        if rat_hitbox.colliderect(cheese_hitbox):
            cheese_x, cheese_y = generate_new_cheese_position()
            score += 1
            # Play the sound effect on cheese collection
            pickup_sound.play()

    elif game_state == "game_over":
        draw_game_over_screen(score, high_score)

    screen.fill((255, 255, 255))

    if game_state == "playing":
        # Draw the score box
        pygame.draw.rect(screen, (0, 0, 0), score_box)
        pygame.font.init()
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        screen.blit(rat_image, (xpos, ypos))
        screen.blit(cheese_image, (cheese_x, cheese_y))

        for enemy_rat in enemy_rat_list:
            screen.blit(buff_rat_image, (enemy_rat.x, enemy_rat.y))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()