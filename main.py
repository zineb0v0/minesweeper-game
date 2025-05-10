import pygame
import os
import numpy as np
from resultats import *
from grille import Grille
from DQN.DQN_agent import *
from DQN.DQN import create_dqn
from minesweeper_env import MinesweeperEnv
from constants import *
import time

# Initialisation Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Démineur")
pygame.display.set_icon(pygame.image.load("images/bombe.png"))
font = pygame.font.SysFont('Consolas', 30)

# Chargement des images
FLAG_IMG = pygame.transform.scale(pygame.image.load("images/flag.png"), (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))
Mine_IMG = pygame.transform.scale(pygame.image.load("images/mine.png"), (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))
background_img = pygame.transform.scale(pygame.image.load("images/image.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
header_img = pygame.transform.scale(pygame.image.load("images/header_BG.webp"), (400, 100))
Flag_logo = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("images/GAGA1.png"), (70, 90)), -30)
cloud_img = pygame.transform.scale(pygame.image.load("images/clouds.webp"), (300, 260))
cloud_img1 = pygame.transform.scale(cloud_img, (170, 100))
cloud_img2 = pygame.transform.scale(cloud_img, (200, 130))
cloud_img3 = pygame.transform.scale(cloud_img, (350, 290))

AI_TURN = 0
PLAYER_TURN = 1


class AIController:
    def __init__(self, grille):
        print("Initializing AI Controller...")  # Debug
        self.grille = grille
        try:
            self.env = self.create_env_from_grid()
            print("Environment created successfully")  # Debug
            self.agent = DQNAgent(self.env)
            print("AI Agent initialized!")  # Debug
        except Exception as e:
            print(f"AI INIT ERROR: {str(e)}")  # Debug
            raise

    def create_env_from_grid(self):
        # Crée un environnement basé sur la grille actuelle
        env = MinesweeperEnv(self.grille.grille_lignes,
                             self.grille.grille_colonnes,
                             self.grille.num_mines)
        # Met à jour l'état de l'environnement pour correspondre à la grille
        env.state_im = self.convert_grid_to_state()
        return env

    def get_ai_move(self):
        state = self.convert_grid_to_state()
        while True:
            action = self.agent.get_action(state)
            row = action // self.grille.grille_colonnes
            col = action % self.grille.grille_colonnes
        
            # Ne pas jouer sur les cases marquées
            if not self.grille.cells[row][col].flagged:  
                return row, col

    def convert_grid_to_state(self):
        state = np.zeros((self.grille.grille_lignes, self.grille.grille_colonnes, 1))
        for i in range(self.grille.grille_lignes):
            for j in range(self.grille.grille_colonnes):
                cell = self.grille.cells[i][j]
                if cell.revealed:
                    if cell.has_mine:
                        state[i][j] = -1  # Mine
                    else:
                        mines = self.grille.compter_mines_voisines(i, j)
                        state[i][j] = mines / 8  # Normaliser entre 0-1
                elif cell.flagged:
                    state[i][j] = -0.5  # Drapeau
                else:
                    state[i][j] = -0.125  # Caché
        return state


def dessiner_grille(screen, grille, offset_x, offset_y):
    for lig in range(grille.grille_lignes):
        for col in range(grille.grille_colonnes):
            x = col * CELL_SIZE + offset_x
            y = lig * CELL_SIZE + offset_y
            cell = grille.cells[lig][col]
            rect = pygame.Rect(x, y + 30, CELL_SIZE - 1, CELL_SIZE - 1)

            color = bleu_pas_fond if cell.revealed else bleu_fond
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

            if cell.revealed and not cell.has_mine:
                mines_voisines = grille.compter_mines_voisines(lig, col)
                if mines_voisines > 0:
                    font = pygame.font.Font(None, 24)
                    text = font.render(str(mines_voisines), True, (0, 0, 255))
                    screen.blit(text, (x + 10, y + 35))

            if cell.revealed and cell.has_mine:
                screen.blit(pygame.transform.scale(Mine_IMG, (CELL_SIZE - 4, CELL_SIZE - 4)), (x + 2, y + 32))

            if cell.flagged and not cell.revealed:
                screen.blit(pygame.transform.scale(FLAG_IMG, (CELL_SIZE - 4, CELL_SIZE - 4)), (x + 2, y + 32))


