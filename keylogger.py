import pygame
import cv2
import numpy as np
import random

pygame.init()

# Pygame 창 설정
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive English Keyboard")

# 크리스마스 색상
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

particles = []

# 파티클 클래스
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = random.randint(3, 8)
        self.vx = random.uniform(-4, 4)  # 속도 설정 (수정된 부분)
        self.vy = random.uniform(-8, -2)  # 속도 설정 (수정된 부분)
        self.color = color  # 주어진 색상 사용
        self.alpha = 255  # 초기 투명도 설정
        self.gravity = 0.1  # 중력 가속도

    def update(self):
        self.x += self.vx
        self.y += self.vy + self.gravity
        self.alpha -= 10  # 투명도 감소
        if self.alpha <= 0:
            return True  # 파티클 제거 필요

    def draw(self, screen):
        pygame.draw.circle(screen, self.color + (self.alpha,), (int(self.x), int(self.y)), int(self.size))


# Pygame 화면에 키 그리기 함수
def draw_key(screen, x, y, width, height, text, is_active=False):
    color = RED if is_active else GRAY
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 1)
    font = pygame.font.Font(None, int(height * 0.4))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)


# 비디오 재생 함수 (OpenCV로 구현)
def play_video(video_file):
    cap = cv2.VideoCapture(video_file)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)  # 현재 비디오의 FPS 가져오기

    # OpenCV 창 생성
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video', frame_width, frame_height)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Video', frame)

        # 원래 FPS에 맞추어 대기 시간 계산
        wait_time = int(1000 / fps)  # 프레임 사이의 대기 시간(ms)
        key = cv2.waitKey(wait_time) & 0xFF

        # 'q' 키를 누르면 종료
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True


# 텍스트 그리기 함수
def draw_text(screen, text, x, y, font, max_width=None):
    alternating_colors = [GREEN, RED]  # 초록과 빨강 색상
    color_index = 0

    lines = text.split('\n')  # 줄 바꿈 문자로 텍스트를 분할

    for line in lines:
        current_x = x
        for char in line:
            char_surface = font.render(char, True, alternating_colors[color_index % 2])
            char_rect = char_surface.get_rect(topleft=(current_x, y))
            screen.blit(char_surface, char_rect)
            current_x += char_rect.width  # 다음 글자 위치로 이동
            color_index += 1
        y += font.get_height()  # 다음 줄로 이동

# 메인 루프
running = True
key_rects = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, text in key_rects:
                if rect.collidepoint(event.pos):
                    if text == '←':
                        typed_text = typed_text[:-1]  # Backspace
                    elif text == 'caps':
                        caps_on = not caps_on  # Caps Lock 토글
                    elif text == 'enter':
                        # Enter 키 누를 때마다 줄 바꿈 추가
                        typed_text += '\n'
                        # "Merry Christmas"가 입력되었는지 확인
                        if typed_text.strip() == "Merry Christmas":
                            video_playing = True  # 비디오 재생 시작
                            typed_text_saved = typed_text  # 입력된 텍스트 저장
                            typed_text = ""  # 입력된 텍스트 초기화
                    elif text not in ['esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
                                      '🔒', 'tab', 'shift', 'fn', 'control', 'option', 'command', '◀', '▲', '▼', '▶']:
                        if text.isalpha():
                            if caps_on:
                                typed_text += text.upper()
                            else:
                                typed_text += text.lower()
                        else:
                            typed_text += text

                    # 파티클 생성
                    x = rect.centerx
                    y = rect.centery
                    for _ in range(random.randint(10, 20)):  # 더 많은 파티클 생성
                        particles.append(
                            Particle(x, y, random.choice([RED, GREEN])))  # 초록과 빨강 색상 사용

    screen.fill(WHITE)

    # 모니터 프레임 그리기
    monitor_x = 50
    monitor_y = 20
    monitor_width = WIDTH - 100
    monitor_height = 100
    pygame.draw.rect(screen, BLACK, (monitor_x, monitor_y, monitor_width, monitor_height), 5)
    pygame.draw.rect(screen, GRAY, (monitor_x + 5, monitor_y + 5, monitor_width - 10, monitor_height - 10))

    # 모니터 안에 텍스트 표시
    font = pygame.font.Font(None, 36)
    if not video_playing:
        draw_text(screen, typed_text, monitor_x + 10, monitor_y + 10, font, monitor_width - 20)
    else:
        draw_text(screen, typed_text_saved, monitor_x + 10, monitor_y + 10, font, monitor_width - 20)

    num_rows = len(keys)
    num_cols = max(len(row) for row in keys)

    key_width = WIDTH / num_cols
    key_height = (HEIGHT - 150) / num_rows  # 모니터 영역을 감안하여 키 높이 조정

    key_rects.clear()

    # 키 그리기
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
        if row_index == 4:  # Shift 키 줄
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

    # 파티클 업데이트 및 그리기
    for particle in particles[:]:  # 리스트를 복사하여 반복 중 수정이 일어나지 않도록 함
        if particle.update():
            particles.remove(particle)
        else:
            particle.draw(screen)

    pygame.display.flip()

    # "Merry Christmas"가 입력되고 비디오가 재생 중일 때
    if video_playing:
        success = play_video("spiral_tree.mp4")
        video_playing = False  # 비디오 재생이 끝나면 다시 False로 설정
        typed_text = typed_text_saved  # 비디오 재생 후에도 입력된 텍스트 유지

pygame.quit()
