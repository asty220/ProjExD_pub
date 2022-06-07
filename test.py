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
    def __init__(self, fn, r, screen):
        super().__init__()
        pg.sprite.Sprite.__init__(self,self.containers)
        self.image = pg.image.load(fn)   #sarface
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect = self.image.get_rect()   #rect
        self.rect.center = pg.mouse.get_pos()
        self.rect.centerx = random.randint(20, screen.rect.width-20)
        self.rect.centery = random.randint(20, screen.rect.height-20)

class Music:
    def __init__(self,fn):
        super().__init__()
        pg.mixer.music.load(fn)
        pg.mixer.music.play()

def main():
    global sc,time,musiclist,piclist

    timeset=4320
    cursor.containers=pg.sprite.RenderUpdates()
    Bomb.containers=pg.sprite.Group()
    clock=pg.time.Clock()

    screen=Screen("rensyu06/sozai/pg_bg.jpg",(1600,900),"エイム練習")             #スクリーンの生成
    screen.disp.blit(screen.image, (0,0))

    cursors=pg.sprite.Group()                       #照準の描写
    cursors.add(cursor("rensyu06/sozai/nc151920.png",0.1,pg.mouse.get_pos))

    target=pg.sprite.Group()                #的の描写
    for _ in range(100):
        target.add(Bomb(piclist[random.randint(0,len(piclist)-1)],1,screen))
    

    while True:
        screen.disp.blit(screen.image, (0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.mouse.set_visible(False)

        target.update(screen)        #的の描写
        target.draw(screen.disp)

        cursors.update()         #照準の描写
        cursors.draw(screen.disp)


        if event.type==pg.MOUSEBUTTONDOWN:          #マウスをクリックした際に読み込まれる
            Music("rensyu06/sozai/nc72338.wav")         #音を再生する
            if len(pg.sprite.groupcollide(cursors,target,0,1))!=0:             #的に重なっているときに読み込まれる
                    sc+=1                                                       #カーソルと重なっていた的を削除し新しい的を生成する
                    target.add(Bomb(piclist[random.randint(0,len(piclist)-1)],1,screen))
                    if len(target)<=1:                                          #万が一的が同時に消えてしまった場合に動き的を補充する
                        target.add(Bomb(piclist[random.randint(0,len(piclist)-1)],1,screen))
        
        font=pg.font.Font(None,30)
        score=font.render(f"score:{str(sc)}",True,"BLACK")
        screen.disp.blit(score,(10,10))
        timelimit=font.render(f"timelimit:{timeset//144-time//144}",True,"BLACK")
        screen.disp.blit(timelimit,(10,30))
        pg.display.update()  # 画面の更新
        clock.tick(144)
        time+=1

        if time>=timeset:
            scores()

def scores():      #ゲームオーバー画面を表示するための関数
    global time,sc,musiclist
    txtlist=[f"GAME OVER",f"Your Score:{sc}!",f"Exit:Press 'ESCAPE' key",f"Restart:Press 'R' Key"]
    while True:
        pg.display.set_caption("game over")         
        bsc=pg.display.set_mode((1600,900))
        bsc_rect=bsc.get_rect()
        bsc.blit(bsc,bsc_rect)
        font=pg.font.Font(None,60)

        for i in range(len(txtlist)):              #文字の表示
            bsc.blit(font.render(txtlist[i],True,"WHITE"),(400,300+60*i))

        key_list=pg.key.get_pressed()           #キー入力に対応した動作
        if key_list[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        if key_list[pg.K_r]:
            if time>=1:
                time=0
                sc=0
            Music(musiclist[random.randint(0,len(musiclist)-1)])
            main()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()         # 画面の更新

def start():            #スタート画面の表示
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
            Music("rensyu06/sozai/nc133938.wav")    #スタート時の音声
        if key_list[pg.K_s]:
            main()              #main関数を実行
        pg.display.update()


if __name__ == "__main__":
    sc=0
    time=0
    musiclist=["rensyu06/sozai/nc211934.wav","rensyu06/sozai/nc133067.wav","rensyu06/sozai/nc127260.mp3","rensyu06/sozai/nc67013.wav","rensyu06/sozai/nc197899.wav"]
    piclist=["rensyu06/sozai/0.png","rensyu06/sozai/1.png","rensyu06/sozai/2.png","rensyu06/sozai/3.png","rensyu06/sozai/4.png","rensyu06/sozai/5.png","rensyu06/sozai/6.png","rensyu06/sozai/7.png","rensyu06/sozai/8.png","rensyu06/sozai/9.png","rensyu06/sozai/ぱっちぃ.png"]
    pg.init() 
    s=pg.mixer.Sound("rensyu06/sozai/フリージア.mp3")
    s.set_volume(0.5)
    s.play(loops=-1)
    start()