def afficher_chrono(screen, temps_ms):
    temps_s = temps_ms // 1000
    sec = temps_s % 60
    min = temps_s // 60
    chrono_text = f"{min:02}:{sec:02}"
    chrono_surface = font.render(chrono_text, True, WHITE)
    text_rect = chrono_surface.get_rect(topright=(SCREEN_WIDTH - 60, 50))
    bg_rect = pygame.Rect(SCREEN_WIDTH - RECT_WIDTH - 35, 45, RECT_WIDTH, RECT_HEIGHT)
    pygame.draw.rect(screen, bleu_fond, bg_rect, border_radius=30)
    screen.blit(chrono_surface, text_rect)


def afficher_message(screen, message):
    font = pygame.font.SysFont(None, 40)
    text = font.render(message, True, (255, 0, 0))
    rect = text.get_rect(center=(screen.get_width() // 2, 25))
    screen.blit(text, rect)


def afficher_flags(screen, flags_restants, total_flags):
    color = RED if flags_restants < 0 else WHITE
    flags_text = f"{flags_restants}"
    flags_surface = font.render(flags_text, True, color)
    text_rect = flags_surface.get_rect(topleft=(85, 50))
    bg_rect = pygame.Rect(35, 45, RECT_WIDTH, RECT_HEIGHT)
    pygame.draw.rect(screen, bleu_fond, bg_rect, border_radius=30)
    screen.blit(flags_surface, text_rect)


def draw_control_buttons():
    button_width, button_height = 120, 40
    padding = 20

    # Bouton Quit
    quit_rect = pygame.Rect(30, SCREEN_HEIGHT - button_height - padding, button_width, button_height)
    pygame.draw.rect(screen, bleu_fond, quit_rect, border_radius=15)
    quit_text = font.render("Quit", True, ORANGE_SHADOW)
    screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

    # Bouton Restart
    restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - button_height - padding, 150, button_height)
    pygame.draw.rect(screen, bleu_pas_fond, restart_rect, border_radius=15)
    pygame.draw.rect(screen, ORANGE_SHADOW, restart_rect, 2, border_radius=15)
    restart_text = font.render("Restart", True, bleu_fond)
    screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))

    # Bouton Menu
    menu_rect = pygame.Rect(SCREEN_WIDTH - button_width - 30, SCREEN_HEIGHT - button_height - padding, button_width,
                            button_height)
    pygame.draw.rect(screen, bleu_fond, menu_rect, border_radius=15)
    menu_text = font.render("Menu", True, ORANGE_SHADOW)
    screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))


def check_button_click(pos):
    x, y = pos
    if 30 <= x <= 150 and SCREEN_HEIGHT - 60 <= y <= SCREEN_HEIGHT - 20:
        return "quit"
    if SCREEN_WIDTH // 2 - 75 <= x <= SCREEN_WIDTH // 2 + 75 and SCREEN_HEIGHT - 60 <= y <= SCREEN_HEIGHT - 20:
        return "restart"
    if SCREEN_WIDTH - 150 <= x <= SCREEN_WIDTH - 30 and SCREEN_HEIGHT - 60 <= y <= SCREEN_HEIGHT - 20:
        return "menu"
    return None


