import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数で与えられたrctが画面の仲か外かを判定する
    引数：こうかとんrctか爆弾rct
    戻り値：真理値タプル（横、縦）/画面内：True,画面外：False
    """
    yoko,tate = True,True
    if rct.left <0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

def gameover(screen: pg.Surface) -> None:
    """
    こうかとんに爆弾が接触した際にゲームオーバー画面を表示させる
    引数：screenのSurface
    戻り値：なし

    """
    sikaku = pg.Surface((1100,650))
    pg.draw.rect(sikaku, 0,pg.Rect(0,0,1100,650))
    sikaku.set_alpha(200)
    screen.blit(sikaku,[0,0])
    
    kknaki_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0,0.9)
    kknaki_rct = kknaki_img.get_rect()
    kknaki_rct.center = (WIDTH/2)+200,HEIGHT/2
    screen.blit(kknaki_img, kknaki_rct)
    kknaki2_rct = kknaki_img.get_rect()
    kknaki2_rct.center = (WIDTH/2)-200,HEIGHT/2
    screen.blit(kknaki_img, kknaki2_rct)
    
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GameOver",
                       True,(255,255,255))
    txt_rct=txt.get_rect()
    txt_rct.center = WIDTH/2,HEIGHT/2
    screen.blit(txt, txt_rct)

    pg.display.update()
    time.sleep(5)
    return
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0,0.9)
    bb_img=pg.Surface((20,20))#爆弾用の空Surface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)#爆弾円を描く
    bb_img.set_colorkey((0,0,0))#四隅の黒を透過させる
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect()#爆弾rectの抽出
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)#
    vx,vy =+5,+5 #爆弾速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            # return
            
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,tpl in DELTA.items():#########
            if key_lst[key]:###########
                sum_mv[0] += tpl[0]##########
                sum_mv[1] += tpl[1]##########            
        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外なら元の場所に戻す↓
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)###########
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出てる
            vx *= -1
        if not tate:  # 縦にはみ出てる
            vy *= -1
        screen.blit(bb_img, bb_rct)######
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
