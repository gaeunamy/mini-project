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
YELLOW = (255, 255, 0)  # 노란색으로 추가 정의
SKY_BLUE = (135, 206, 235)  # 하늘색
COLORS = [SKY_BLUE] * 8  # 모든 섹션을 하늘색으로 초기화

# 폰트 설정
font = pygame.font.Font(None, 36)

# 게임 변수
running = True
spinning = False
angle = 0
spin_speed = 20  # 반응 속도를 빠르게 설정
result_text = ""
num_sections = 8
center = (screen_width // 2, screen_height // 2)
radius = 250
pin_angle = 270  # 핀의 각도를 270도로 설정하여 상단 중앙에 배치
pin_length = 20
pin_width = 10  # 핀의 너비를 조정
selected_section = -1  # 선택된 섹션의 인덱스, 초기값은 -1 (선택되지 않음을 의미)
last_section = -1  # 마지막에 멈춘 섹션의 인덱스, 초기값은 -1 (아직 없음을 의미)

# 섹션 텍스트 설정
section_texts = [f"Section {i + 1}" for i in range(num_sections)]

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not spinning:
            spinning = True
            spin_speed = random.randint(10, 20)
            selected_section = -1  # 새로 스핀을 시작할 때 선택된 섹션 초기화
            last_section = -1  # 새로 스핀을 시작할 때 마지막 섹션 초기화

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
                selected_section = i  # 선택된 섹션 업데이트

        if spin_speed < 0.1:
            spin_speed = 0
            spinning = False
            # 결과 계산
            result_angle = (pin_angle - angle) % 360
            last_section = int(result_angle // (360 / num_sections))
            result_text = f"{section_texts[last_section]}"

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

        # 마지막에 멈춘 섹션은 빨간색으로 그리기
        if i == last_section:
            pygame.draw.polygon(screen, RED, [center, (x1, y1), (x2, y2)])
        else:
            pygame.draw.polygon(screen, COLORS[i], [center, (x1, y1), (x2, y2)])

        # 섹션 텍스트 그리기
        text_angle = (start_angle + end_angle) / 2
        text_x = center[0] + int(radius / 1.5 * math.cos(text_angle))
        text_y = center[1] + int(radius / 1.5 * math.sin(text_angle))
        text_surface = font.render(section_texts[i], True, BLACK)
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)

    # 역삼각형 핀 그리기
    pin_base_left = (
        center[0] + (radius - pin_length) * math.cos(math.radians(pin_angle + pin_width / 2)),
        center[1] + (radius - pin_length) * math.sin(math.radians(pin_angle + pin_width / 2))
    )
    pin_base_right = (
        center[0] + (radius - pin_length) * math.cos(math.radians(pin_angle - pin_width / 2)),
        center[1] + (radius - pin_length) * math.sin(math.radians(pin_angle - pin_width / 2))
    )
    pin_tip = (
        center[0] + (radius + pin_length) * math.cos(math.radians(pin_angle)),
        center[1] + (radius + pin_length) * math.sin(math.radians(pin_angle))
    )
    pygame.draw.polygon(screen, RED, [pin_tip, pin_base_right, pin_base_left])

    # 결과 텍스트 그리기
    if result_text:
        text_surface = font.render(result_text, True, BLACK)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, 50))

    pygame.display.flip()
    pygame.time.Clock().tick(60)  # 반응 속도를 높이기 위해 주기를 더 짧게 설정

pygame.quit()
