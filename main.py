#AI for Game Programming Unit 3 Lab 1 - Halloween Monster Ambush Solution

import pygame
import random
import sys

# Initialize Pygame
pygame.init()


# --- WINDOW CONFIGURATION ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAB 1 — Halloween Monster Ambush")
clock = pygame.time.Clock()


# --- COLORS ---
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GRAY   = (50, 50, 50)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)


# Location Visual Colors
GRAVEYARD_COLOR = (100, 105, 110)    # Slate Gray
HAUNTED_COLOR   = (75, 0, 130)       # Indigo
FOREST_COLOR    = (34, 139, 34)      # Forest Green
PUMPKIN_COLOR   = (255, 140, 0)      # Dark Orange


# --- GAME DATA & STATES ---
states = ["Graveyard + 10", "Haunted House + 5", "Forest + 8", "Pumpkin Patch + 20"]
rewards = [10, 5, 8, 20]

# Step 2 — Transition Matrix
transition_matrix = [
    [0.10, 0.45, 0.30, 0.15],  # Graveyard
    [0.35, 0.10, 0.40, 0.15],  # Haunted House
    [0.25, 0.35, 0.15, 0.25],  # Forest
    [0.40, 0.20, 0.20, 0.20]   # Pumpkin Patch
]


# Step 3 — Place the monster (Start at Index 2: Forest)
current_state = 2


# Game variables
round_count = 0
max_rounds = 10
human_score = 0
ai_score = 0


# UI Display Text Strings
msg_ambush = "Press 1-4 to predict the monster's next move!"
msg_result = ""
msg_current = f"Current Location: {states[current_state]}"
msg_moved = ""
game_over = False


# --- FONTS ---
font_title = pygame.font.SysFont("Arial", 28, bold=True)
font_body = pygame.font.SysFont("Arial", 22, bold=True)
font_ui = pygame.font.SysFont("Arial", 24)


# --- RECTS FOR STEP 1 (Four Locations Layout) ---
# Upper Left, Upper Right, Lower Left, Lower Right
quad_w, quad_h = WIDTH // 2, HEIGHT // 3
rect_graveyard = pygame.Rect(0, 0, quad_w, quad_h)
rect_haunted   = pygame.Rect(quad_w, 0, quad_w, quad_h)
rect_forest    = pygame.Rect(0, quad_h, quad_w, quad_h)
rect_pumpkin   = pygame.Rect(quad_w, quad_h, quad_w, quad_h)


