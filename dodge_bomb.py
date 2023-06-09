import random
import sys
import pygame as pg

delta = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0)
        }




def check_bound(scr_rect: pg.Rect, obj_rect: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定して、真理値タプルを返す関数
    引数1：画面surfaceのrect
    引数2:こうかとん、爆弾surfaceのrect
    戻り値:横方向、縦方向のはみ出し判定結果
    """
    yoko, tate = True, True
    if obj_rect.left < scr_rect.left or scr_rect.right < obj_rect.right:
        yoko = False
    if obj_rect.top < scr_rect.top or obj_rect.bottom > scr_rect.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    x, y = random.randint(0,1600), random.randint(0,900)
    bb_rect = bb_img.get_rect()
    bb_rect.center = x, y
    vx, vy = +1, +1
    kk_rect = kk_img.get_rect()
    kk_rect.center = 600, 400
    a, b, c = 10, 20, 255
    tmr = 0
    kk_delta = {
        (-1,0):pg.transform.rotozoom(kk_img, 0, 0),
        (0,-1):pg.transform.rotozoom(kk_img, 90, 0),
        (1,0):pg.transform.rotozoom(kk_img, 180, 0),
        (0,1):pg.transform.rotozoom(kk_img, 270, 0),
    }

    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0
        
        tmr += 1 
        a = tmr/10
        b = tmr/10
        c = 255-tmr/30
        bb_img = pg.Surface((a*10, a*10))
        pg.draw.circle(bb_img, (c, 0, 0), (b, b), b)  # tmrが100増えるごとに円の直径が大きくなっていく
        bb_img.set_colorkey((0, 0, 0))
        key_lst = pg.key.get_pressed()
        for k, mv in delta.items():
            if key_lst[k]:
                kk_rect.move_ip(mv)
        if check_bound(screen.get_rect(), kk_rect) != (True, True):
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rect.move_ip(-mv[0], -mv[1])
        screen.blit(bg_img, [0, 0])
        for k, mv in delta.items():
            for delt, img in kk_delta.items():
                if k == delt:
                    kk_img = img
        screen.blit(kk_img, kk_rect)
        bb_rect.move_ip(vx,vy)
        yoko, tate = check_bound(screen.get_rect(), bb_rect)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rect)
        if kk_rect.colliderect(bb_rect):
            return
        

        pg.display.update()
        clock.tick(300)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()