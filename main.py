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
cicekler = ["tulip.jpg", "daisy.png"]  # Flower images

# Buttons
yuz_dugmesi = pygame.Rect(100, 500, 150, 50)  # Human
nesne_dugmesi = pygame.Rect(325, 500, 100, 50)  # Object
pareidolia_yuzu_dugmesi = pygame.Rect(550, 500, 150, 50)  # Pareidolia

# Flower buttons
lale_dugmesi = pygame.Rect(200, 500, 100, 50)  # Tulip
papatya_dugmesi = pygame.Rect(500, 500, 100, 50)  # Daisy

# Font
font = pygame.font.Font(None, 36)


def draw_buttons(is_flower_question):
    if is_flower_question:
        pygame.draw.rect(screen, black, lale_dugmesi)
        pygame.draw.rect(screen, black, papatya_dugmesi)
        lale_text = font.render("Lale", True, white)
        papatya_text = font.render("Papatya", True, white)
        screen.blit(lale_text, (lale_dugmesi.x + 20, lale_dugmesi.y + 10))
        screen.blit(papatya_text, (papatya_dugmesi.x + 10, papatya_dugmesi.y + 10))
    else:
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


def check_answer(selected_button, current_image):
    global dogru, yanlis
    if selected_button == yuz_dugmesi and current_image in insan_yuzu:
        print("Doğru: İnsan Yüzü")
        dogru += 1
    elif selected_button == nesne_dugmesi and current_image in nesne:
        print("Doğru: Nesne")
        dogru += 1
    elif selected_button == pareidolia_yuzu_dugmesi and current_image in pareidolia_yuzu:
        print("Doğru: Pareidolia Yüzü")
        dogru += 1
    elif selected_button == lale_dugmesi and current_image == "tulip.jpg":
        print("Doğru: Lale")
        dogru += 1
    elif selected_button == papatya_dugmesi and current_image == "daisy.png":
        print("Doğru: Papatya")
        dogru += 1
    else:
        print("Yanlış Seçim")
        yanlis += 1


def display_question(question):
    question_text = font.render(question, True, black)
    screen.blit(question_text, (200, 50))


def prepare_question_sequence():
    flower_questions = cicekler * (len(insan_yuzu + nesne + pareidolia_yuzu) // len(cicekler) + 1)
    other_questions = insan_yuzu + nesne + pareidolia_yuzu
    random.shuffle(flower_questions)
    random.shuffle(other_questions)

    sequence = []
    for f, o in zip(flower_questions, other_questions):
        sequence.extend([f, o])

    return sequence[:len(other_questions) * 2]

running = True
showing_qr_image_before = True
showing_special_image = False
showing_qr_image_after = False
show_buttons = False
image_start_time = 0

all_special_images = prepare_question_sequence()
current_special_index = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and show_buttons:
            mouse_pos = event.pos
            current_image = all_special_images[current_special_index]
            is_flower = current_image in cicekler
            if is_flower:
                if lale_dugmesi.collidepoint(mouse_pos):
                    check_answer(lale_dugmesi, current_image)
                elif papatya_dugmesi.collidepoint(mouse_pos):
                    check_answer(papatya_dugmesi, current_image)
            else:
                if yuz_dugmesi.collidepoint(mouse_pos):
                    check_answer(yuz_dugmesi, current_image)
                elif nesne_dugmesi.collidepoint(mouse_pos):
                    check_answer(nesne_dugmesi, current_image)
                elif pareidolia_yuzu_dugmesi.collidepoint(mouse_pos):
                    check_answer(pareidolia_yuzu_dugmesi, current_image)

            # Move to the next question
            current_special_index += 1
            if current_special_index >= len(all_special_images):
                running = False
            else:
                show_buttons = False
                showing_qr_image_before = True
                image_start_time = time.time()

    screen.fill(white)

    if showing_qr_image_before:
        if time.time() - image_start_time >= 0.3:  # Show QR image for 0.3 seconds
            showing_qr_image_before = False
            showing_special_image = True
            image_start_time = time.time()
        else:
            load_and_draw_image(random.choice(anlamsiz_resimler))
    elif showing_special_image:
        if time.time() - image_start_time >= 0.1:  # Show special image for 0.1 seconds
            showing_special_image = False
            showing_qr_image_after = True
            image_start_time = time.time()
        else:
            load_and_draw_image(all_special_images[current_special_index])
            display_question("Resimde ne gördünüz?")
    elif showing_qr_image_after:
        if time.time() - image_start_time >= 0.3:  # Show QR image for 0.3 seconds
            showing_qr_image_after = False
            show_buttons = True
        else:
            load_and_draw_image(random.choice(anlamsiz_resimler))
    elif show_buttons:
        is_flower = all_special_images[current_special_index] in cicekler
        draw_buttons(is_flower)
        display_question("Resimde ne gördünüz?")

    pygame.display.flip()
    pygame.time.wait(50)  # Add a small delay to control the frame rate

print("Doğru Cevap Sayısı: ", dogru)  # Correct answer count at the end
print("Yanlış Cevap Sayısı: ", yanlis)  # Wrong answer count at the end
pygame.quit()