import pygame
import requests
import json
import random
import time

# OpenWeatherMap API 설정
API_KEY = "0b4e2fd700cc120a631ac8e90b157d6a"
CITY = "Busan"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Pygame 초기화
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("실시간 날씨 시각화")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# 날씨 데이터 가져오기
def get_weather():
    response = requests.get(URL)
    data = json.loads(response.text)
    return data

# 비 효과
class Raindrop:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, -10)
        self.speed = random.randint(5, 15)
        self.size = random.randint(2, 5)

    def fall(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, WIDTH)

    def draw(self):
        pygame.draw.line(screen, BLUE, (self.x, self.y), (self.x, self.y + self.size), 1)

# 구름 효과
class Cloud:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(50, 200)
        self.speed = random.uniform(0.5, 1.5)
        self.size = random.randint(50, 100)

    def move(self):
        self.x += self.speed
        if self.x > WIDTH + 100:
            self.x = -100

    def draw(self):
        pygame.draw.circle(screen, GRAY, (int(self.x), int(self.y)), self.size)

# 눈 효과
class Snowflake:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, -10)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(3, 7)

    def fall(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, WIDTH)

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)

# 태양의 빛나는 효과 그리기
def draw_sun_with_glow(x, y, radius):
    # 반투명한 빛나는 레이어 추가
    for i in range(5, 50, 10):  # 여러 겹의 반투명 원을 그려서 빛나는 효과 만들기
        glow_color = (255, 255, 0, 128 - i * 2)  # 반투명한 노란색
        glow_surface = pygame.Surface((radius * 2 + i * 2, radius * 2 + i * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, glow_color, (radius + i, radius + i), radius + i)
        screen.blit(glow_surface, (x - radius - i, y - radius - i))
    
    # 태양 그리기
    pygame.draw.circle(screen, YELLOW, (x, y), radius)

# 번개 효과 클래스
class Lightning:
    def __init__(self):
        self.timer = 0
        self.lightning_duration = random.uniform(0.1, 0.3)
        self.lightning_gap = random.uniform(2, 5)  # 번개 간격

    def flash(self):
        current_time = time.time()
        if current_time - self.timer > self.lightning_gap:
            self.lightning_gap = random.uniform(2, 5)
            self.timer = current_time
            return True
        return False

    def draw(self):
        # 랜덤한 번개 위치 및 크기
        start_x = random.randint(100, WIDTH - 100)
        start_y = random.randint(0, HEIGHT // 2)

        lightning_points = [(start_x, start_y)]  # 번개의 시작점
        # 번개를 위한 지그재그 선 그리기
        for _ in range(5):  # 5개의 지그재그 포인트 추가
            new_x = lightning_points[-1][0] + random.randint(-20, 20)
            new_y = lightning_points[-1][1] + random.randint(20, 60)
            lightning_points.append((new_x, new_y))

        # 번개가 끝나는 점 추가
        end_x = lightning_points[-1][0] + random.randint(-20, 20)
        end_y = HEIGHT
        lightning_points.append((end_x, end_y))

        # 번개 그리기
        screen.fill(BLACK)  # 배경을 검은색으로 설정
        pygame.draw.lines(screen, YELLOW, False, lightning_points, 3)  # 노란색 번개 그리기
        pygame.display.flip()

        # 번개 번쩍임 효과 (화면을 하얗게 번쩍이게)
        time.sleep(self.lightning_duration)  # 번개 지속 시간
        screen.fill(WHITE)  # 화면을 흰색으로 번쩍이게
        pygame.display.flip()
        time.sleep(0.1)  # 잠깐 동안 하얀 화면 유지
        screen.fill(BLACK)  # 화면을 다시 검은색으로 설정

# 메인 루프
def main():
    clock = pygame.time.Clock()
    raindrops = [Raindrop() for _ in range(100)]
    clouds = [Cloud() for _ in range(5)]
    snowflakes = [Snowflake() for _ in range(100)]
    lightning = Lightning()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        # 날씨 데이터 가져오기 (실제 사용 시 API 호출 빈도 제한에 주의)
        weather = get_weather()
        temp = weather['main']['temp']
        description = weather['weather'][0]['main']

        # 날씨에 따른 효과 그리기
        if description.lower() in ['rain', 'drizzle']:
            for drop in raindrops:
                drop.fall()
                drop.draw()
        elif description.lower() == 'clear':
            # 맑은 날씨일 때 태양과 빛나는 효과 그리기
            draw_sun_with_glow(WIDTH - 100, 100, 50)
        elif description.lower() == 'clouds':
            # 구름 많은 날씨일 때 구름 그리기
            for cloud in clouds:
                cloud.move()
                cloud.draw()
        elif description.lower() == 'snow':
            # 눈 내리는 날씨일 때 눈송이 그리기
            for flake in snowflakes:
                flake.fall()
                flake.draw()
        elif description.lower() == 'thunderstorm':
            # 천둥 번개 그리기
            if lightning.flash():
                lightning.draw()
        elif description.lower() == 'fog':
            # 안개 효과 (화면 전체에 안개를 추가)
            fog_surface = pygame.Surface((WIDTH, HEIGHT))
            fog_surface.set_alpha(120)  # 투명도 설정
            fog_surface.fill(GRAY)
            screen.blit(fog_surface, (0, 0))

        # 온도 표시
        font = pygame.font.Font(None, 36)
        temp_text = font.render(f"Temperature: {temp}°C", True, BLACK)
        screen.blit(temp_text, (10, 10))

        # 날씨 설명 표시
        desc_text = font.render(f"Weather: {description}", True, BLACK)
        screen.blit(desc_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
