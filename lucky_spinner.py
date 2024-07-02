import pygame
import random
import math

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lucky Spinner with Pin")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
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
pin_angle = 270  # 핀의 각도를 270도로 설정하여 상단 중앙에 배치

# 섹션 텍스트 설정
section_texts = [f"Section {i + 1}" for i in range(num_sections)]

# 핀 설정
pin_length = 20
pin_width = 20

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

        # 핀이 돌림판에 닿을 때마다 속도를 줄임
        pin_angle_rad = math.radians(pin_angle)
        pin_x = center[0] + radius * math.cos(pin_angle_rad)
        pin_y = center[1] + radius * math.sin(pin_angle_rad)

        for i in range(num_sections):
            section_angle = (360 / num_sections) * i + angle
            section_angle_rad = math.radians(section_angle)
            section_x = center[0] + radius * math.cos(section_angle_rad)
            section_y = center[1] + radius * math.sin(section_angle_rad)

            if abs(pin_x - section_x) < 5 and abs(pin_y - section_y) < 5:
                spin_speed *= 0.9  # 속도를 줄임

        if spin_speed < 0.1:
            spin_speed = 0
            spinning = False
            # 결과 계산
            result_angle = (pin_angle - angle) % 360
            section = int(result_angle // (360 / num_sections))
            result_text = f"{section_texts[section]}"

    # 화면 그리기
    screen.fill(WHITE)

    # 돌림판 그리기
    for i in range(num_sections):
        start_angle = math.radians((360 / num_sections) * i + angle)
        end_angle = math.radians((360 / num_sections) * (i + 1) + angle)

        x1 = center[0] + radius * math.cos(start_angle)
        y1 = center[1] + radius * math.sin(start_angle)
        x2 = center[0] + radius * math.cos(end_angle)
        y2 = center[1] + radius * math.sin(end_angle)

        pygame.draw.polygon(screen, COLORS[i % len(COLORS)], [center, (x1, y1), (x2, y2)])

        # 섹션 텍스트 그리기
        text_angle = (start_angle + end_angle) / 2
        text_x = center[0] + int(radius / 1.5 * math.cos(text_angle))
        text_y = center[1] + int(radius / 1.5 * math.sin(text_angle))
        text_surface = font.render(section_texts[i], True, BLACK)
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)

    # 삼각형 핀 그리기
    pin_base_left = (
        center[0] + (radius - pin_length) * math.cos(math.radians(pin_angle - pin_width / 2)),
        center[1] + (radius - pin_length) * math.sin(math.radians(pin_angle - pin_width / 2))
    )
    pin_base_right = (
        center[0] + (radius - pin_length) * math.cos(math.radians(pin_angle + pin_width / 2)),
        center[1] + (radius - pin_length) * math.sin(math.radians(pin_angle + pin_width / 2))
    )
    pin_tip = (
        center[0] + (radius + pin_length) * math.cos(math.radians(pin_angle)),
        center[1] + (radius + pin_length) * math.sin(math.radians(pin_angle))
    )
    pygame.draw.polygon(screen, RED, [pin_base_left, pin_base_right, pin_tip])

    # 결과 텍스트 그리기
    if result_text:
        text_surface = font.render(result_text, True, BLACK)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, 50))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
