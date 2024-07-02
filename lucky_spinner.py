import pygame
import random
import math

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lucky Spinner")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), 
    (255, 255, 0), (0, 255, 255), (255, 0, 255), 
    (192, 192, 192), (128, 0, 128)
]

# 폰트 설정
font = pygame.font.Font(None, 36)

# 게임 변수
running = True
spinning = False
angle = 0
spin_speed = 0
result_text = ""
num_sections = 8
center = (screen_width // 2, screen_height // 2)
radius = 250

# 섹션 텍스트 설정
section_texts = [f"Section {i+1}" for i in range(num_sections)]

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not spinning:
            spinning = True
            spin_speed = random.randint(10, 20)

    if spinning:
        angle += spin_speed
        spin_speed *= 0.99  # 서서히 멈추게 하는 감속
        if spin_speed < 0.1:
            spin_speed = 0
            spinning = False
            # 결과 계산
            result_angle = angle % 360
            section = math.floor(result_angle / (360 / num_sections))  # 예시로 8개의 섹션으로 나눔
            result_text = f"{section_texts[section]}"

    # 화면 그리기
    screen.fill(WHITE)

    # 돌림판 그리기
    for i in range(num_sections):
        start_angle = (360 / num_sections) * i
        end_angle = (360 / num_sections) * (i + 1)
        pygame.draw.arc(
            screen, COLORS[i % len(COLORS)], 
            (*center, radius * 2, radius * 2), 
            start_angle + angle, end_angle + angle
        )
        # 섹션 텍스트 그리기
        text_angle = math.radians(start_angle + (180 / num_sections) + angle)
        text_x = center[0] + int(radius / 2 * math.cos(text_angle))
        text_y = center[1] + int(radius / 2 * math.sin(text_angle))
        text_surface = font.render(section_texts[i], True, BLACK)
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)

    # 결과 텍스트 그리기
    if result_text:
        text_surface = font.render(result_text, True, BLACK)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, 50))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
