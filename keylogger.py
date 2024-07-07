import pygame
import cv2
import numpy as np
import random

pygame.init()

# Pygame 창 설정
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive English Keyboard")

# 색상 정의
RED = (220, 50, 50)
GREEN = (50, 150, 50)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# 키 배열 정의
keys = [
    ['esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', '🔒'],
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '←'],
    ['tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
    ['caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'enter'],
    ['shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'shift'],
    ['fn', 'control', 'option', 'command', ' ', 'command', 'option', '◀', '▲', '▼', '▶']
]

typed_text = ""
caps_on = False
video_playing = False
video_played = False
color_timer = 0

particles = []
snowflakes = []

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = random.randint(3, 8)
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-8, -2)
        self.color = color
        self.alpha = 255
        self.gravity = 0.1

    def update(self):
        self.x += self.vx
        self.y += self.vy + self.gravity
        self.alpha -= 10
        if self.alpha <= 0:
            return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color + (self.alpha,), (int(self.x), int(self.y)), int(self.size))

class Snowflake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2)

    def update(self):
        self.y += self.speed
        self.x += random.uniform(-0.5, 0.5)  # 약간의 좌우 움직임 추가

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

def draw_key(screen, x, y, width, height, text, is_active=False):
    color = RED if is_active else GRAY
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 1)
    font = pygame.font.Font(None, int(height * 0.4))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

def play_video(video_file):
    cap = cv2.VideoCapture(video_file)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video', frame_width, frame_height)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Video', frame)

        wait_time = int(1000 / fps)
        key = cv2.waitKey(wait_time) & 0xFF

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True

def draw_text(screen, text, x, y, font, max_width=None, blink=False):
    colors = [GREEN, RED]
    current_x = x
    for i, char in enumerate(text):
        if char == '\n':
            y += font.get_height()
            current_x = x
            continue
        color = colors[(i + color_timer // 5) % 2] if blink else BLACK
        char_surface = font.render(char, True, color)
        screen.blit(char_surface, (current_x, y))
        current_x += char_surface.get_width()

running = True
key_rects = []

monitor_x = 50
monitor_y = 20
monitor_width = WIDTH - 100
monitor_height = 100

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, text in key_rects:
                if rect.collidepoint(event.pos):
                    if text == '←':
                        typed_text = typed_text[:-1]
                    elif text == 'caps':
                        caps_on = not caps_on
                    elif text == 'enter':
                        typed_text += '\n'
                        if typed_text.strip() == "Merry Christmas":
                            video_playing = True
                            typed_text_saved = typed_text
                            typed_text = ""
                    elif text not in ['esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
                                      '🔒', 'tab', 'shift', 'fn', 'control', 'option', 'command', '◀', '▲', '▼', '▶']:
                        if text.isalpha():
                            if caps_on:
                                typed_text += text.upper()
                            else:
                                typed_text += text.lower()
                        else:
                            typed_text += text

                    x = rect.centerx
                    y = rect.centery
                    for _ in range(random.randint(10, 20)):
                        particles.append(Particle(x, y, random.choice([RED, GREEN])))

    screen.fill(WHITE)

    # 모니터 프레임 그리기
    pygame.draw.rect(screen, BLACK, (monitor_x, monitor_y, monitor_width, monitor_height), 5)
    pygame.draw.rect(screen, GRAY, (monitor_x + 5, monitor_y + 5, monitor_width - 10, monitor_height - 10))

    # 눈 생성
    if video_played and random.random() < 0.3:  # 30% 확률로 새 눈송이 생성
        snowflakes.append(Snowflake(random.randint(monitor_x, monitor_x + monitor_width), monitor_y))

    # 눈 업데이트 및 그리기
    for snowflake in snowflakes[:]:
        snowflake.update()
        if snowflake.y > monitor_y + monitor_height:
            snowflakes.remove(snowflake)
        else:
            snowflake.draw(screen)

    font = pygame.font.Font(None, 36)
    if not video_played:
        draw_text(screen, typed_text, monitor_x + 10, monitor_y + 10, font, monitor_width - 20)
    else:
        draw_text(screen, typed_text_saved, monitor_x + 10, monitor_y + 10, font, monitor_width - 20, blink=True)

    num_rows = len(keys)
    num_cols = max(len(row) for row in keys)

    key_width = WIDTH / num_cols
    key_height = (HEIGHT - 150) / num_rows

    key_rects.clear()

    for row_index, row in enumerate(keys):
        y = monitor_height + 50 + row_index * key_height
        x = 0
        row_width = 0
        for key in row:
            if key == 'shift':
                width = key_width * 2.3 if row_index == 4 else key_width * 1.5
            elif key == 'tab':
                width = key_width * 1.3
            elif key in ['caps', 'fn', 'control', 'option', 'command']:
                width = key_width * 1.5
            elif key == ' ':
                width = key_width * 5
            elif key == 'enter':
                width = key_width * 2
            else:
                width = key_width
            row_width += width

        extra_space = WIDTH - row_width
        if row_index == 4:
            shift_extra = extra_space / 2
            for i, key in enumerate(row):
                if key == 'shift':
                    width = key_width * 2.3 + shift_extra
                else:
                    width = key_width
                rect = draw_key(screen, x, y, width, key_height, key, key == 'caps' and caps_on)
                key_rects.append((rect, key))
                x += width
        else:
            extra_per_key = extra_space / len(row)
            for key in row:
                if key == 'shift':
                    width = key_width * 2.3
                elif key == 'tab':
                    width = key_width * 1.3
                elif key in ['caps', 'fn', 'control', 'option', 'command']:
                    width = key_width * 1.5
                elif key == ' ':
                    width = key_width * 5
                elif key == 'enter':
                    width = key_width * 2
                else:
                    width = key_width
                width += extra_per_key
                rect = draw_key(screen, x, y, width, key_height, key, key == 'caps' and caps_on)
                key_rects.append((rect, key))
                x += width

    for particle in particles[:]:
        if particle.update():
            particles.remove(particle)
        else:
            particle.draw(screen)

    pygame.display.flip()

    color_timer = (color_timer + 1) % 10

    if video_playing:
        success = play_video("spiral_tree.mp4")
        video_playing = False
        video_played = True

pygame.quit()