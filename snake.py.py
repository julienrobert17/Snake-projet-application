#on importe nos modules
import random
import pygame
import tkinter as tk
from tkinter import messagebox
pygame.init


#objet principal
class cube(object):
    rows=20
    w= 500
    #on initialise les variables positions
    def __init__(self,start,dirnx=0,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 0
        self.dirny = 0
        self.color = color
        
    
    #prend en compte les changements de x et y effectuer dans la class snake
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny= dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
        
    
    
    #ajoute au snake les yeux et définie leurs disgn
    def draw (self,surface, eyes=False):
        dis = self.w // self. rows
        i = self.pos[0]
        j= self.pos[1]
        pygame.draw.rect(surface,self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        #on ajoute les yeux sur le premier cube uniquement
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
                 
                 
                 
#objet principal                
class snake (object):
    #on crée une liste body
    body=[]
    #on crée un dictionnaire
    turn= {}
    
    
    def __init__(self,color,pos):
        #on définit nos paramètres
        self.color=color
        #on dit que la tete est egale au cube de la position donnée, celle de depart
        self.head=cube(pos)
        #classe les body dans la liste afin u'ils soient bien ordonnés
        self.body.append(self.head)
        #on definit des direction en x et en y
        #si dirny=1 alors dirnx=0 afin qu'on ne bouge que dans une direction
        self.dirnx = 0
        self.dirny = 1
       
    
    def move (self):
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
                    self.dirnx = -1
                    self.dirny = 0
                    #on definit une case a laquelle les cases vont touner
                    #on stock dans le dictionnaire
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
                #si la touche fleche droite est entrée    
                if keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
                #si la touche fleche du haut est entrée    
                if keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
                #si la touche fleche du bas est entrée    
                if keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
        #on regarde dans la liste des positions que l'on a
        #i est l'index et cubeP l'objet
        for i, cubeP in enumerate (self.body):
            #pour chaque objet cubeP on prend leur position et on regarde si elle est
            #dans notre disctionnaire turn
             p= cubeP.pos[:]
             # si p est dans le dictionnaire turn
             if p in self.turn:
                 #on donne a la ou on est la valeur de notre disctionnaire turn
                 #en ce point (la dirn x et la dirn y)
                 turn = self.turn[p]
                 #notre objet prends ensuite ses dirn x et dirn y
                 cubeP.move(turn[0], turn[1])
                 #si on est sur le dernier cube
                 if i== len(self.body)-1:
                     #on enlève le fait de touner de la position sur le terrain
                     #comme ça on évite que le snake tourne seul en repassant ici
                     self.turn.pop(p)
                     
                 #on verifie si on attein le bord de la map   
             else:
                 #ex: si on bouge a gauche et la position de notre cube est <=0
                 # on change cette position a l'equivalent a droite                 
                 if cubeP.dirnx == -1 and cubeP.pos[0] <= 0: cubeP.pos = (cubeP.rows-1, cubeP.pos[1])
                 #si on va a droite on est envoyé a gauche
                 elif cubeP.dirnx == 1 and cubeP.pos[0] >= cubeP.rows-1: cubeP.pos = (0,cubeP.pos[1])
                 #si on va en bas on est envoiyé en haut
                 elif cubeP.dirny == 1 and cubeP.pos[1] >= cubeP.rows-1: cubeP.pos = (cubeP.pos[0], 0)
                 #si on va en haut on est envoyé en bas
                 elif cubeP.dirny == -1 and cubeP.pos[1] <= 0: cubeP.pos = (cubeP.pos[0],cubeP.rows-1)
                 #si rien n'est problèmatique le cube se deplace en dirny et dirnx
                 else: cubeP.move(cubeP.dirnx,cubeP.dirny)
                 
                 
                 
                 
                 
                 
                 
    #on réinitialise les variable pour recommencer une partie
    def reset (self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        
        
    #fonction qui ajoute un cube aux serpents
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        #fait apparaitre un cube à une position précise en fonction de la direction du snake
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        #le cube que l'on vient d'ajouter prend la direction du snake
        self.body[-1].dirnx=dx
        self.body[-1].dirny=dy
        
        
    #definie si le cube est ou non la tete du snake
    def draw (self, surface):
        for i, cubeP in enumerate(self.body):
            if i ==0:
                cubeP.draw(surface, True)
            else:
                cubeP.draw(surface)
    
    
    
def drawGrid (w, rows, surface):
    #on definit la taille entreles lignes de la grille
    # // = quotient de division entier
    sizeBtwn= w // rows
    x=0
    y=0
    #on crée une boucle qui tourne le nombre de fois qu'on a de lignes
    for l in range (rows):
        #on incrémente x puis y
        x = x + sizeBtwn
        y = y + sizeBtwn 
        #on dessine les lignes, 2 a chaque tour
        #on choisi une couleur,ici blanc
        #une position de départ ici (x,o) et une position de fin (x,w)
        pygame.draw.line(surface,(255,255,255),(x,0),(x,w))
        pygame.draw.line(surface,(255,255,255),(0,y),(w,y))
    
    
    
def redrawWindow(surface):
    #On recupères les valeurs globales du code
    global rows, width, s, snack
    #on mets un fond noir sur la fenetre
    surface.fill((10,180,80))
    s.draw(surface)
    snack.draw(surface)
    #avec pygame on affiche une grille
    drawGrid(width,rows,surface)
    #on demande a pygame de mettre a jour l'affichage
    pygame.display.update()


#fonction qui fait apparaitre aléatoirement les snacks
def randomSnack(rows,item):
    positions= item.body
    
    #crée un boucle tant qu'on a pas break
    while True:
        #randomize la position x et y du snack
        x=random.randrange(rows)
        y=random.randrange(rows)
        #vérifie si la position du snack n'est pas celle du snake
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            #si c'est le cas on reboucle
            continue
        else:
            #sinon on sort de la boucle et on revoie la position x et y du snake
            break
    return (x,y)    
        
    pass

def message_box(subject, content):
    #On recupères les valeurs globales du code
    global s,body
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    #on affiche un message avec un titre et un contenu
    messagebox.showinfo(subject, content + '\nscore = '+str(len(s.body)))
    
    try:
        root.destroy()
        
    except:
        pass
    
    
    
    

if __name__=="__main__":  
    #On recupères les valeurs globales du code
    global width, rows, s, snack 
    #on definit nos valeurs de base
    #nombre de colonnes
    rows=20
    width=500
    vit=12
    delay=50
    

    #on initialise une fenetre pygame(largeur, hauteur)
    #win prend la valeur de la surface
    win = pygame.display.set_mode((500,500))
    #on initialise notre serpent: couleur et position
    s = snake((255,0,0), (10,10))
    
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    #on crée une boucle
    run= True
    #on init a la valeur 
    clock = pygame.time.Clock()
    while run :
        #Permet d'attendre (+ il est grand + c'est lent)
        pygame.time.delay(delay)
        #nombre de tick par frame (+ il est grand + c'est rapide)
        clock.tick(vit)   
        s.move()
        if s.body[0].pos == snack.pos:
            #on incrémente la vitesse
            vit=vit*1.1
            #on decrémente le time delay afin d'augmenter la vitesse du serpent
            #si lalongeur modulo 3 =0 seulement afin de ne pas aller trop vite
            if len(s.body) % 3 ==0:
                if delay > 15:
                    delay=delay -1
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))
        #on verifie pour x valant chaque case de taille du snake    
        for x in range(len(s.body)):
            #si la case verifiée est une case prise par le corps de notre serpent
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                #alors on meurt et tkinter affiche le score
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                #remise a 0 des valeurs si le joeur fait rejouer
                vit=12
                delay=50
                s.reset((10,10))
                break 
        #on appel notre fonction en lui donnant une surface (ici Win)     
        redrawWindow(win)

