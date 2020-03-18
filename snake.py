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
    
    def __init__(self,start,dirnx=0,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 0
        self.dirny = 0
        self.color = color
        
    
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny= dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
        
    
    
    
    def draw (self,surface, eyes=False):
        dis = self.w // self. rows
        i = self.pos[0]
        j= self.pos[1]
        pygame.draw.rect(surface,self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
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
            #
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
            #pour chaque objet on prend leur position et on regarde si elle est
            #dans notre disctionnaire turn
             p= cubeP.pos[:]
             # si p est dans le dictionnaire turn
             if p in self.turn:
                 #20.37#########################################################%
                 turn = self.turn[p]
                 cubeP.move(turn[0], turn[1])
                 if i== len(self.body)-1:
                     self.turn.pop(p)
             else:
                 if cubeP.dirnx == -1 and cubeP.pos[0] <= 0: cubeP.pos = (cubeP.rows-1, cubeP.pos[1])
                 elif cubeP.dirnx == 1 and cubeP.pos[0] >= cubeP.rows-1: cubeP.pos = (0,cubeP.pos[1])
                 elif cubeP.dirny == 1 and cubeP.pos[1] >= cubeP.rows-1: cubeP.pos = (cubeP.pos[0], 0)
                 elif cubeP.dirny == -1 and cubeP.pos[1] <= 0: cubeP.pos = (cubeP.pos[0],cubeP.rows-1)
                 else: cubeP.move(cubeP.dirnx,cubeP.dirny)
                 #########################################################
                 
                 
                 
                 
                 
                 
                     
    def reset (self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        
        
    
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        
        self.body[-1].dirnx=dx
        self.body[-1].dirny=dy
        
        
    
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


    
def randomSnack(rows,item):
    positions= item.body
    
    while True:
        
        x=random.randrange(rows)
        y=random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)    
        
    pass

def message_box(subject, content):
    #On recupères les valeurs globales du code
    global s,body
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    print('score=', len(s.body))
    
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
    vit=10
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
        pygame.time.delay(50)
        #nombre de tick par frame (+ il est grand + c'est rapide)
        clock.tick(vit)   
        s.move()
        if s.body[0].pos == snack.pos:
            #on incrémente la vitesse
            vit=vit+0.5
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))
            
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                vit=10
                s.reset((10,10))
                break 
        #on appel notre fonction en lui donnant une surface (ici Win)     
        redrawWindow(win)

