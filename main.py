import pygame
import random
from sys import exit


class enemies:
    def __init__(self,freq,pos): 

        #Freq = frequence de mouvement des enemies (inutilisé actuellement)
        self.freq = freq 

        #Pos = la position de l'enemie actuel (quelle piece)
        self.pos = pos

    #on attribut un nouvelle position a l'ennemie
    def posChange(self,newPos):
        self.pos = newPos

    #ici on bouge l'ennemie de piece de maniere aléatoire
    def roomChange(self):

        #on attribut directement la position actuelle a une variable pour rendre le code plus claire
        posNow = self.pos

        #on utilise posChange pour modifier la position de l'ennemie a 'aide d'un dictionnaire
        #qui contient les differentes liaisons entre chaque pieces
        self.posChange(room[posNow][random.randint(0,len(room[posNow])-1)])
        return self.pos


#On créer chaqu'une des images avec une classe pour que le programme
# qui faittourner le jeux soit plus lisible
class Images:
    def __init__(self, image, sizes):
        
        #donc on charge l'image
        self.image = pygame.image.load(image)

        #puis on ajuste la taille
        self.image = pygame.transform.scale(self.image, sizes)


#creer une classe pour l'ouverture et la fermeture des portes
#sert a avoir un code plus lisible
class Door:
    def __init__(self):

        #en gros on a si la porte s'ouvre(self.open), si elle se ferme(self.close) et sa position(self.pos(si elle est ouverte ou non))
        self.close = 0
        self.open = 0
        self.pos = -1000
    def closing(self):

        #donc si elle se ferme en gros on met self.close = 5 et du coup pour les 5 prochain     
        #rafraichissement la porte va baisser (et du coup on enleve 1 a self.close pour avoir une condition d'arret)                                        
        if self.close != 0:
            self.pos += 200
            self.close -= 1

    #ici on fait la meme pour l'ouverture
    def opening(self):
        if self.open != 0:
            self.pos -= 200
            self.open -= 1

DoorLStat = Door()
DoorRStat = Door()

#on a un tableau basé sur le principe de matrice avec chaque item étant la piece actuelle et les pieces liées
room = {"R1":["R2","R3"],
        "R2":["R1","R3","R4"],
        "R3":["R1","R2"],
        "R4":["R2"]
        }

