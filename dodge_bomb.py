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

accs = [a for a in range(1,11)]##########

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
    sikaku = pg.Surface((WIDTH,HEIGHT))
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

def init_bb_imgs() ->  tuple[list[pg.Surface], list[int]]:
    """
    拡大・加速する爆弾の生成
    引数：なし
    戻り値：accs(加速倍率のintリスト),bb_imgs(爆弾表示のためのpg.Surfaceリスト)

    """
    
    bb_imgs=[]
    
    bb_accs = [a for a in range(1,11)]# 加速度のリスト
    
    for r in range(1, 11):# 拡大のリスト
        # bb_accs.append(r)  # 加速度
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs,bb_accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    飛ぶ方向に応じてこうかとんの画像を切り替える
    引数：移動量タプル

    """
    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0,0.9)
    kk_img2 = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45,0.9)
    kk_img3 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45,0.9)
    kk_img4 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 90,0.9)
        
    kk_dict={(0,0):kk_img,
             (-5,0):kk_img,
             (-5,-5):kk_img2,
             (0,-5):pg.transform.flip(kk_img4,False,True),
             (+5,-5):pg.transform.flip(kk_img2,True,False),
             (+5,0):pg.transform.flip(kk_img,True,False),
             (+5,+5):pg.transform.flip(kk_img3,True,False),
             (0,+5):pg.transform.flip(kk_img,False,True),
             (-5,+5):pg.transform.flip(kk_img3,False,False),
    }
    
    return kk_dict[sum_mv]

def calc_orientation(org: pg.Rect, dst: pg.Rect,current_xy: tuple[float, float]) -> tuple[float, float]:
    pass


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
        
        #拡大加速の処理↓  
        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//100, 9)]  
        avy = vy*bb_accs[min(tmr//100, 9)]
        bb_img = bb_imgs[min(tmr//100, 9)]
            
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,tpl in DELTA.items():#########
            if key_lst[key]:###########
                sum_mv[0] += tpl[0]##########
                sum_mv[1] += tpl[1]##########            
        kk_rct.move_ip(sum_mv)
        
        kk_img = get_kk_img((0, 0)) 
        kk_img = get_kk_img(tuple(sum_mv))
        
        #こうかとんが画面外なら元の場所に戻す↓
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx,avy)###avx,avyに変更######
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