def show_welcome_screen():
    show_welcome = True
    while show_welcome:
        screen.blit(background_img, (0, 0))
        welcome_font = pygame.font.SysFont("pixel-font.ttf", 60)
        welcome_text = welcome_font.render("DÉMINEUR", True, ORANGE_SHADOW)
        screen.blit(welcome_text, welcome_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

        # Bouton Start
        button_width, button_height = 140, 50
        start_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height // 2,
                                 button_width, button_height)
        pygame.draw.rect(screen, ORANGE_SHADOW, (start_rect.x, start_rect.y + 8, button_width, button_height),
                         border_radius=10)
        pygame.draw.rect(screen, bleu_fond, start_rect, border_radius=10)
        start_text = font.render("START", True, WHITE)
        screen.blit(start_text, start_text.get_rect(center=start_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False

            if event.type == pygame.MOUSEBUTTONDOWN and start_rect.collidepoint(pygame.mouse.get_pos()):
                return True, True

    return False, False


def choose_game_mode():
    choosing = True
    ai_mode = False

    while choosing:
        screen.blit(background_img, (0, 0))
        welcome_font = pygame.font.SysFont("pixel-font.ttf", 60)
        welcome_text = welcome_font.render("DÉMINEUR", True, ORANGE_SHADOW)
        screen.blit(welcome_text, welcome_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

        # Bouton Solo
        button_width, button_height = 140, 50
        solo_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height // 2,
                                button_width, button_height)
        pygame.draw.rect(screen, ORANGE_SHADOW, (solo_rect.x, solo_rect.y + 8, button_width, button_height),
                         border_radius=10)
        pygame.draw.rect(screen, bleu_fond, solo_rect, border_radius=10)
        solo_text = font.render("SOLO", True, WHITE)
        screen.blit(solo_text, solo_text.get_rect(center=solo_rect.center))

        # Bouton AI
        ai_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 75 - button_height // 2,
                              button_width, button_height)
        pygame.draw.rect(screen, ORANGE_SHADOW, (ai_rect.x, ai_rect.y + 8, button_width, button_height),
                         border_radius=10)
        pygame.draw.rect(screen, bleu_fond, ai_rect, border_radius=10)
        ai_text = font.render("AI", True, WHITE)
        screen.blit(ai_text, ai_text.get_rect(center=ai_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if solo_rect.collidepoint(pygame.mouse.get_pos()):
                    return True, False
                elif ai_rect.collidepoint(pygame.mouse.get_pos()):
                    return True, True

    return False, False


def choose_difficulty():
    choosing = True
    difficulty = None

    while choosing:
        screen.blit(background_img, (0, 0))
        screen.blit(cloud_img, (-100, 500))
        screen.blit(cloud_img1, (370, 200))
        screen.blit(cloud_img, (250, 440))
        screen.blit(cloud_img, (-90, -150))

        welcome_font = pygame.font.SysFont("pixel-font.ttf", 60)
        welcome_text = welcome_font.render("DÉMINEUR", True, ORANGE_SHADOW)
        screen.blit(welcome_text, welcome_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))

        button_width, button_height = 190, 50
        easy_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height // 2,
                                button_width, button_height)
        medium_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 75 - button_height // 2,
                                  button_width, button_height)
        hard_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 150 - button_height // 2,
                                button_width, button_height)

        # Dessiner les boutons
        for rect, text, y_offset in [(easy_rect, "Facile", 0),
                                     (medium_rect, "Moyen", 75),
                                     (hard_rect, "Difficile", 150)]:
            pygame.draw.rect(screen, ORANGE_SHADOW, (rect.x, rect.y + 8, button_width, button_height), border_radius=10)
            pygame.draw.rect(screen, bleu_fond, rect, border_radius=10)
            btn_text = font.render(text, True, WHITE)
            screen.blit(btn_text, btn_text.get_rect(center=rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(pygame.mouse.get_pos()):
                    return (9, 9, 10)  # Facile
                elif medium_rect.collidepoint(pygame.mouse.get_pos()):
                    return (14, 14, 30)  # Moyen
                elif hard_rect.collidepoint(pygame.mouse.get_pos()):
                    return (16, 16, 50)  # Difficile

    return None


def main():
    # Écrans initiaux
    show_game, ai_mode = show_welcome_screen()
    if not show_game:
        pygame.quit()
        return

    show_game, ai_mode = choose_game_mode()
    if not show_game:
        pygame.quit()
        return

    difficulty = choose_difficulty()
    if not difficulty:
        pygame.quit()
        return

    grille_lignes, grille_colonnes, num_mines = difficulty
    grille = Grille(grille_lignes, grille_colonnes, num_mines)

    # Variables de jeu
    jeu_demarre = False
    temps_debut = 0
    temps_ecoule = 0
    clicks = 1
    revealed = 0
    ai_controller = None
    current_turn = PLAYER_TURN  # Player starts first
    ai_thinking_start_time = None
    # Initialize AI if selected
    if ai_mode:
        try:
            ai_controller = AIController(grille)
        except Exception as e:
            print(f"Failed to initialize AI: {e}")
            ai_mode = False

    # Boucle principale
    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # Gestion du temps
        if jeu_demarre and not grille.game_over:
            temps_ecoule = current_time - temps_debut

        # Affichage
        screen.blit(background_img, (0, 0))
        screen.blit(cloud_img, (-140, 390))
        screen.blit(cloud_img3, (-50, 430))
        screen.blit(cloud_img, (260, 400))
        screen.blit(cloud_img2, (140, 500))
        screen.blit(header_img, (30, 15))

        offset_x = (screen.get_width() - grille.grille_colonnes * CELL_SIZE) // 2
        offset_y = (screen.get_height() - grille.grille_lignes * CELL_SIZE) // 2

        dessiner_grille(screen, grille, offset_x, offset_y)
        afficher_flags(screen, grille.num_mines - grille.flags_places, grille.num_mines)
        screen.blit(Flag_logo, (7, 5))

        if jeu_demarre:
            afficher_chrono(screen, temps_ecoule)

        # Indicateur de tour simplifié
        if ai_mode and not grille.game_over:
            turn_text = "Player Turn"   if current_turn == PLAYER_TURN else "AI Turn"
            turn_color = (0, 255, 0) if current_turn == PLAYER_TURN else (255, 0, 0)
            turn_surface = font.render(turn_text, True, turn_color)
            screen.blit(turn_surface, (SCREEN_WIDTH // 2 - 50, 50))

        draw_control_buttons()
        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Boutons de contrôle
                action = check_button_click(event.pos)
                if action == "quit":
                    running = False
                elif action == "restart":
                    main()
                    return
                elif action == "menu":
                    main()
                    return

                # Gestion du clic joueur
                if current_turn == PLAYER_TURN and not grille.game_over:
                    
                    x, y = event.pos
                    if y >= 30:  # Évite la zone du header
                        col = (x - offset_x) // CELL_SIZE
                        row = (y - offset_y - 30) // CELL_SIZE
                        
                        if 0 <= row < grille_lignes and 0 <= col < grille_colonnes:
                            if not jeu_demarre:
                                jeu_demarre = True
                                temps_debut = current_time
                            
                            if event.button == 1:  # Clic gauche
                                if not grille.cells[row][col].flagged:
                                    grille.reveal_cell(row, col)
                                    if ai_mode:
                                        current_turn = AI_TURN
                            elif event.button == 3:  # Clic droit
                                grille.put_flag(row, col)

        # Tour de l'IA (version simplifiée)
        if ai_mode and current_turn == AI_TURN and not grille.game_over:
            
            if ai_thinking_start_time is None:
                ai_thinking_start_time = current_time   
            elif current_time - ai_thinking_start_time > 1000:  # IA pense pendant 1 seconde    
                ai_thinking_start_time = None
                try:
                     # Pause pour simuler le temps de réflexion de l'IA
                    row, col = ai_controller.get_ai_move()
                    if not grille.cells[row][col].flagged:
                        grille.reveal_cell(row, col)
                        
                        current_turn = PLAYER_TURN
                        
                except Exception as e:
                    print(f"AI move error: {e}")
                    current_turn = PLAYER_TURN

        # Fin de partie
        if grille.game_over or verifier_victoire(grille, grille_lignes, grille_colonnes):
            efficacite = (revealed / clicks) * 100 if clicks > 0 else 0
            stats_data = {
                'time': temps_ecoule,
                'clicks': clicks,
                'efficiency': efficacite,
                'result': "VICTOIRE !" if grille.victoire else "PERDU !"
            }
            
            # Afficher l'écran de fin
            screen.blit(background_img, (0, 0))
            dessiner_grille(screen, grille, offset_x, offset_y)
            afficher_flags(screen, grille.num_mines - grille.flags_places, grille.num_mines)
            afficher_chrono(screen, stats_data['time'])
            
            # Afficher les stats
            panel_rect = pygame.Rect(50, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 100, 120)
            pygame.draw.rect(screen, (20, 40, 70), panel_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), panel_rect, 2, border_radius=5)

            stats_font = pygame.font.SysFont('Arial', 20)
            y = panel_rect.y + 25
            stats = [
                f"Temps: {temps_ecoule / 1000:.3f} sec",
                f"Clics: {clicks}",
                f"Efficacité: {efficacite:.0f}%"
            ]

            for stat in stats:
                text = stats_font.render(stat, True, (255, 255, 255))
                screen.blit(text, (panel_rect.x + 20, y + 10))
                y += 25

            result_font = pygame.font.SysFont('Arial', 24, bold=True)
            result_color = (0, 255, 0) if "VICTOIRE" in stats_data['result'] else (255, 0, 0)
            result_text = result_font.render(stats_data['result'], True, result_color)
            screen.blit(result_text, (panel_rect.centerx - 30, panel_rect.y + 10))

            draw_control_buttons()
            pygame.display.flip()

            # Attendre l'action du joueur
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        action = check_button_click(pygame.mouse.get_pos())
                        if action == "quit":
                            waiting = False
                            running = False
                        elif action == "restart":
                            main()
                            return
                        elif action == "menu":
                            main()
                            return

    pygame.quit()
if __name__ == "__main__":
    main()