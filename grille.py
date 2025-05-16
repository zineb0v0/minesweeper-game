import random
from constants import *
from mines.ChampMines import ChampDeMines


class Cellule:
    def __init__(self):
        self.flagged = False  # Seul attribut nécessaire
        self.revealed = False  # Si la cellule a été révélée
        self.has_mine = False  # Si la cellule contient une mine

class Grille:
    def __init__(self, grille_lignes, grille_colonnes,num_mines):
        self.cells = [[Cellule() for _ in range(grille_colonnes)] for _ in range(grille_lignes)]
        self.champ = None  # ChampDeMines, initialisé après le premier clic
        self.first_click = True  # Pour s'assurer que les mines ne sont générées qu'une seule fois
        self.game_over = False
        self.flags_places = 0
        self.grille_lignes = grille_lignes
        self.grille_colonnes = grille_colonnes
        self.num_mines = num_mines
        self.victoire = False

    def put_flag(self, lig, col):
        if 0 <= lig < self.grille_lignes and 0 <= col < self.grille_colonnes:
            cell = self.cells[lig][col]
            if not cell.revealed:
                if not cell.flagged and self.flags_places < MAX_FLAGS:
                    cell.flagged = True
                    self.flags_places += 1
                    return True
                elif cell.flagged:
                    cell.flagged = False
                    self.flags_places -= 1
                    return True
        return False


    def reveal_cell(self, lig, col):
        if not (0 <= lig < self.grille_lignes and 0 <= col < self.grille_colonnes):
            return False  # Invalid coordinates

        if self.first_click:
            self.champ = ChampDeMines(self.grille_lignes, self.num_mines)
            self.champ.generer_mines((lig, col))
            for mine in self.champ.mines:
                self.cells[mine.x][mine.y].has_mine = True
            self.first_click = False

        cell = self.cells[lig][col]
        if cell.revealed or cell.flagged:
            return False  # Already revealed or flagged, nothing happened

        if cell.has_mine:
            cell.revealed = True
            self.game_over = True
            for mine in self.champ.mines:
                self.cells[mine.x][mine.y].revealed = True
        else:
            self._reveal_recursive(lig, col)

        return True  # A valid reveal occurred


    def _reveal_recursive(self, lig, col):
        """Révèle récursivement les cellules vides."""
        # Vérifier les limites de la grille
        if not (0 <= lig < self.grille_lignes and 0 <= col < self.grille_colonnes):
            return

        cell = self.cells[lig][col]
        # Ne pas traiter les cellules déjà révélées, minées ou marquées
        if cell.revealed or cell.has_mine or cell.flagged:
            return

        cell.revealed = True
        # Si pas de mines voisines, continuer la récursion
        if self.compter_mines_voisines(lig, col) == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i != 0 or j != 0:  # Éviter la cellule actuelle
                        self._reveal_recursive(lig + i, col + j)
                        # Compte le nombre de mines voisines pour une cellule donnée

    # Cette méthode est appelée lorsque la cellule est révélée
    # et permet de savoir combien de mines sont autour d'elle     par Abdelghani Bensalih
    def compter_mines_voisines(self, lig, col):
        mines = 0
        for i in range(-1, 2):  # -1, 0, 1
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                voisin_lig = lig + i
                voisin_col = col + j
                if 0 <= voisin_lig < self.grille_lignes and 0 <= voisin_col < self.grille_colonnes:
                    if self.cells[voisin_lig][voisin_col].has_mine:
                        mines += 1
        return mines 
    


    