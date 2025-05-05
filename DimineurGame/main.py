import pygame
from resultats import *
from grille import Grille

# from resultats import fin_de_jeu
pygame.init()  # Initialise tous les modules Pygame et Active les modules graphiques/audio/inputs
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Crée la fenêtre de jeu avec les dimensions définies dans constants.py

pygame.display.set_caption("Démineur")  # Définit le titre de la fenêtre
pygame.display.set_icon(pygame.image.load("images/bombe.png"))
font = pygame.font.SysFont('Consolas', 30)

FLAG_IMG = pygame.image.load("images/flag.png")  # Charge l'image du drapeau
FLAG_IMG = pygame.transform.scale(FLAG_IMG, (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))  # Redimensionne l'image à 80% de la taille d'une cellule
Mine_IMG = pygame.image.load("images/mine.png")
Mine_IMG = pygame.transform.scale(Mine_IMG, (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))

BG_COLOR = (10, 25, 47)  # Bleu nuit
background_img = pygame.image.load("images/image.png")  # or .png, whatever you have
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Make sure it fits the window
header_img = pygame.image.load("images/header_BG.webp")
header_img = pygame.transform.scale(header_img , (400,100))  # Make sure it fits the window

Flag_logo = pygame.image.load("images/GAGA1.png")
Flag_logo = pygame.transform.scale(Flag_logo, (70, 90))
Flag_logo = pygame.transform.rotate(Flag_logo, -30)

cloud_img = pygame.image.load("images/clouds.webp")  # or .png, whatever you have
cloud_img = pygame.transform.scale(cloud_img, (300, 260))
cloud_img1 = pygame.transform.scale(cloud_img, (170, 100))
cloud_img2 = pygame.transform.scale(cloud_img, (200, 130))
cloud_img3 = pygame.transform.scale(cloud_img, (350, 290))

def dessiner_grille(screen, grille,offset_x, offset_y):
    for lig in range(grille.grille_lignes):
        for col in range(grille.grille_colonnes):
            x = col * CELL_SIZE + offset_x
            y = lig * CELL_SIZE + offset_y
            cell = grille.cells[lig][col]
            rect = pygame.Rect(x,y + 30, CELL_SIZE - 1, CELL_SIZE - 1)

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

    text_rect = chrono_surface.get_rect()
    text_rect.topright = (SCREEN_WIDTH - 60, 50)  # En haut à droite avec un petit espace


    bg_rect = pygame.Rect(
        SCREEN_WIDTH- RECT_WIDTH-35,
        45,
        RECT_WIDTH,
        RECT_HEIGHT
        )

    # Fond pour le chrono
    pygame.draw.rect(screen, bleu_fond, bg_rect, border_radius=30)
    screen.blit(chrono_surface, text_rect)


