import pygame
pygame.init()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First game")

screenWidth=500
x= 250
y = 250
width = 20
height = 20
vel=5

run = True
while run:
    
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys= pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:
        x-= vel
    if keys[pygame.K_RIGHT] and x< screenWidth-width-vel:
        x+= vel
    if keys[pygame.K_UP] and y > vel:
        y -=vel
    if keys[pygame.K_DOWN]and y< screenWidth-height-vel:
        y+= vel
        
    win.fill((0,0,0))    
    pygame.draw.rect(win, (0,255,0),(x, y, width, height)) 
    pygame.display.update()
            
            
pygame.quit()            

baptiste TTT