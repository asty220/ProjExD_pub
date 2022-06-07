import random
import pygame as pg
import sys


class Screen:
    def __init__(self,fn,wh,title):
        #fn:背景画像,wh:高さ、横幅,title:
        pg.display.set_caption(title)
        self.width, self.height=wh   #(1600, 900)
        self.disp = pg.display.set_mode((self.width, self.height)) #surface
        self.rect = self.disp.get_rect()   #rect
        self.image = pg.image.load(fn)

class cursor(pg.sprite.Sprite):

    def __init__(self, fn, r, xy):
        super().__init__()
        pg.sprite.Sprite.__init__(self,self.containers)
        self.image = pg.image.load(fn)   #sarface
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect = self.image.get_rect()   #rect
        self.rect.center = pg.mouse.get_pos()   

    def update(self):
        self.rect.center=pg.mouse.get_pos()



class Bomb(pg.sprite.Sprite):
    def __init__(self,cl,x,haya,screen):
        super().__init__()
        pg.sprite.Sprite.__init__(self,self.containers)
        self.image = pg.Surface((2*x,2*x))
        self.image.set_colorkey((0,0,0))
        pg.draw.circle(self.image, cl, (x,x), x)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(20, screen.rect.width-20)
        self.rect.centery = random.randint(20, screen.rect.height-20)

class Music:
    def __init__(self,fn,x=0,y=2):
        super().__init__()
        pg.mixer.music.load(fn)
        pg.mixer.music.play()

def main():
    global sc,time

    timeset=4320
    cursor.containers=pg.sprite.RenderUpdates()
    Bomb.containers=pg.sprite.Group()
    clock=pg.time.Clock()

    screen=Screen("rensyu05/fig/pg_bg.jpg",(1600,900),"エイム練習")
    screen.disp.blit(screen.image, (0,0))

    cursors=pg.sprite.Group()
    cursors.add(cursor("rensyu06/sozai/nc151920.png",0.1,pg.mouse.get_pos))

    target=pg.sprite.Group()
    for _ in range(2):
        target.add(Bomb((255,0,0),10,(2,2),screen))

    while True:
        screen.disp.blit(screen.image, (0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.mouse.set_visible(False)

        target.update(screen)
        target.draw(screen.disp)

        cursors.update()
        cursors.draw(screen.disp)

        if event.type==pg.MOUSEBUTTONDOWN:
            Music("rensyu06/sozai/nc72338.wav")
            if len(pg.sprite.groupcollide(cursors,target,0,1))!=0:
                    sc+=1
                    target.add(Bomb((255,0,0),10,(2,2),screen))
        
        font=pg.font.Font(None,30)
        score=font.render(f"score:{str(sc)}",True,"BLACK")
        screen.disp.blit(score,(10,10))
        font=pg.font.Font(None,30)
        timelimit=font.render(f"timelimit:{timeset/144-time//144}",True,"BLACK")
        screen.disp.blit(timelimit,(10,30))
        pg.display.update()  # 画面の更新
        clock.tick(144)
        time+=1
        if time>=timeset:
            scores()

def scores():      #ゲームオーバー画面を表示するための関数
    global time,sc
    while True:
        pg.display.set_caption("game over")
        bsc=pg.display.set_mode((1600,900))
        bsc_rect=bsc.get_rect()
        bsc.blit(bsc,bsc_rect)
        font=pg.font.Font(None,60)
        txt2=f"GAME OVER"
        score3=font.render(txt2,True,"WHITE")
        bsc.blit(score3,(400,350))
        txt=f"Your Score:{sc}!"
        score=font.render(txt,True,"WHITE")
        bsc.blit(score,(400,410))
        txt1=f"Exit:Press 'ESCAPE' key"
        score1=font.render(txt1,True,"WHITE")
        bsc.blit(score1,(400,460))
        txt3=f"Restert:Press 'R' Key"
        score3=font.render(txt3,True,"WHITE")
        bsc.blit(score3,(400,510))
        key_list=pg.key.get_pressed()
        if key_list[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        if key_list[pg.K_r]:
            if time>=1:
                time=0
                sc=0
            Music("rensyu06/sozai/nc211934.wav")
            main()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()

def start():
    timecount=0
    while True:
        pg.display.set_caption("Start")
        bs=pg.display.set_mode((1600,900))
        bsc_rect=bs.get_rect()
        bs.blit(bs,bsc_rect)
        font=pg.font.Font(None,80)
        font1=pg.font.Font(None,60)
        txt2=f"START!"
        txt4=f"Press 'S' key!"
        score3=font.render(txt2,True,"WHITE")
        bs.blit(score3,(400,350))
        score4=font1.render(txt4,True,"WHITE")
        bs.blit(score4,(400,400))
        key_list=pg.key.get_pressed()
        timecount+=1
        if timecount==144:
            Music("rensyu06/sozai/nc133938.wav")
        if key_list[pg.K_s]:
            main()
        pg.display.update()


if __name__ == "__main__":
    sc=0
    time=0
    pg.init() 
    start()


