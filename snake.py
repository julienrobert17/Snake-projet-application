#on importe nos modules
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import pygame.mixer


# Creer une table
#c.execute('''CREATE TABLE score
 #            (score real)''')

#objet principal
class carre(object):
    ligne=20
    h= 500
    #on initialise les variables positions
    def __init__(self,debut,dirx=0,diry=0,couleur=(255,0,0)):
        self.pos = debut
        self.dirx = 0
        self.diry = 0
        self.couleur = couleur
        
    
    #prend en compte les changements de x et y effectuer dans la class serpent
    def depl(self, dirx, diry):
        #changement de position de x dans class serpent
        self.dirx = dirx
        #changement de position de y dans class serpent
        self.diry= diry
        #changement de position actuel du serpent
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)
        
    
    
    #ajoute au serpent les yeux et définie leurs disgn
    def draw (self,surface, oeil=False):
        dis = self.h // self. ligne
        i = self.pos[0]
        j= self.pos[1]
        pygame.draw.rect(surface,self.couleur, (i*dis+1,j*dis+1,dis-2,dis-2))
        #on ajoute les yeux sur le premier carre uniquement
        if oeil:
            centre = dis//2
            radius = 3
            #mathematiquement on definit la position d'un oeil
            cercleMillieu = (i*dis+centre-radius,j*dis+8)
            #mathematiquement on definit la position de l'autre oeil
            cercleMillieu2 = (i*dis + dis -radius*2, j*dis+8)
            #via une commande pygame on affiche le premier oeil
            pygame.draw.circle(surface, (0,0,0), cercleMillieu, radius)
            #via une commande pygame on affiche le deuxieme oeil
            pygame.draw.circle(surface, (0,0,0), cercleMillieu2, radius)
                 
                 
                 
