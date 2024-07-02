import pygame
import random
import math

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lucky Spinner with Arrow")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SKY_BLUE = (135, 206, 235)
COLOR_SKY_BLUE = SKY_BLUE
COLOR_YELLOW = YELLOW
COLOR_RED = RED

# 폰트 설정
font = pygame.font.Font(None, 36)

# 게임 변수
running = True
spinning = False
angle = 0
spin_speed = 20
result_text = ""
num_sections = 8
center = (screen_width // 2, screen_height // 2)
radius = 250
arrow_width = 30  
arrow_height = 40  
arrow_head_height = 20  
arrow_head_base = 10  
arrow_tail_width = 10  
selected_section = -1
last_section = -1

# 섹션 텍스트 설정
section_texts = [
    "피자",    # 섹션 1
    "치킨",    # 섹션 2
    "Section 3",
    "Section 4",
    "Section 5",
    "Section 6",
    "Section 7",
    "Section 8"
]

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not spinning:
            spinning = True
            spin_speed = random.randint(10, 20)
            selected_section = -1
            last_section = -1

    if spinning:
        angle += spin_speed
        spin_speed *= 0.99

        pin_x = center[0]
        pin_y = center[1] - radius

        for i in range(num_sections):
            section_angle = (360 / num_sections) * i + angle
            section_angle_rad = math.radians(section_angle)
            section_x = center[0] + radius * math.cos(section_angle_rad)
            section_y = center[1] + radius * math.sin(section_angle_rad)

            # 섹션의 중심 각도 계산
            section_center_angle = (360 / num_sections) * i + angle + 180 / num_sections
            section_center_angle_rad = math.radians(section_center_angle)
            section_center_x = center[0] + radius * math.cos(section_center_angle_rad)
            section_center_y = center[1] + radius * math.sin(section_center_angle_rad)

            if abs(pin_x - section_center_x) < 5 and abs(pin_y - section_center_y) < 5:
                spin_speed *= 0.9
                selected_section = i

        if spin_speed < 0.1:
            spin_speed = 0
            spinning = False
            result_angle = 270 - angle % 360
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

        if i == selected_section:
            pygame.draw.polygon(screen, COLOR_YELLOW, [center, (x1, y1), (x2, y2)])
        elif i == last_section:
            pygame.draw.polygon(screen, COLOR_RED, [center, (x1, y1), (x2, y2)])
        else:
            pygame.draw.polygon(screen, COLOR_SKY_BLUE, [center, (x1, y1), (x2, y2)])

        # 섹션 텍스트 그리기
        text_angle = (start_angle + end_angle) / 2
        text_x = center[0] + int(radius / 1.5 * math.cos(text_angle))
        text_y = center[1] + int(radius / 1.5 * math.sin(text_angle))
        text_surface = font.render(section_texts[i], True, BLACK)
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)

    # 화살표 핀 그리기
    arrow_tip = (
        center[0],
        center[1] - radius + arrow_height
    )
    arrow_head_left = (
        center[0] - arrow_head_base,
        center[1] - radius + arrow_head_height
    )
    arrow_head_right = (
        center[0] + arrow_head_base,
        center[1] - radius + arrow_head_height
    )
    arrow_tail_left_top = (
        center[0] - arrow_tail_width // 2,
        center[1] - radius
    )
    arrow_tail_left_bottom = (
        center[0] - arrow_tail_width // 2,
        center[1] - radius + arrow_height
    )
    arrow_tail_right_top = (
        center[0] + arrow_tail_width // 2,
        center[1] - radius
    )
    arrow_tail_right_bottom = (
        center[0] + arrow_tail_width // 2,
        center[1] - radius + arrow_height
    )

    # 화살표 머리 (삼각형) 그리기
    pygame.draw.polygon(screen, COLOR_RED, [arrow_tip, arrow_head_right, arrow_head_left])
    # 화살표 꼬리 (직사각형) 그리기
    #pygame.draw.polygon(screen, COLOR_RED, [arrow_tail_left_top, arrow_tail_left_bottom, arrow_tail_right_bottom, arrow_tail_right_top])

    # 결과 텍스트 그리기
    if result_text:
        text_surface = font.render(result_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 50))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