running = True
while running:
    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
           
        elif event.type == pygame.KEYDOWN and not game_over:
            # Step 4 — Allow the player to choose an ambush (Keys 1 to 4)
            human_prediction = None
            if event.key == pygame.K_1: human_prediction = 0
            elif event.key == pygame.K_2: human_prediction = 1
            elif event.key == pygame.K_3: human_prediction = 2
            elif event.key == pygame.K_4: human_prediction = 3
           
            if human_prediction is not None:
                # --- AI CHALLENGE LOGIC ---
                # AI looks at the current row and picks the highest probability index
                row = transition_matrix[current_state]
                ai_probability = row.index(max(row))

                # AI also gets expected value
                expected = []
                for i in range(4):
                    value = transition_matrix[current_state][i] * rewards[i]
                    expected.append(value)
                ai_best_action = expected.index(max(expected))

                # AI uses random choice
                ai_random = random.randint(0, 3)

                # AI choice
                ai_prediction = ai_probability  # This can be changed

                # Step 5 — Generate the monster's next location
                next_state = random.choices(range(4), weights=row, k=1)[0]
               
                # Step 6 — Compare human prediction with outcome
                if human_prediction == next_state:
                    human_score += 1
                    msg_result = "AMBUSH SUCCESSFUL!"
                else:
                    msg_result = "The monster escaped!"
                   
                # Compare AI prediction with outcome
                if ai_prediction == next_state:
                    ai_score += 1
               
                # Progress Round
                round_count += 1
               
                # Update UI elements for Step 7
                msg_current = f"Current Location: {states[current_state]}"
                msg_ambush = f"Your Ambush: {states[human_prediction]} (AI chose: {states[ai_prediction]})"
                msg_moved = f"Monster Moved To: {states[next_state]}"
               
                # Update current state for the next turn
                current_state = next_state
               
                # Step 8 — Play 10 rounds maximum
                if round_count >= max_rounds:
                    game_over = True


    # --- DRAWING / DISPLAY ---
    screen.fill(BLACK)
   
    # Step 1 — Render Four Locations (Rectangles)
    pygame.draw.rect(screen, GRAVEYARD_COLOR, rect_graveyard)
    pygame.draw.rect(screen, HAUNTED_COLOR, rect_haunted)
    pygame.draw.rect(screen, FOREST_COLOR, rect_forest)
    pygame.draw.rect(screen, PUMPKIN_COLOR, rect_pumpkin)
   
    # Draw Location Grid Divider Lines
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT * 2 // 3), 5)
    pygame.draw.line(screen, BLACK, (0, quad_h), (WIDTH, quad_h), 5)
   
    # Render Location Text Labels
    screen.blit(font_title.render("GRAVEYARD (1)", True, WHITE), (20, 20))
    screen.blit(font_title.render("HAUNTED HOUSE (2)", True, WHITE), (WIDTH // 2 + 20, 20))
    screen.blit(font_title.render("DARK FOREST (3)", True, WHITE), (20, quad_h + 20))
    screen.blit(font_title.render("PUMPKIN PATCH (4)", True, WHITE), (WIDTH // 2 + 20, quad_h + 20))
   
    # Draw Monster Visual Indicator (Red Circle) in its current area
    if current_state == 0:   monster_pos = (quad_w // 2, quad_h // 2)
    elif current_state == 1: monster_pos = (quad_w + quad_w // 2, quad_h // 2)
    elif current_state == 2: monster_pos = (quad_w // 2, quad_h + quad_h // 2)
    elif current_state == 3: monster_pos = (quad_w + quad_w // 2, quad_h + quad_h // 2)
   
    pygame.draw.circle(screen, RED, monster_pos, 25)
    monster_lbl = font_body.render("MONSTER", True, BLACK)
    screen.blit(monster_lbl, (monster_pos[0] - monster_lbl.get_width() // 2, monster_pos[1] - 10))


    # --- LOWER HUD DISPLAY (Step 7 & Challenge) ---
    # Background for the text panel
    pygame.draw.rect(screen, GRAY, (0, HEIGHT * 2 // 3, WIDTH, HEIGHT // 3))
    pygame.draw.line(screen, WHITE, (0, HEIGHT * 2 // 3), (WIDTH, HEIGHT * 2 // 3), 4)
   
    # Text Placement Coordinates
    text_x = 30
    start_y = (HEIGHT * 2 // 3) + 15
    line_spacing = 32
   
    if not game_over:
        # Step 7 Outputs
        screen.blit(font_ui.render(msg_current, True, WHITE), (text_x, start_y))
        screen.blit(font_ui.render(msg_ambush, True, WHITE), (text_x, start_y + line_spacing))
        screen.blit(font_ui.render(msg_moved, True, WHITE), (text_x, start_y + line_spacing * 2))
       
        # Color outcome conditionally
        color_res = GREEN if "SUCCESSFUL" in msg_result else RED
        screen.blit(font_body.render(msg_result, True, color_res), (text_x, start_y + line_spacing * 3))
       
        # Track active scores
        score_text = f"Round: {round_count}/{max_rounds}  |  Human Score: {human_score}  |  AI Score: {ai_score}"
        screen.blit(font_body.render(score_text, True, WHITE), (text_x, start_y + line_spacing * 4))
    else:
        # Game Over summary screen showing Challenge metrics
        game_over_lbl = font_title.render("GAME OVER (10 Rounds Completed)", True, RED)
        screen.blit(game_over_lbl, (text_x, start_y))
       
        h_perf = f"Human Prediction Success: {human_score}/{max_rounds}"
        a_perf = f"AI Prediction Success: {ai_score}/{max_rounds}"
        screen.blit(font_body.render(h_perf, True, WHITE), (text_x, start_y + line_spacing * 1.5))
        screen.blit(font_body.render(a_perf, True, WHITE), (text_x, start_y + line_spacing * 2.5))
       
        # Announce overall winner
        if human_score > ai_score:
            winner_text = "Result: Human Beats the AI!"
        elif ai_score > human_score:
            winner_text = "Result: AI Beats the Human!"
        else:
            winner_text = "Result: It's a Tie!"
        screen.blit(font_title.render(winner_text, True, GREEN), (text_x, start_y + line_spacing * 4))


    pygame.display.flip()
    clock.tick(30)


pygame.quit()
sys.exit()