def afficher_message(screen, message):
    font = pygame.font.SysFont(None, 40)
    text = font.render(message, True, (255, 0, 0))
    rect = text.get_rect(center=(screen.get_width() // 2, 25))
    screen.blit(text, rect)


def afficher_flags(screen, flags_restants, total_flags):
    color = RED if flags_restants < 0 else WHITE  # Rouge si trop de drapeaux placés
    flags_text = f"{flags_restants}"

    flags_surface = font.render(flags_text, True, color)

    # Crée un rectangle autour du texte
    text_rect = flags_surface.get_rect()
    text_rect.topleft = (85, 50)  # Position du texte (comme tu veux)

    bg_rect = pygame.Rect(
        35,
        45,
        RECT_WIDTH,
        RECT_HEIGHT
    )

    # Dessine le fond arrondi
    pygame.draw.rect(screen, bleu_fond, bg_rect, border_radius=30)
    screen.blit(flags_surface, text_rect)
def afficher_stats(screen, temps_ecoule, clicks, efficacite, resultat):
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
        screen.blit(text, (panel_rect.x + 20, y +10))
        y += 25

    result_font = pygame.font.SysFont('Arial', 24, bold=True)
    result_color = (0, 255, 0) if "VICTOIRE" in resultat else (255, 0, 0)
    result_text = result_font.render(resultat, True, result_color)
    screen.blit(result_text, (panel_rect.centerx - 30, panel_rect.y +10))

def draw_control_buttons():
    """Dessine les boutons de contrôle en bas de l'écran (texte seulement)"""
    button_width = 120
    button_width1 = 150
    button_height = 40
    padding = 20

    # Bouton Quit (texte seulement)
    quit_rect = pygame.Rect(30, SCREEN_HEIGHT - button_height - padding, button_width, button_height)
    pygame.draw.rect(screen, bleu_fond, quit_rect, border_radius=15)  # Fond bleu foncé
    quit_text = font.render("Quit", True, ORANGE_SHADOW)  # Texte gris clair
    quit_text_rect = quit_text.get_rect(center=quit_rect.center)
    screen.blit(quit_text, quit_text_rect)

    # Bouton Restart (texte seulement)
    restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width1 // 2, SCREEN_HEIGHT - button_height - padding,
                               button_width1, button_height)
    pygame.draw.rect(screen, bleu_pas_fond, restart_rect, border_radius=15)  # Fond bleu clair-rose
    pygame.draw.rect(screen, ORANGE_SHADOW, restart_rect, width=2, border_radius=15)  # <- seulement la bordure

    restart_text = font.render("Restart", True, bleu_fond)
    restart_text_rect = restart_text.get_rect(center=restart_rect.center)
    screen.blit(restart_text, restart_text_rect)

    # Bouton Menu (texte seulement)
    menu_rect = pygame.Rect(SCREEN_WIDTH - button_width - 30, SCREEN_HEIGHT - button_height - padding, button_width,
                            button_height)
    pygame.draw.rect(screen, bleu_fond, menu_rect, border_radius=15)
    menu_text = font.render("Menu", True, ORANGE_SHADOW)
    menu_text_rect = menu_text.get_rect(center=menu_rect.center)
    screen.blit(menu_text, menu_text_rect)

def check_button_click(pos):
    """Vérifie quel bouton a été cliqué (zones approximatives autour du texte)"""
    x, y = pos
    
    # Zones cliquables approximatives (adaptez selon la taille de votre texte)
    if 10 <= x <= 110 and SCREEN_HEIGHT - 50 <= y <= SCREEN_HEIGHT - 10:  # Quit
        return "quit"
    if SCREEN_WIDTH//2 - 50 <= x <= SCREEN_WIDTH//2 + 50 and SCREEN_HEIGHT - 50 <= y <= SCREEN_HEIGHT - 10:  # Restart
        return "restart"
    if SCREEN_WIDTH - 110 <= x <= SCREEN_WIDTH - 10 and SCREEN_HEIGHT - 50 <= y <= SCREEN_HEIGHT - 10:  # Menu
        return "menu"
    
    return None
def handle_stats_screen(screen, grille, stats_data,offset_x,offset_y):
    screen.blit(background_img, (0, 0))
    dessiner_grille(screen, grille,offset_x,offset_y)
    afficher_flags(screen, grille.num_mines - grille.flags_places, grille.num_mines)
    afficher_chrono(screen, stats_data['time'])
    afficher_stats(screen, stats_data['time'], stats_data['clicks'], stats_data['efficiency'], stats_data['result'])
        
    draw_control_buttons()
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = check_button_click(event.pos)
                if action:
                    return action
    return None

def main():
    # État pour la page d'accueil
    show_welcome = True
    
    while show_welcome:
        # Dessiner la page d'accueil
        screen.blit(background_img, (0, 0))
        # Titre
        welcome_font = pygame.font.SysFont("pixel-font.ttf", 60)
        welcome_text = welcome_font.render("DÉMINEUR", True, ORANGE_SHADOW)
        welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        screen.blit(welcome_text, welcome_rect)
        
        # Bouton Start
        start_font = pygame.font.SysFont('Consolas', 30)
        start_text = start_font.render("START", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

        button_width, button_height = 140, 50

        pygame.draw.rect(screen, ORANGE_SHADOW, ( SCREEN_WIDTH // 2 - button_width // 2 , SCREEN_HEIGHT // 2 - button_height // 2 +8, button_width , button_height),border_radius= 10)
        pygame.draw.rect(screen, bleu_fond, (SCREEN_WIDTH // 2 - button_width // 2,  SCREEN_HEIGHT // 2 - button_height // 2, button_width, button_height), border_radius=10)
        screen.blit(start_text, start_rect)
        
        pygame.display.flip()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if SCREEN_WIDTH//2-70 <= mouse_pos[0] <= SCREEN_WIDTH//2+70 and \
                   SCREEN_HEIGHT//2-25 <= mouse_pos[1] <= SCREEN_HEIGHT//2+25:
                    show_welcome = False
    start = True
    play = False
    jeu_demarre = False
    grille_lignes, grille_colonnes, num_mines = 0,0,0
    clicks = 1
    revealed = 0
    start_time = 0
    show_stats = False

    while start:
        #dessiner la page d'accueil avec 3 niveaux de difficulté
        screen.blit(background_img, (0, 0))
        screen.blit(cloud_img, (-100, 500))
        screen.blit(cloud_img1, (370, 200))
        screen.blit(cloud_img, (250, 440))
        screen.blit(cloud_img, (-90, -150))

        title_rect = welcome_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(welcome_text, title_rect)

        button_width, button_height = 190, 50
        # Positions Y pour les trois boutons
        easy_y = SCREEN_HEIGHT // 2
        medium_y = easy_y + 75
        hard_y = medium_y + 75

        easy_text = font.render("Facile", True, WHITE)
        easy_rect = easy_text.get_rect(center=(SCREEN_WIDTH // 2, easy_y))

        pygame.draw.rect(screen, ORANGE_SHADOW, (
        SCREEN_WIDTH // 2 - button_width // 2, easy_y - button_height // 2 + 8, button_width, button_height),border_radius=10)
        pygame.draw.rect(screen, bleu_fond, (
        SCREEN_WIDTH // 2 - button_width // 2, easy_y - button_height // 2, button_width, button_height),border_radius=10)
        screen.blit(easy_text, easy_rect)

        medium_text = font.render("Moyen", True, WHITE)
        medium_rect = medium_text.get_rect(center=(SCREEN_WIDTH // 2, medium_y))

        pygame.draw.rect(screen, ORANGE_SHADOW, (SCREEN_WIDTH // 2 - button_width // 2, medium_y - button_height // 2 + 8, button_width, button_height),border_radius=10)
        pygame.draw.rect(screen, bleu_fond, (SCREEN_WIDTH // 2 - button_width // 2, medium_y - button_height // 2, button_width, button_height),border_radius=10)
        screen.blit(medium_text, medium_rect)

        hard_text = font.render("Difficile", True, WHITE)
        hard_rect = hard_text.get_rect(center=(SCREEN_WIDTH // 2, hard_y))
        pygame.draw.rect(screen, ORANGE_SHADOW, (SCREEN_WIDTH // 2 - button_width // 2, hard_y - button_height // 2 + 8, button_width, button_height),border_radius=10)
        pygame.draw.rect(screen, bleu_fond, (SCREEN_WIDTH // 2 - button_width // 2, hard_y - button_height // 2, button_width, button_height),border_radius=10)
        screen.blit(hard_text, hard_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if easy_rect.collidepoint(x, y): 
                    grille_lignes, grille_colonnes, num_mines = 9, 9, 10
                    play = True
                    start = False
                elif medium_rect.collidepoint(x, y):
                    grille_lignes, grille_colonnes, num_mines = 14, 14, 30
                    play = True
                    start = False
                elif hard_rect.collidepoint(x, y):
                    grille_lignes, grille_colonnes, num_mines = 16, 16, 50
                    play = True
                    start = False
            
    grille = Grille(grille_lignes,grille_colonnes,num_mines)  # Initialisation de la grille
    jeu_demarre = False
    temps_debut = 0
    temps_ecoule = 0
    clicks = 1
    revealed = 0
    play = True

    # Boucle principale du jeu
    while play:
        if jeu_demarre and not grille.game_over:
            temps_ecoule = pygame.time.get_ticks() - temps_debut

        screen.blit(background_img, (0, 0))

        screen.blit(cloud_img, (-140, 390))
        screen.blit(cloud_img3, (-50, 430))
        screen.blit(cloud_img, (260, 400))
        screen.blit(cloud_img2, (140, 500))

        screen.blit(header_img, (30,15))
        offset_x = (screen.get_width() - grille.grille_colonnes * CELL_SIZE) // 2
        offset_y = (screen.get_height() - grille.grille_lignes * CELL_SIZE) // 2

        dessiner_grille(screen, grille, offset_x, offset_y)
        afficher_flags(screen, grille.num_mines - grille.flags_places, grille.num_mines)
        screen.blit(Flag_logo, (7,5))

        if jeu_demarre:
            afficher_chrono(screen, temps_ecoule)
        
        draw_control_buttons()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier les boutons de contrôle
                action = check_button_click(event.pos)
                if action == "quit":
                    pygame.quit()
                    return
                elif action == "restart":
                    grille = Grille(grille_lignes, grille_colonnes, num_mines)
                    jeu_demarre = False
                    temps_debut = 0
                    temps_ecoule = 0
                    clicks = 0
                    revealed = 0
                    continue
                elif action == "menu":
                    play = False
                    main()  # Retour au menu principal
                    return
                
                # Gestion des clics sur la grille
                x, y = pygame.mouse.get_pos()
                if y >= 30:
                    col = (x-offset_x) // CELL_SIZE
                    lig = (y -offset_y- 30) // CELL_SIZE
                    
                    if 0 <= lig < grille_lignes and 0 <= col < grille_colonnes and not grille.game_over:
                        if not jeu_demarre:
                            jeu_demarre = True
                            temps_debut = pygame.time.get_ticks()
                            
                        if event.button == 3:  # Clic droit
                            grille.put_flag(lig, col)
                            clicks += 1
                        elif event.button == 1:  # Clic gauche
                            if not grille.cells[lig][col].flagged:
                                if grille.reveal_cell(lig, col):
                                    clicks += 1
                                    revealed += 1
                                    if grille.cells[lig][col].has_mine:
                                        grille.game_over = True
        # Vérifier fin de partie
        if grille.game_over or verifier_victoire(grille, grille_lignes, grille_colonnes):
            efficacite = (revealed / clicks) * 100
            stats_data = {
                'time': temps_ecoule,
                'clicks': clicks,
                'efficiency': efficacite,
                'result': "VICTOIRE !" if grille.victoire else "PERDU !",
                'grille': grille
            }
            
            action = handle_stats_screen(screen, grille, stats_data,offset_x,offset_y)
            if action == "quit":
                pygame.quit()
                return
            elif action == "restart":
                grille = Grille(grille_lignes, grille_colonnes, num_mines)
                jeu_demarre = False
                temps_debut = 0
                temps_ecoule = 0
                clicks = 1
                revealed = 0
            elif action == "menu":
                play = False
                main()
                return

    pygame.quit()


if __name__ == "__main__":
    main()
