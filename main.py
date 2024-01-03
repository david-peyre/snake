import pygame
import sys
import random
import json


# Initialisation de Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)

# Niveaux de difficulté
DIFFICULTY_LEVELS = {
    "Easy": 8,
    "Medium": 12,
    "Hard": 16
}

direction = "RIGHT"  # Initialisation de la direction
snake_length = 1  # Initialisation de la longueur du serpent
score = 0  # Initialisation du score

# Fonction principale
def main():
    global direction
    global snake_length
    global score

    # Initialisation de la fenêtre
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Afficher le menu pour choisir le niveau de difficulté
    difficulty_level = show_menu(screen)

    # Initialisation du serpent
    snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

    # Position initiale de la pomme
    apple = spawn_apple(snake)

    # Initialisation de la vitesse du serpent
    FPS = DIFFICULTY_LEVELS[difficulty_level]

    # Horloge pour contrôler la vitesse du jeu
    clock = pygame.time.Clock()

    # Boucle principale du jeu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = "UP"
                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    direction = "RIGHT"

        # Déplacement du serpent
        snake = move_snake(snake, direction)

        # Vérification des collisions
        if check_collision(snake):
            pygame.quit()
            sys.exit()

        # Vérification si le serpent mange la pomme
        if snake[0] == apple:
            score += 1
            snake_length += 1
            save_score(score)  # Appel de la fonction pour enregistrer le score dans le fichier JSON
            apple = spawn_apple(snake)


        # Affichage du fond
        screen.fill(WHITE)

        # Affichage du serpent
        draw_snake(screen, snake)

        # Affichage de la pomme
        draw_apple(screen, apple)

        # Rafraîchissement de l'écran
        pygame.display.flip()

        # Contrôle de la vitesse du jeu
        clock.tick(FPS)

def save_score(score):
    data = {"score": score}
    with open("score.json", "w") as file:
        json.dump(data, file)


# Fonction pour déplacer le serpent
def move_snake(snake, direction):
    x, y = snake[0]
    if direction == "UP":
        y -= CELL_SIZE
    elif direction == "DOWN":
        y += CELL_SIZE
    elif direction == "LEFT":
        x -= CELL_SIZE
    elif direction == "RIGHT":
        x += CELL_SIZE

    # Correction pour permettre au serpent de traverser les bords de l'écran
    x %= SCREEN_WIDTH
    y %= SCREEN_HEIGHT

    # Ajout de la nouvelle tête du serpent
    snake.insert(0, (x, y))

    # Réduction de la longueur du serpent s'il est trop long
    if len(snake) > snake_length:
        snake.pop()

    return snake

# Fonction pour dessiner le serpent
def draw_snake(screen, snake):
    for segment in snake:
        pygame.draw.circle(screen, GREEN, (segment[0] + CELL_SIZE // 2, segment[1] + CELL_SIZE // 2), CELL_SIZE // 2)
    draw_score(screen, score)

# Fonction pour générer une position aléatoire pour la pomme
def spawn_apple(snake):
    while True:
        x = random.randrange(0, SCREEN_WIDTH, CELL_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT, CELL_SIZE)
        if (x, y) not in snake:
            return (x, y)

# Fonction pour dessiner la pomme
def draw_apple(screen, apple):
    pygame.draw.circle(screen, RED, (apple[0] + CELL_SIZE // 2, apple[1] + CELL_SIZE // 2), CELL_SIZE // 2)

# Fonction pour vérifier les collisions avec les bords de l'écran ou avec le serpent lui-même
def check_collision(snake):
    x, y = snake[0]
    if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT or len(snake) != len(set(snake)):
        return True
    return False

# Fonction pour afficher le menu et choisir le niveau de difficulté
def show_menu(screen):
    menu_font = pygame.font.Font(None, 36)
    selected_level = 0

    while True:
        screen.fill(WHITE)

        for i, (level, speed) in enumerate(DIFFICULTY_LEVELS.items()):
            text = menu_font.render(f"{level}: {speed} FPS", True, RED if i == selected_level else BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))

            # Ajout d'un rectangle autour du texte
            pygame.draw.rect(screen, RED if i == selected_level else BLACK, text_rect, 2)

            screen.blit(text, text_rect.topleft)

        pygame.display.flip()

        # Option Score
        score_text = menu_font.render("Score", True, RED if selected_level == len(DIFFICULTY_LEVELS) else BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + len(DIFFICULTY_LEVELS) * 40))
        pygame.draw.rect(screen, RED if selected_level == len(DIFFICULTY_LEVELS) else BLACK, score_rect, 2)
        screen.blit(score_text, score_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % len(DIFFICULTY_LEVELS)
                elif event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % len(DIFFICULTY_LEVELS)
                elif event.key == pygame.K_RETURN:
                    if selected_level == len(DIFFICULTY_LEVELS):
                        return "Score"
                    else:
                        return list(DIFFICULTY_LEVELS.keys())[selected_level]

# Fonction pour dessiner le score
def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# Exécution de la fonction principale
if __name__ == "__main__":
    main()
