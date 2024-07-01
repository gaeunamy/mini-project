import pygame
import sys

pygame.init()

# 화면 설정
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('춤추는 산타')

# 이미지 로드
santa_img = pygame.image.load('santa.png')
santa_rect = santa_img.get_rect()
santa_rect.center = (400, 300)  # 초기 위치 설정

# 움직임 변수 설정
dx = 5

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 산타의 위치 업데이트
    santa_rect.x += dx

    # 화면 경계에 닿으면 방향 전환
    if santa_rect.right >= 800 or santa_rect.left <= 0:
        dx = -dx

    # 화면 지우기
    screen.fill((255, 255, 255))

    # 산타 이미지 그리기
    screen.blit(santa_img, santa_rect)

    # 화면 업데이트
    pygame.display.flip()

    # 프레임 속도 조절
    pygame.time.Clock().tick(30)  # 초당 30 프레임

pygame.quit()
sys.exit()
