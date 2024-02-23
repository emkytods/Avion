import pygame
import sys
import random
import os

try:
    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,30'  # Définir la position de la fenêtre (coin supérieur gauche de l'écran)

    pygame.init()

    # Taille et titre de la fenêtre
    largeur = 1538
    hauteur = 797
    fenetre = pygame.display.set_mode((largeur, hauteur))  # Initialiser en mode fenêtré
    titre_fenetre = "Jeu d'avion et pièces"
    pygame.display.set_caption(titre_fenetre)
    #print("Une fenêtre du nom de", '"' + titre_fenetre + '"', "devrait s'ouvrir")

    # Chargement et redimensionnement de l'avion
    avion = pygame.image.load("avion.png")
    avion_redimensionne = pygame.transform.scale(avion, (avion.get_width() // 6, avion.get_height() // 6))

    # Chargement et redimensionnement de la pièce
    piece = pygame.image.load("piece.png")
    piece_redimensionne = pygame.transform.scale(piece, (piece.get_width() // 14, piece.get_height() // 14))

    # Chargement du son pour le ramassage de la pièce
    chemin_absolu = os.path.abspath("piece.wav")
    son_ramassage_piece = pygame.mixer.Sound(chemin_absolu)

    son_ramassage_piece.set_volume(0.02)

    # Position initiale de l'avion
    position_x = 400
    position_y = (hauteur - avion_redimensionne.get_height()) // 2

    # Initialisation de l'horloge pour gérer la vitesse de rafraîchissement
    clock = pygame.time.Clock()

    # Drapeaux pour indiquer si les touches sont enfoncées
    gauche_pressee = False
    droite_pressee = False
    haut_pressee = False
    bas_pressee = False

    # Couleur de fond initiale
    couleur_fond = (0, 166, 255)

    # Liste pour stocker les positions des pièces
    positions_pieces = []

    # Nombre aléatoire de pièces entre 5 et 10
    nombre_pieces = random.randint(3, 9)

    compteur_point = 0

    police = pygame.font.Font(None, 30)

    vitesse = 5
    vitessemax = 15
    vitessemin = 0

    NbPxRetourligne = 25

    # Génération des positions aléatoires des pièces
    def Generation_piece():
        global nombre_pieces  # Indiquer que nous allons modifier la variable globale nombre_pieces
        nombre_pieces = random.randint(3, 9)  # Générer un nouveau nombre aléatoire de pièces
        positions_pieces.clear()  # Effacer la liste des positions précédentes
        for _ in range(nombre_pieces):
            x_piece = random.randint(0, largeur - piece_redimensionne.get_width())
            y_piece = random.randint(0, hauteur - piece_redimensionne.get_height())
            # Vérifier s'il y a collision avec une pièce existante
            while any(pygame.Rect(x_piece, y_piece, piece_redimensionne.get_width(), piece_redimensionne.get_height()).colliderect(pygame.Rect(px, py, piece_redimensionne.get_width(), piece_redimensionne.get_height())) for px, py in positions_pieces):
                x_piece = random.randint(0, largeur - piece_redimensionne.get_width())
                y_piece = random.randint(0, hauteur - piece_redimensionne.get_height())
            positions_pieces.append((x_piece, y_piece))
    Generation_piece()  # Générer des pièces au début du jeu

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Appuie touche clavier
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    droite_pressee = True
                elif event.key == pygame.K_LEFT:
                    gauche_pressee = True
                elif event.key == pygame.K_UP:
                    haut_pressee = True
                elif event.key == pygame.K_DOWN:
                    bas_pressee = True
                elif event.key == pygame.K_p:
                    if vitesse < vitessemax:
                        vitesse += 1
                elif event.key == pygame.K_m:
                    if vitesse > vitessemin:
                        vitesse -= 1

            # Relachement touche clavier
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    droite_pressee = False
                elif event.key == pygame.K_LEFT:
                    gauche_pressee = False
                elif event.key == pygame.K_UP:
                    haut_pressee = False
                elif event.key == pygame.K_DOWN:
                    bas_pressee = False

        # Déplacement horizontal
        deplacement_horizontal = 0
        if gauche_pressee:
            deplacement_horizontal -= vitesse
        if droite_pressee:
            deplacement_horizontal += vitesse

        # Déplacement vertical
        deplacement_vertical = 0
        if haut_pressee:
            deplacement_vertical -= vitesse
        if bas_pressee:
            deplacement_vertical += vitesse

        # Mise à jour de la position de l'avion en fonction des déplacements horizontal et vertical
        position_x += deplacement_horizontal
        position_y += deplacement_vertical

        # Gestion de la sortie de l'avion par les bords de l'écran
        if position_x > largeur:  # Si l'avion sort par la droite
            position_x = -avion_redimensionne.get_width()  # Le faire réapparaître à gauche
        elif position_x < -avion_redimensionne.get_width():  # Si l'avion sort par la gauche
            position_x = largeur  # Le faire réapparaître à droite
        if position_y > hauteur:  # Si l'avion sort par le bas
            position_y = -avion_redimensionne.get_height()  # Le faire réapparaître en haut
        elif position_y < -avion_redimensionne.get_height():  # Si l'avion sort par le haut
            position_y = hauteur  # Le faire réapparaître en bas

        # Gestion de l'orientation de l'avion en fonction des touches pressées
        if haut_pressee:
            if droite_pressee:
                angle = -45
            elif gauche_pressee:
                angle = 45
            else:
                angle = 0
        elif bas_pressee:
            if droite_pressee:
                angle = -135
            elif gauche_pressee:
                angle = 135
            else:
                angle = 180
        elif droite_pressee:
            angle = -90
        elif gauche_pressee:
            angle = 90
        else:
            angle = 0

        # Rotation de l'image de l'avion en fonction des touches pressées
        avion_rotation = pygame.transform.rotate(avion_redimensionne, angle)

        # Vérification de la collision entre l'avion et chaque pièce
        pieces_a_supprimer = []
        for i, (x_piece, y_piece) in enumerate(positions_pieces):
            piece_rect = pygame.Rect(x_piece, y_piece, piece_redimensionne.get_width(), piece_redimensionne.get_height())
            avion_rect = pygame.Rect(position_x, position_y, avion_redimensionne.get_width(), avion_redimensionne.get_height())
            if avion_rect.colliderect(piece_rect):
                # Jouer le son lorsque la collision est détectée
                son_ramassage_piece.play()
                # Supprimer la pièce touchée de la liste
                pieces_a_supprimer.append(i)
                # Augmenter le compteur de points
                compteur_point += 100

        # Générer de nouvelles pièces si toutes ont été collectées
        if len(pieces_a_supprimer) == len(positions_pieces):
            Generation_piece()

        # Suppression des pièces qui ont été touchées par l'avion
        for index in sorted(pieces_a_supprimer, reverse=True):
            del positions_pieces[index]

        # Affichage du personnage et mise à jour de l'écran
        fenetre.fill(couleur_fond)
        fenetre.blit(avion_rotation, (position_x, position_y))

        # Affichage des pièces restantes
        for x, y in positions_pieces:
            fenetre.blit(piece_redimensionne, (x, y))



        # Affichage du nombre de pièces collectées
        texte_piece = police.render("Points : " + str(compteur_point), True, (255, 255, 255))  # Texte à afficher avec la couleur blanche
        fenetre.blit(texte_piece, (10, 10))  # Affichage du texte en haut à gauche de la fenêtre

        # Affichage de la vitesse actuelle
        if vitesse == vitessemax:
            couleur_texte = (255, 30, 30)
        elif vitesse == vitessemin:
            couleur_texte = (30, 30, 255)
        else:
            couleur_texte = (255, 255, 255)

        # Affichage du texte de présentation
        texte_presentation = police.render(("Bienvenue dans le jeu de l'avion !"), True, (255, 255, 255))
        fenetre.blit(texte_presentation, (largeur/2-160, 19))
        texte_presentation2 = police.render(("Appuyez sur les flèches directionnelles pour vous déplacer."), True, (255, 255, 255))
        fenetre.blit(texte_presentation2, (largeur/2-280, 19+NbPxRetourligne))

        # Affichage des commandes
        texte_commande1 = police.render("p : vitesse + 1", True, (255, 255, 255))
        fenetre.blit(texte_commande1, (10, 10+NbPxRetourligne))
        texte_commande2 = police.render("m : vitesse - 1", True, (255, 255, 255))
        fenetre.blit(texte_commande2, (10, 10+NbPxRetourligne*2))

        #Affichage de la vitesse
        texte_vitesseactuelle = police.render("Vitesse : " + str(vitesse), True, couleur_texte)
        fenetre.blit(texte_vitesseactuelle, (10, 10+NbPxRetourligne*3))  # Positionnement du texte

        pygame.display.flip()

        # Rafraichissement 70 img/s
        clock.tick(70)

# Gestion des erreurs
except pygame.error as pygame_error:
    print("Erreur pygame :", pygame_error)
    pygame.quit()
    sys.exit()

except Exception as e:
    print("Une erreur inattendue est survenue :", e)
    pygame.quit()
    sys.exit()