#objet principal                
class serpent (object):
    #on crée une liste corp
    corp=[]
    #on crée un dictionnaire
    vir= {}
    
    
    def __init__(self,couleur,pos):
        #on définit nos paramètres
        self.couleur=couleur
        #on dit que la tete est egale au carre de la position donnée, celle de depart
        self.tete=carre(pos)
        #classe les corp dans la liste afin u'ils soient bien ordonnés
        self.corp.append(self.tete)
        #on definit des direction en x et en y
        #si diry=1 alors dirx=0 afin qu'on ne bouge que dans une direction
        self.dirx = 0
        self.diry = 1
       
    
    def depl (self):
        #il se passe une commande sur pygame
        for event in pygame.event.get():
            #si on clique sur la croix rouge alors event.type devient pygame QUIT donc:
            if event.type == pygame.QUIT:
                #on quitte pygame
                pygame.quit()
                
            #keys prends la dernière valeur de la touche touchée par l'utilisateur    
            keys= pygame.key.get_pressed()
            
            for key in keys:
                #si la touche fleche gauche est entrée
                #on change les directions selon la touche préssée
                if keys[pygame.K_LEFT]:
                    #
                    self.dirx = -1
                    self.diry = 0
                    #on definit une case a laquelle les cases vont touner
                    #on stock dans le dictionnaire
                    self.vir[self.tete.pos[:]] = [self.dirx, self.diry]
                #si la touche fleche droite est entrée    
                if keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.vir[self.tete.pos[:]] = [self.dirx, self.diry]
                #si la touche fleche du haut est entrée    
                if keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.vir[self.tete.pos[:]] = [self.dirx, self.diry]
                #si la touche fleche du bas est entrée    
                if keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.vir[self.tete.pos[:]] = [self.dirx, self.diry]
                    
        #on regarde dans la liste des positions que l'on a
        #i est l'index et carreP l'objet
        for i, carreP in enumerate (self.corp):
            #pour chaque objet carreP on prend leur position et on regarde si elle est
            #dans notre disctionnaire vir
             p= carreP.pos[:]
             # si p est dans le dictionnaire vir
             if p in self.vir:
                 #on donne a la ou on est la valeur de notre disctionnaire vir
                 #en ce point (la dir x et la dir y)
                 vir = self.vir[p]
                 #notre objet prends ensuite ses dir x et dir y
                 carreP.depl(vir[0], vir[1])
                 #si on est sur le dernier carre
                 if i== len(self.corp)-1:
                     #on enlève le fait de touner de la position sur le terrain
                     #comme ça on évite que le serpent tourne seul en repassant ici
                     self.vir.pop(p)
                     
                 #on verifie si on attein le bord de la map   
             else:
                 #ex: si on bouge a gauche et la position de notre carre est <=0
                 # on change cette position a l'equivalent a droite                 
                 if carreP.dirx == -1 and carreP.pos[0] <= 0: carreP.pos = (carreP.ligne-1, carreP.pos[1])
                 #si on va a droite on est envoyé a gauche
                 elif carreP.dirx == 1 and carreP.pos[0] >= carreP.ligne-1: carreP.pos = (0,carreP.pos[1])
                 #si on va en bas on est envoiyé en haut
                 elif carreP.diry == 1 and carreP.pos[1] >= carreP.ligne-1: carreP.pos = (carreP.pos[0], 0)
                 #si on va en haut on est envoyé en bas
                 elif carreP.diry == -1 and carreP.pos[1] <= 0: carreP.pos = (carreP.pos[0],carreP.ligne-1)
                 #si rien n'est problèmatique le carre se deplace normalement en diry et dirx
                 else: carreP.depl(carreP.dirx,carreP.diry)
                 
                 
                 
                 
                 
                 
                 
                     
    #on réinitialise les variable pour recommencer une partie
    def reset (self,pos):
        self.tete = carre(pos)
        self.corp = []
        self.corp.append(self.tete)
        self.virs = {}
        self.dirx = 0
        self.diry = 1
        
        
    #fonction qui ajoute un carre aux serpents
    def addCarre(self):
        #queue est un carre ajouté derrère
        queue = self.corp[-1]
        #il sont equivalents
        dx, dy = queue.dirx, queue.diry
        #fait apparaitre un carre à une position précise en fonction de la direction du serpent
        if dx == 1 and dy == 0:
            self.corp.append(carre((queue.pos[0]-1,queue.pos[1])))
        elif dx == -1 and dy == 0:
            self.corp.append(carre((queue.pos[0]+1,queue.pos[1])))
        elif dx == 0 and dy == 1:
            self.corp.append(carre((queue.pos[0],queue.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.corp.append(carre((queue.pos[0],queue.pos[1]+1)))
        #le carre que l'on vient d'ajouter prend la direction du serpent
        self.corp[-1].dirx=dx
        self.corp[-1].diry=dy
        
        
    #definie si le carre est ou non la tete du serpent
    def draw (self, surface):
        for i, carreP in enumerate(self.corp):
            #Si il est le premier carre il est dessiné en tant que tete 
            if i ==0:
                carreP.draw(surface, True)
            #Sinon carre normal    
            else:
                carreP.draw(surface)
    
    
    
def drawGrid (h, ligne, surface):
    #on definit la taille entreles lignes de la grille
    # // = quotient de division entier
    ecart= h // ligne
    x=0
    y=0
    #on crée une boucle qui tourne le nombre de fois qu'on a de lignes
    for l in range (ligne):
        #on incrémente x puis y
        x = x + ecart
        y = y + ecart 
        #on dessine les lignes, 2 a chaque tour
        #on choisi une couleur,ici blanc
        #une position de départ ici (x,o) et une position de fin (x,h)
        pygame.draw.line(surface,(255,255,255),(x,0),(x,h))
        #on fait pareil pour l'horizontal 
        pygame.draw.line(surface,(255,255,255),(0,y),(h,y))
    
    
    
def redrawWindow(surface):
    #On recupères les valeurs globales du code
    global ligne, larg, s, snack
    #on mets un fond sur la map
    surface.fill((225, 220, 95))
    s.draw(surface)
    snack.draw(surface)
    #avec pygame on affiche une grille
    drawGrid(larg,ligne,surface)
    #on demande a pygame de mettre a jour l'affichage
    pygame.display.update()


    
#fonction qui fait apparaitre aléatoirement les snacks
def randomSnack(ligne,self):
    #on enregistre dans position le dictionnaire des emplacements actuels du serpent
    positions= self.corp
    
    #crée un boucle tant qu'on a pas break
    while True:
        #randomize la position x et y du snack
        x=random.randrange(ligne)
        y=random.randrange(ligne)
        #vérifie si la position du snack n'est pas celle du serpent
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            #si c'est le cas on reboucle
            continue
        else:
            #sinon on sort de la boucle et on revoie la position x et y du serpent
            break
    return (x,y)    
        
    

def message_box(subject, content):
    #On recupères les valeurs globales du code
    global s,corp
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    #on affiche un message avec un titre et un contenu
    #subject= titre definit plus tot "You Lost!"
    #puis content affiche "play again..."+ le score actuel
    messagebox.showinfo(subject, content + '\nscore = '+str(len(s.corp)))
    
    try:
        #ferme la fenetre
        root.destroy()
        
    except:
        pass
    
    
    
    

if __name__=="__main__":  
    #On recupères les valeurs globales du code
    global larg, ligne, s, snack 
    
    pygame.init
    pygame.mixer.init()

    #on definit nos valeurs de base
    #nombre de colonnes
    ligne=20
    larg=500
    vit=12
    delay=50
    #sound = pygame.mixer.Sound ("C:/Users/cours/Desktop/CPYTHON/musique.OGG")

    #on initialise une fenetre pygame(largeur, hauteur)
    #win prend la valeur de la surface
    win = pygame.display.set_mode((500,500))
    #on initialise notre serpent: couleur et position
    s = serpent((255,0,0), (10,10))
    # le snack prends une position aléatoire et une couleur verte
    snack = carre(randomSnack(ligne, s), couleur=(0,255,0))
    
    #on initialise la variable
    run= True
    #on init a la valeur clock pour recuperer le temps via pygame
    clock = pygame.time.Clock()
    #on lance le son
    #sound.play()
    
    #on crée une boucle
    while run :
        #Permet d'attendre (+ il est grand + c'est lent)
        pygame.time.delay(delay)
        #nombre de tick par frame (+ il est grand + c'est rapide)
        #c'est une limitation du nombre maximal de case/sec de la vitesse du serpent
        clock.tick(vit)   
        s.depl()
        #si la position de la tete du serpent est sur le snack
        if s.corp[0].pos == snack.pos:
            #on incrémente la vitesse
            vit=vit*1.1
            #on decrémente le time delay afin d'augmenter la vitesse du serpent
            #si la longeur modulo 3 =0 seulement afin de ne pas aller trop vite
            if len(s.corp) % 3 ==0:
                if delay > 15:
                    #le delay diminu pour augmenter la vitesse
                    delay=delay -1
            #on lance la fonction addcarre pour grandir
            s.addCarre()
            #on dit a snack de prendre les nouvelles valeurs
            snack = carre(randomSnack(ligne, s), couleur=(0,255,0))
            
        #on verifie pour x valant chaque case de taille du serpent    
        for x in range(len(s.corp)):
            #si la case verifiée est une case prise par le corps de notre serpent
            #on verifie si la postion s.corp[x].pos fait partie de la liste z.pos(liste des postions des cases du serpent)
            # en Commençant a partir de x+1 car sinon on verifie notre propre case et on perds automatiquement
            if s.corp[x].pos in list(map(lambda z:z.pos,s.corp[x+1:])):
                #on prends la valeur de la taille du serpent 
                scoref=len(s.corp)
                #alors on meurt et tkinter affiche le score
                print('Score: ', len(s.corp))       
                message_box('You Lost!', 'Play again...')
                #remise au point de départ des valeurs si le joeur fait rejouer
                vit=12
                delay=50
                s.reset((10,10))
                break 
        #on appel notre fonction en lui donnant une surface (ici Win)     
        redrawWindow(win)