#on definie la fonction qui fait tourner le programme (en mode java ouuuuuu)
def main():

    #on créer la fenetre
    screen = pygame.display.set_mode((1000,750))
    clock = pygame.time.Clock()

    #on définie des variables qui vont décider des mouvement. On a ImagePos pour ou le joueur regarde,
    #LightsOff pour les lumiere et DoorTimer pour le temps que les portes se ferment
    LightsLOff = 1
    LightsROff = 1
    DoorLTimer = 0
    DoorRTimer = 0
    ImagePos = -375

    #la on choisi les image a charger (donc le bureau et les portes etc...)
    Office = Images("Office.png", (1750, 750))
    DoorL = Images("DoorL.png", (1750, 750))
    DoorR = Images("DoorR.png", (1750, 750))
    NoLLights = Images("NoLLights.png", (1750, 750))
    NoRLights = Images("NoRLights.png", (1750, 750))
    Background = Images("Background.png", (1750, 750))

    #on définie le nom de la fenetre
    pygame.display.set_caption('Un Quinté de Lune chez Frederick B.')
    
    running = True

    #ici, tant que running = True on a le jeu qui tourne
    while running:
        for event in pygame.event.get():

            #mais si l'evenement QUIT occure, aka on clique sur la croix de la fenetre
            #running prend la valeur false et on arrete le programme.
            if event.type == pygame.QUIT:
                running = False
                exit()

        #ça c'est juste histoire de refresh la page
        screen.fill("lime")

        #MousePos renvoie la position de la souris
        MousePos = pygame.mouse.get_pos()

        #et MouseClique renvoie si la souris clique ou pas (duh)
        MouseClick = pygame.mouse.get_pressed()

        #Ici on verifie la position de la souris pour pouvoir cliquer sur chaqu'un des deux boutons pour fermer la porte
        if MouseClick[0] == True and DoorLStat.pos == -1000 and MousePos[1] > 400 and MousePos[1] < 450 and MousePos[0] > 35 and MousePos[0] < 85:

            #donc on change la valeur de DoorLStat.close pour plus tard appeler la methode qui va fermer la porte etape par etape
            DoorLStat.close = 5

            #et on augmente le timer qui va diminuer afin de reouvrir la porte au bout d'un certain temps
            DoorLTimer = 120


        #ici on verifie la souris pour la lmumiere
        elif MouseClick[0] == True and MousePos[1] > 535 and MousePos[1] < 585 and MousePos[0] > 35:

            #si on est entrain de cliquer sur le bouton, LightsLOff = -1 donc elle est allumé
            LightsLOff = -1
                
        else:

            #sinon = 1 et elle s'eteint a nouveau
            LightsLOff = 1
        


        #ici c'est la meme mais pour la droite
        if MouseClick[0] == True and DoorRStat.pos == -1000 and MousePos[1] > 400 and MousePos[1] < 450 and MousePos[0] < 965 and MousePos[0] > 910:
            DoorRStat.close = 5
            DoorRTimer = 120
            
        elif MouseClick[0] == True and MousePos[1] > 535 and MousePos[1] < 585 and MousePos[0] < 965:
            LightsROff = -1
                
        else:
            LightsROff = 1 


        #en gros on va suivre la souris a l'opposé afin de bouger la camera dans le sens ou la souris va
        if MousePos[0] < 875 and MousePos[0] > 125:

            #ici c'est juste histoire d'avoir un pas de 5 parceque j'avais envie mdr
            ImagePos = (-MousePos[0]+125)//5*5

        #et la c'est pour que lorsqu'on est au bon endroit la cam se fixe au bon point
        #parceque sinon la cam se bloquait avant d'etre au bord de la fenetre
        elif MousePos[0] >= 875:
            ImagePos = -745
        elif MousePos[0] <= 125:
            ImagePos = 0


        #ici, si le timer est different de 0 on le decremente a chaque tour de boucle pour creer un vrai timer
        if DoorLTimer != 0:
            DoorLTimer -= 1

        #lorsqu'il est egale a 0 (et que la porte est fermer) on change DoorLStat.open pour lancer l'ouverture de la porte
        elif DoorLTimer == 0 and DoorLStat.pos == 0:
            DoorLStat.open = 5
        
        #ici c'est pareil pour la porte de droite
        if DoorRTimer != 0:
            DoorRTimer -= 1
        elif DoorRTimer == 0 and DoorRStat.pos == 0:
            DoorRStat.open = 5
        

        #on appel les fonctions pour fla fermeture ou l'ouverture des portes
        DoorLStat.closing()
        DoorRStat.closing()
        DoorLStat.opening()
        DoorRStat.opening()


        #en gros blit sers a decider de la position de l'image, mais selon l'ordre
        #dans lequel on blit les images ça va decider de quels images et au dessus de l'autre
        screen.blit(Background.image,(ImagePos, 0))
        if LightsLOff == 1:
            screen.blit(NoLLights.image,(ImagePos, 0))
        if LightsROff == 1:
            screen.blit(NoRLights.image,(ImagePos, 0))
        screen.blit(DoorL.image,(ImagePos, DoorLStat.pos))
        screen.blit(DoorR.image,(ImagePos, DoorRStat.pos))
        screen.blit(Office.image,(ImagePos, 0))
            
        #flip c'est juste pour afficher tout notre bordel
        pygame.display.flip()
        #et ça c'est juste pour dire que notre jeu tourner a 60fps  
        clock.tick(60)        


#enfin, si notre projet s'appel "main" on lance le programme, c'est juste histoire d'avoir
#une condition qui sera forcement vrai pour pouvoir demarrer la fonction main
#et du coup oui main c'est le nom du code mais aussi de la fonction principale (celle ligne 33)
if __name__ == '__main__':
    pygame.init()
    main()                                             
    pygame.quit()
    

#TODO:
#	Ecran plus près pour affichage


#	Ennemies qui bouge
#	Detcteur de mouvements (couloire brille rouge)


#	Tache a accomplir
#	Porte nombre d'usage limité (a recharger avec les tache)
#	PTS de colmpetences (ameliorer la vitesse des taches et de rechargement des portes)
#	LightsROff ne marche pas, a reparer