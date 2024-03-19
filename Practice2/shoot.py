import pygame
import sys
def game():
    pygame.init()
    #屏幕参数
    pygame.display.set_caption("SHOOT")
    screen = pygame.display.set_mode((1000,700))
    bg_color = (0,0,0)
    screen_rect = screen.get_rect()

    #物体参数
    rect = pygame.Rect(30,0,
                       50,50)
   
    rect_color = (255,255,255)
    rect.centery = screen_rect.centery
    y = float(rect.centery)
    rect_factor = 0.2
        #物体移动状态
    rect_moving_up = False
    rect_moving_down = False

    #子弹参数
    
    # bullet_rect = pygame.Rect(0,0,
    #                      15,3)
    bullet__rect_color = (123,123,123)
    bullet_rect_factor = 1
    bullets = []


    
    
    
    
    while True:
        #检查事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                sys.exit()

            if event.type ==pygame.KEYDOWN:
                if event.key  == pygame.K_ESCAPE:

                    sys.exit()
                
                if event.key == pygame.K_UP:

                    rect_moving_up = True
                if event.key == pygame.K_DOWN:

                    rect_moving_down = True

            #         def fire_bullet():
            # for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet_rect = pygame.Rect(0,0,
                         15,3)
                        bullet_rect.right = rect.right
                        bullet_rect.centery = rect.centery
                        
                        new_bullet = bullet_rect
                        bullets.append(new_bullet)




            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_UP:

                    rect_moving_up = False
                if event.key == pygame.K_DOWN:

                    rect_moving_down = False
        
        
        #rect移动事件
        if rect_moving_up and rect.top > 0:

            y -= rect_factor
            
        if rect_moving_down and rect.bottom < screen_rect.bottom:
            y += rect_factor
        
        #如果bullets不为空，则射出子弹
        if bullets:
            for bullet in bullets:

                bullet.centerx += bullet_rect_factor
        #子弹如果超出边界则移除
            if bullet.centerx >screen_rect.right:
                bullets.remove(bullet)
            
            
        
        

        
        rect.centery = y

    

        
        screen.fill(bg_color)
        pygame.draw.rect(screen,rect_color,rect)
        for bullet_rect in bullets:

            pygame.draw.rect(screen,bullet__rect_color,bullet_rect)
        pygame.display.flip()


game()
