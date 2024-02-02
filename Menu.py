import pygame
import subprocess
import pygame.mixer
import chessmain
import sys

pygame.init()

# Cửa sổ game
screen = pygame.display.set_mode((512+140, 512))

#Âm thanh
start_sound = pygame.mixer.Sound(r'sounds/game-start.mp3')
quit_sound = pygame.mixer.Sound(r'sounds/game-end.mp3')
move_self = pygame.mixer.Sound(r'sounds/move-self.mp3')
move_opponent = pygame.mixer.Sound(r'sounds/move-opponent.mp3')
move_check = pygame.mixer.Sound(r'sounds/move-check.mp3')
pre_move = pygame.mixer.Sound(r'sounds/premove.mp3')
tenseconds_time = pygame.mixer.Sound(r'sounds/tenseconds - time.mp3')

background_music = pygame.mixer.Sound(r'sounds/music-background.mp3')

#Tạo nút menu
start_button = pygame.Rect(380+50, 70, 100, 25)
quit_button = pygame.Rect(380+50, 370, 100, 25)
about_me = pygame.Rect(380+50, 270, 100, 25)
play_with_ai = pygame.Rect(380+50, 170, 100, 25)

# Một ví dụ về thông tin thành viên
about_me_info = """
Python 10 - nhóm 9
Nguyen Anh Tu - B21DCCN747
Dang Minh Duc - B21DCCN236
Le Duc Thang - B21DCCN664
Kieu Van Hieu - B21DCCN052

How to play:
When it is your turn, select a piece and 
click on the green square to move it.
Press "z" to undo your previous move.
Press "r" to restart the game.
Press "m" to return to the main menu.
"""

def Draw(start_button, quit_button, about_me, play_with_ai):
    # front cho văn bản
    font = pygame.font.Font(None, 36)
    # Màu sắc
    white = (48, 216, 242)
    black = (30, 18, 36)
    # Vẽ nút menu
    pygame.draw.rect(screen, black, start_button)
    pygame.draw.rect(screen, black, quit_button)
    pygame.draw.rect(screen, black, about_me)
    pygame.draw.rect(screen, black, play_with_ai)
    # Vẽ văn bản trên nút
    start_text = font.render("      Start ", True, 'white')
    quit_text = font.render(" Exit", True, 'white')
    about_me_react = font.render("    Info", True, 'white')
    play_with_ai_react = font.render("Bot", True, 'white')
    screen.blit(start_text, (360+50, 70))
    screen.blit(quit_text, (400+50, 370))
    screen.blit(about_me_react, (380+50, 270))
    screen.blit(play_with_ai_react, (410+50, 170))
    # icon loa
    speaker_image = pygame.image.load(r'images/speaker.png')
    speaker_rect = speaker_image.get_rect()
    speaker_rect.topleft = (5, 15)  # Đặt vị trí ở góc trên bên trái
    screen.blit(speaker_image, speaker_rect)
    pygame.display.update()
    return speaker_rect

back_to_main = False
background_music_on = True  # Khởi tạo biến background_music_on ở đầu chương trình

def ShowInfo():
    global screen, back_to_main, background_music_on
    about_me_screen = True
    while about_me_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    quit_sound.play()
                    back_to_main = True
                    about_me_screen = False  # Thoát khỏi vòng lặp

        pygame.draw.rect(screen, (0, 0, 0), (50, 50, 412, 412))
        font = pygame.font.Font(None, 28)
        lines = about_me_info.splitlines()
        y = 50
        for line in lines:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (70, y))
            y += 28

        back_button = pygame.Rect(400, 10, 100, 40)
        pygame.draw.rect(screen, (0, 0, 0), back_button)
        back_font = pygame.font.Font(None, 28)
        back_text = back_font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (410, 20))
        pygame.display.update()

def Background():
    # Cửa sổ game
    screen = pygame.display.set_mode((512 + 140, 512))
    # Tiêu đề
    pygame.display.set_caption('Chess')
    # Icon game
    icon = pygame.image.load(r'images/icon.png')
    pygame.display.set_icon(icon)
    # background game
    bg = pygame.image.load(r'images/bgchess.jpg')
    screen.blit(bg, (0, 0))
    pygame.display.update()

def Music():
    if background_music_on:
        background_music.set_volume(0.3)  # âm lượng còn 30%
        background_music.play(loops=-1)  # lặp vô hạn

def menu():
    global background_music, screen, back_to_main, background_music_on
    running = True
    Background()
    Music()
    speaker_rect = Draw(start_button, quit_button, about_me, play_with_ai)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    print("Bắt đầu trò chơi")  # Thay thế bằng mã để bắt đầu trò chơi thực tế
                    start_sound.play()
                    if background_music_on:
                        background_music.stop()
                    chessmain.main(singlePlayer = False)
                elif quit_button.collidepoint(event.pos):
                    quit_sound.play()
                    pygame.time.wait(1000)
                    running = False
                elif speaker_rect.collidepoint(event.pos):
                    quit_sound.play()
                    if background_music.get_volume() > 0:
                        background_music.set_volume(0)
                        background_music_on = False
                    else:
                        background_music.set_volume(0.3)
                        background_music_on = True

                elif about_me.collidepoint(event.pos):
                    quit_sound.play()
                    ShowInfo()
                    if back_to_main:
                        if background_music_on:
                            background_music.stop()
                        back_to_main = False
                    return menu()

                elif play_with_ai.collidepoint(event.pos):
                    quit_sound.play()
                    if background_music_on:
                        background_music.stop()
                    print('Chơi với Bot ')
                    chessmain.main(singlePlayer=True)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    menu()
