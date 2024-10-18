import pygame
import random
import colorsys
import math

# Pygame 초기화
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("유전 알고리즘 시뮬레이션")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 생물체 클래스
class Organism:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 10
        self.speed = random.uniform(1, 3)
        self.direction = random.uniform(0, 2 * 3.14159)

    def move(self):
        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)
        
        # 화면 경계 처리
        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def mutate(self):
        h, s, v = colorsys.rgb_to_hsv(*[x/255.0 for x in self.color])
        h = (h + random.uniform(-0.1, 0.1)) % 1.0
        s = max(0, min(1, s + random.uniform(-0.1, 0.1)))
        v = max(0, min(1, v + random.uniform(-0.1, 0.1)))
        self.color = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v))

# 환경 클래스
class Environment:
    def __init__(self):
        self.target_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def evaluate_fitness(self, organism):
        return 1 - (sum((a - b) ** 2 for a, b in zip(organism.color, self.target_color)) / (3 * 255 ** 2))

# 초기 생물체 생성
def create_initial_population(size):
    return [Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT),
                     (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            for _ in range(size)]

# 메인 루프
def main():
    clock = pygame.time.Clock()
    population = create_initial_population(50)
    environment = Environment()
    generation = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        # 생물체 이동 및 그리기
        for organism in population:
            organism.move()
            organism.draw()

        # 적합도 평가 및 선택
        fitnesses = [environment.evaluate_fitness(org) for org in population]
        total_fitness = sum(fitnesses)
        
        if total_fitness > 0:
            probabilities = [f / total_fitness for f in fitnesses]
            new_population = random.choices(population, weights=probabilities, k=len(population))
        else:
            new_population = random.choices(population, k=len(population))

        # 돌연변이
        for organism in new_population:
            if random.random() < 0.1:  # 10% 확률로 돌연변이 발생
                organism.mutate()

        population = new_population
        generation += 1

        # 정보 표시
        font = pygame.font.Font(None, 36)
        gen_text = font.render(f"Generation: {generation}", True, BLACK)
        target_text = font.render(f"Target Color: RGB{environment.target_color}", True, BLACK)
        screen.blit(gen_text, (10, 10))
        screen.blit(target_text, (10, 50))

        # 목표 색상 표시
        pygame.draw.rect(screen, environment.target_color, (WIDTH - 100, 10, 90, 90))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()