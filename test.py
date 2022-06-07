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
        self.surface = pg.Surface(wh) #imageとは別のsurfaceを生成(熊田)


class cursor(pg.sprite.Sprite):
    def __init__(self, fn, r):
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
    global time, sc

    max_tar = 2 #表示する的の数(熊田)
    timeset = 288
    cursor.containers=pg.sprite.RenderUpdates()
    Bomb.containers=pg.sprite.Group()
    clock=pg.time.Clock()

    screen=Screen("ProjExD_pub/sozai/pg_bg.jpg",(1600,900),"エイム練習")             #スクリーンの生成
    screen.disp.blit(screen.image, (0,0))

    cursors=pg.sprite.Group()                       #照準の描写
    cursors.add(cursor("ProjExD_pub/sozai/nc151920.png",0.1))

    target=pg.sprite.Group()                #的の描写
    for _ in range(max_tar):
        target.add(Bomb(pic_list[random.randint(0,len(pic_list)-1)],1,screen))
    
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


        if event.type == pg.MOUSEBUTTONDOWN:          #マウスをクリックした際に読み込まれる
            Music("ProjExD_pub/sozai/nc72338.wav")         #音を再生する
            if len(pg.sprite.groupcollide(cursors,target,0,1))!=0:             #的に重なっているときに読み込まれる
                    sc += 1                                                       
                    target.add(Bomb(pic_list[random.randint(0,len(pic_list)-1)],1,screen)) #カーソルと重なっていた的を削除し新しい的を生成する
                    if len(target) <= 1:                                          #万が一的が同時に消えてしまった場合に動き的を補充する
                        target.add(Bomb(pic_list[random.randint(0,len(pic_list)-1)],1,screen))
        
        font=pg.font.Font(None,30)
        score=font.render(f"score:{str(sc)}",True,"BLACK")
        screen.disp.blit(score,(10,10))
        timelimit=font.render(f"timelimit:{timeset//144-time//144}",True,"BLACK")
        screen.disp.blit(timelimit,(10,30))
        pg.display.update()  # 画面の更新
        clock.tick(144)
        time += 1

        if time>=timeset:
            scores()

def scores():      #ゲームオーバー画面を表示するための関数
    global time,sc
    txtlist = ["GAME OVER",f"Your Score:{sc}!","Exit:Press 'ESCAPE' key","Restart:Press 'R' Key"]

    while True:
        score_screen = Screen("ProjExD_pub/sozai/pg_bg.jpg", (1600, 900), ("game over")) #Screenクラスを用いてscoreのスクリーンを表示(熊田)
        score_screen.disp.blit(score_screen.surface,score_screen.rect)
        font=pg.font.Font(None,60)

        for i in range(len(txtlist)):              #文字の表示
            score_screen.disp.blit(font.render(txtlist[i],True,"WHITE"),(400,300+60*i))

        key_list = pg.key.get_pressed()           #キー入力に対応した動作
        if key_list[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        if key_list[pg.K_r]:
            if time >= 1:
                time = 0
                sc = 0
            Music(music_list[random.randint(0,len(music_list)-1)])
            main()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()         # 画面の更新

def start():            #スタート画面の表示
    timecount = 0

    while True:
        start_screen = Screen("ProjExD_pub/sozai/pg_bg.jpg", (1600, 900), "Start")
        #pg.display.set_caption("Start")
        #bs=pg.display.set_mode((1600,900))
        #bsc_rect=bs.get_rect()
        #bs.blit(bs,bsc_rect)
        font = pg.font.Font(None,80)
        font1 = pg.font.Font(None,60)
        txt2 = "START!"
        txt4 = "Press 'S' key!"
        score3 = font.render(txt2,True,"WHITE")
        start_screen.disp.blit(score3,(400,350))
        score4=font1.render(txt4,True,"WHITE")
        start_screen.disp.blit(score4,(400,400))
        key_list=pg.key.get_pressed()
        timecount += 1
        if timecount == 144:
            Music("ProjExD_pub/sozai/nc133938.wav")    #スタート時の音声
        if key_list[pg.K_s]:
            main()              #main関数を実行
        pg.display.update()


if __name__ == "__main__":
    sc = 0
    time = 0
    music_list = ["ProjExD_pub/sozai/nc211934.wav","ProjExD_pub/sozai/nc133067.wav","ProjExD_pub/sozai/nc127260.mp3","ProjExD_pub/sozai/nc67013.wav","ProjExD_pub/sozai/nc197899.wav"]
    pic_list = ["ProjExD_pub/sozai/0.png","ProjExD_pub/sozai/1.png","ProjExD_pub/sozai/2.png","ProjExD_pub/sozai/3.png","ProjExD_pub/sozai/4.png","ProjExD_pub/sozai/5.png","ProjExD_pub/sozai/6.png","ProjExD_pub/sozai/7.png","ProjExD_pub/sozai/8.png","ProjExD_pub/sozai/9.png","ProjExD_pub/sozai/ぱっちぃ.png"]
    pg.init() 
    sound = pg.mixer.Sound("ProjExD_pub/sozai/フリージア.mp3")
    sound.set_volume(0.5)
    sound.play(loops=-1)
    start()