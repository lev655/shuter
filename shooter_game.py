from pygame import * 
from random import randint 
from time import time as timer 

lifes = 3
monsters_killed = 0

font.init()
font_life = font.SysFont('Impact', 48) 

font_killed = font.SysFont('Impact', 48)



class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, x_speed = 3): 
        sprite.Sprite.__init__(self) 
        self.image = transform.scale(image.load(player_image),(size_x, size_y)) 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
        self.x_speed = x_speed   
        self.rel = False 
        self.reltime = 0 
        self.t = 0 
 
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y)) 
 
    def update(self): 
        keys = key.get_pressed() 
        if keys[K_LEFT] and self.rect.x > 0: 
            self.x_speed = -10 
            self.rect.x += self.x_speed 
 
        if keys[K_RIGHT] and self.rect.x < 650: 
            self.x_speed = 10 
            self.rect.x += self.x_speed 
 
        if keys[K_SPACE]: 
            if self.reltime < 1 and self.rel == False: 
                        self.reltime = self.reltime + 1 
                        pule = GameSprite("bullet.png", self.rect.centerx, self.rect.centery, 20, 20) 
                        pules.add(pule) 
            if self.reltime  >= 1 and self.rel == False : #если игрок сделал 5 выстрелов 
                    self.t = timer() #засекаем время, когда это произошло 
                    self.rel = True #ставим флаг перезарядки 
 
        if self.rel == True: 
           now_time = timer() #считываем время 
        
           if now_time - self.t < 0.1: #пока не прошло 3 секунды выводим информацию о перезарядке 
               pass 
           else: 
               self.reltime = 0   #обнуляем счётчик пуль 
               self.rel = False #сбрасываем флаг перезарядки 
 
 
 
    def update_enemy(self): 
        self.rect.y += self.x_speed 
        if self.rect.y > 500: 
            self.rect.x = randint(0, 620) 
            self.rect.y = 0  
            self.x_speed = randint(5, 8) 
 
    def update_bullet(self): 
        self.rect.y -= 15 
        if self.rect.y < -20: 
            self.kill() 

 
rocket = GameSprite("rocket.png", 300,350,90,110) 
pule = GameSprite("bullet.png", rocket.rect.centerx, rocket.rect.centery, 20, 20) 
 
pules = sprite.Group() 
 
 
monsters = sprite.Group() 
for i in range(1, 6): 
    monster = GameSprite('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 7)) 
    monsters.add(monster) 
 
 
window = display.set_mode((700, 500)) 
display.set_caption('Шутер') 
 
background = transform.scale(image.load("galaxy.jpg"),(700, 500)) 
 
game = True 
while game: 
    for e in event.get(): 
        if e.type == QUIT: 
            game = False 
    rocket.update() 
 
    for m in monsters: 
        m.update_enemy() 
 
    for p in pules: 
        p.update_bullet() 
 

    if sprite.spritecollide(rocket, monsters, True ):
        lifes -= 1
        monsters.add(monster)
    
    if lifes < 0:
        game = False

    if sprite.groupcollide(pules, monsters, True, True):
        monsters_killed += 1
        monster = GameSprite('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 7)) 
        monsters.add(monster)
        
    

    window.blit(background,(0, 0)) 
    
    text_life = font_life.render('Жизни:'+ str(lifes), 1, (255,255, 255))
    window.blit(text_life, (10, 20))

    text_killed = font_killed.render('Убитые враги:' + str(monsters_killed), 1, (255, 255, 255) )
    window.blit(text_killed, (300, 20))


    monsters.draw(window) 
    rocket.reset() 
 
    pules.draw(window) 
    
    display.update() 
    time.delay(52)
