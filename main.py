import random
import pygame
import time

pygame.init()
dogru = 0  # Correct
yanlis = 0  # Wrong

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pareidolia Test")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Define pictures
anlamsiz_resimler = ["d1.jpg", "d2.jpg", "d3.jpg"]  # Random qr-like images
insan_yuzu = ["yuz1.jpg", "yuz2.jpg", "yuz3.jpg", "yuz4.jpg", "yuz5.jpg", "yuz6.jpg"]  # Human faces
nesne = ["nesne1.png"]  # Objects
pareidolia_yuzu = ["para1.png", "para2.png", "para3.png", "para4.png", "para5.png"]  # Pareidolia faces

# Buttons
yuz_dugmesi = pygame.Rect(100, 500, 150, 50)  # Human
nesne_dugmesi = pygame.Rect(325, 500, 100, 50)  # Object
pareidolia_yuzu_dugmesi = pygame.Rect(550, 500, 150, 50)  # Pareidolia

# Font
font = pygame.font.Font(None, 36)


def draw_buttons():
    pygame.draw.rect(screen, black, yuz_dugmesi)
    pygame.draw.rect(screen, black, nesne_dugmesi)
    pygame.draw.rect(screen, black, pareidolia_yuzu_dugmesi)
    insan_yuzu_text = font.render("İnsan Yüzü", True, white)
    nesne_text = font.render("Nesne", True, white)
    pareidolia_text = font.render("Pareidolia Yüzü", True, white)
    screen.blit(insan_yuzu_text, (yuz_dugmesi.x + 10, yuz_dugmesi.y + 10))
    screen.blit(nesne_text, (nesne_dugmesi.x + 20, nesne_dugmesi.y + 10))
    screen.blit(pareidolia_text, (pareidolia_yuzu_dugmesi.x + 5, pareidolia_yuzu_dugmesi.y + 10))


def load_and_draw_image(image_path):
    image = pygame.image.load("img/" + image_path)
    image = pygame.transform.scale(image, (400, 400))
    screen.blit(image, (200, 100))


def check_answer(selected_button):
    global dogru, yanlis
    if selected_button == yuz_dugmesi and gosterilenresim in insan_yuzu:
        print("Doğru: İnsan Yüzü")
        dogru += 1
    elif selected_button == nesne_dugmesi and gosterilenresim in nesne:
        print("Doğru: Nesne")
        dogru += 1
    elif selected_button == pareidolia_yuzu_dugmesi and gosterilenresim in pareidolia_yuzu:
        print("Doğru: Pareidolia Yüzü")
        dogru += 1
    else:
        print("Yanlış Seçim")
        yanlis += 1


running = True
showing_special_image = False
special_image_start_time = 0
show_buttons = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and show_buttons:
            mouse_pos = event.pos
            if yuz_dugmesi.collidepoint(mouse_pos):
                check_answer(yuz_dugmesi)
                show_buttons = False
            elif nesne_dugmesi.collidepoint(mouse_pos):
                check_answer(nesne_dugmesi)
                show_buttons = False
            elif pareidolia_yuzu_dugmesi.collidepoint(mouse_pos):
                check_answer(pareidolia_yuzu_dugmesi)
                show_buttons = False

    screen.fill(white)

    if showing_special_image:
        if time.time() - special_image_start_time >= 0.2:
            showing_special_image = False
            show_buttons = True
        else:
            load_and_draw_image(gosterilenresim)
            showing_special_image = True
    elif not show_buttons:
        if random.random() < 0.01:  # %10
            gosterilenresim = random.choice(insan_yuzu + nesne + pareidolia_yuzu)
            special_image_start_time = time.time()
            showing_special_image = True

        else:
            gosterilenresim = random.choice(anlamsiz_resimler)

        # draw random qr-like images
        load_and_draw_image(gosterilenresim)

    # draw buttons
    if show_buttons:
        draw_buttons()

    pygame.display.flip()

print("Doğru Cevap Sayısı: ", dogru)  # Correct answer count at the end
print("Yanlış Cevap Sayısı: ", yanlis)  # Wrong answer count at the end
pygame.quit()
