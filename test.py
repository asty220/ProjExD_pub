import random
import pygame as pg
import sys


class Screen:
    def __init__(self, fn, wh, title):
        #fn:背景画像,wh:高さ、横幅,title:
        pg.display.set_caption(title)
        self.width, self.height=wh   #(1600, 900)
        self.disp = pg.display.set_mode((self.width, self.height)) #surface
        self.rect = self.disp.get_rect()   #rect
        self.image = pg.image.load(fn)

class cursor(pg.sprite.Sprite):
    def __init__(self, fn, r):
        super().__init__()
        self.image = pg.image.load(fn)   #sarface
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect = self.image.get_rect()   #rect
        self.rect.center = pg.mouse.get_pos()   

    def update(self):
        self.rect.center=pg.mouse.get_pos()

class Bomb(pg.sprite.Sprite):
    def __init__(self, fn, r, screen):
        super().__init__()
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
    sc = 0
    time = 0
    
    piclist = ["sozai/0.png","sozai/1.png","sozai/2.png","sozai/3.png","sozai/4.png","sozai/5.png","sozai/6.png","sozai/7.png","sozai/8.png","sozai/9.png","sozai/ぱっちぃ.png"]

    second = 30 #秒表記で管理(三村)
    timeset = second * 144
    
    cursor.containers = pg.sprite.RenderUpdates()
    Bomb.containers = pg.sprite.Group()
    clock = pg.time.Clock()

    screen = Screen("sozai/pg_bg.jpg", (1600,900), "エイム練習")             #スクリーンの生成
    screen.disp.blit(screen.image, (0,0))

    cursors = pg.sprite.Group()                       #照準の描写
    cursors.add(cursor("sozai/nc151920.png", 0.1))

    target = pg.sprite.Group()                #的の描写
    for _ in range(2):
        target.add(Bomb(piclist[random.randint(0,len(piclist)-1)], 1, screen))

    cursors=pg.sprite.Group()                       #照準の描写
    cursors.add(cursor("sozai/nc151920.png",0.1))

    target=pg.sprite.Group()                #的の描写
    for _ in range(2):
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


        if event.type == pg.MOUSEBUTTONDOWN:          #マウスをクリックした際に読み込まれる
            Music("sozai/nc72338.wav")         #音を再生する
            if len(pg.sprite.groupcollide(cursors, target, 0, 1))!=0:             #的に重なっているときに読み込まれる
                    sc+=1                                                       #カーソルと重なっていた的を削除し新しい的を生成する
                    target.add(Bomb(piclist[random.randint(0,len(piclist)-1)], 1, screen))
                    if len(target)<=1:                                          #万が一的が同時に消えてしまった場合に動き的を補充する
                        target.add(Bomb(piclist[random.randint(0,len(piclist)-1)], 1, screen))
        
        font=pg.font.Font(None,30)

        score=font.render(f"score:{str(sc)}", True, "BLACK")
        screen.disp.blit(score, (10,10))

        timelimit=font.render(f"timelimit:{second-time//144}", True, "BLACK")
        screen.disp.blit(timelimit, (10,30))

        pg.display.update()  # 画面の更新
        clock.tick(144)
        time += 1

        if time >= timeset:
            scores(sc)

def scores(sc):      #ゲームオーバー画面を表示するための関数
    
    musiclist = ["sozai/nc211934.wav", "sozai/nc133067.wav", "sozai/nc127260.mp3", "sozai/nc67013.wav", "sozai/nc197899.wav"]
    txtlist = ["GAME OVER", f"Your Score:{sc}!", "Exit:Press 'ESCAPE' key", "Restart:Press 'R' Key"]
    while True:
        pg.display.set_caption("game over")         
        bsc = pg.display.set_mode((1600,900))
        bsc_rect=bsc.get_rect()
        bsc.blit(bsc,bsc_rect)
        
        font=pg.font.Font(None,60)
        for i in range(len(txtlist)):              #文字の表示
            bsc.blit(font.render(txtlist[i], True, "WHITE"), (400,300+60*i))

        key_list = pg.key.get_pressed()           #キー入力に対応した動作
        if key_list[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        if key_list[pg.K_r]:
            Music(musiclist[random.randint(0, len(musiclist)-1)])
            main()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()         # 画面の更新

def start():            #スタート画面の表示
    timecount = 0
    while True:
        pg.display.set_caption("Start")
        bs = pg.display.set_mode((1600,900))
        bsc_rect = bs.get_rect()
        bs.blit(bs,bsc_rect)
        font = pg.font.Font(None,80)
        txt2 ="START!"
        score3=font.render(txt2,True,"WHITE")
        bs.blit(score3,(400,350))

        font1=pg.font.Font(None,60)
        txt4 = "Press 'S' key!"
        score4=font1.render(txt4,True,"WHITE")
        bs.blit(score4,(400,400))

        key_list=pg.key.get_pressed()
        timecount += 1
        if timecount == 144:
            Music("sozai/nc133938.wav")    #スタート時の音声
        if key_list[pg.K_s]:
            main()              #main関数を実行
        pg.display.update()


if __name__ == "__main__":
    pg.init()
    s = pg.mixer.Sound("sozai/フリージア.mp3")
    s.set_volume(0.5)
    s.play(loops=-1)
    start()