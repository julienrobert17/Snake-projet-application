#on importe nos modules
import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init

#objet principal
class cube(object):
    #dimension du tableau
    rows=20
    #taille des blocks
    w= 500
    #initialisation des variables
    def __init__(self,start,dirnx=0,dirny=0,color=(255,0,0)):
        #va servir à tracker la position du block 
        self.pos = start
        #coordonnés du block
        self.dirnx = 0
        self.dirny = 0
        #couleur du block
        self.color = color
        
    
    #track les déplacements
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
        
    
    
    #dessin des yeux pour que seul le premier block les possèdes
    def draw (self,surface, eyes=False):
        dis = self.w // self. rows
        i = self.pos[0]
        j= self.pos[1]
        pygame.draw.rect(surface,self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        if eyes:
            #ecart entre les yeux
            centre = dis//2
            #arrondis les cercles
            radius = 3
            #positionne les yeux
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,250,255), circleMiddle, radius)
            pygame.draw.circle(surface, (0,250,255), circleMiddle2, radius)
                 
                 
                 
#objet principal                
class snake (object):
    #corp du snake dans un tableau
    body=[]
    #class enregistre la direction
    turn= {}
    
    
    def __init__(self,color,pos):
        self.color=color
        self.head=cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
       
    
    def move (self):
        #boucle infini qui va défiler les events et terminer le jeu quand event égal pygame.QUIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
                
            keys= pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
                if keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
                if keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
                if keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
        
        for i, cubeP in enumerate (self.body):
             p= cubeP.pos[:]
             if p in self.turn:
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
                 
                 
                 
                 
                 
                 
                 
    #reset toute les variables pour rejouer
    def reset (self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.vit=10
        
        
    #va ajouter un cube au snake
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        #on va incrémenter le tableau body en fonction de la direction actuel du snake
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        
        #permet au body de suivre le mouvement
        self.body[-1].dirnx=dx
        self.body[-1].dirny=dy
        
        
    #defini la différence de entre le premier block et les suivants
    def draw (self, surface):
        for i, cubeP in enumerate(self.body):
            if i ==0:
                cubeP.draw(surface, True)
            else:
                cubeP.draw(surface)
    
    
#   
def drawGrid (w, rows, surface):
    sizeBtwn= w // rows
    x=0
    y=0
    for l in range (rows):
        x = x + sizeBtwn
        y = y + sizeBtwn 
        pygame.draw.line(surface,(255,255,255),(x,0),(x,w))
        pygame.draw.line(surface,(255,255,255),(0,y),(w,y))
    
    
    
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows,surface)
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
    
    global width, rows, s, snack    
    #on definit nos valeurs de base
    #nombre de colonnes
    rows=20
    width=500
    vit=10
    #on initialise une fenetre pygame(largeur, hauteur)
    win = pygame.display.set_mode((500,500))
    #on initialise notre serpent
    s = snake((0,255,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    
    run= True
    clock = pygame.time.Clock()
    while run :
        
        pygame.time.delay(1)
        clock.tick(vit)   
        s.move()
        if s.body[0].pos == snack.pos:
            vit=vit+0.5
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))
            
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                #imprime le score avec la longueur du snake
                print('Score: ', len(s.body))
                #fonction tkinter 
                message_box('You Lost!', 'Play again...')
                vit=10
                s.reset((10,10))
                break    
        redrawWindow(win)

