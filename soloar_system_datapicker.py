import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PLANET_RADIUS = 30
ORBIT_RADIUS = 200  # Orbit radius from the center of the screen

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Solar System Datepicker')

# Planets initial positions and colors
sun_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
mercury_pos = (SCREEN_WIDTH // 2 + ORBIT_RADIUS, SCREEN_HEIGHT // 2)
venus_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + ORBIT_RADIUS)
earth_pos = (SCREEN_WIDTH // 2 - ORBIT_RADIUS, SCREEN_HEIGHT // 2)
planets = {
    'Mercury': {'angle': 0, 'color': GRAY, 'pos': list(mercury_pos)},
    'Venus': {'angle': 0, 'color': GREEN, 'pos': list(venus_pos)},
    'Earth': {'angle': 0, 'color': BLUE, 'pos': list(earth_pos)}
}

# Selected date
selected_year = 2024
selected_month = 7
selected_day = 1

# Fonts
font = pygame.font.Font(None, 36)

def draw_planet(name, angle, color):
    # Calculate position based on angle and orbit radius
    x = int(sun_pos[0] + ORBIT_RADIUS * math.cos(math.radians(angle)))
    y = int(sun_pos[1] - ORBIT_RADIUS * math.sin(math.radians(angle)))  # Negative sin because y-axis is flipped
    pygame.draw.circle(screen, color, (x, y), PLANET_RADIUS)

def draw_text(text, pos, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def update_display():
    screen.fill(BLACK)
    draw_text(f"Selected Date: {selected_year}-{selected_month}-{selected_day}", (20, 20))

    for planet, data in planets.items():
        draw_planet(planet, data['angle'], data['color'])

    pygame.display.flip()

# Dragging variables
dragging = False
selected_planet = None
offset_x = 0
offset_y = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for planet, data in planets.items():
                planet_pos = data['pos']
                if pygame.math.Vector2(x - planet_pos[0], y - planet_pos[1]).length() <= PLANET_RADIUS:
                    dragging = True
                    selected_planet = planet
                    offset_x = planet_pos[0] - x
                    offset_y = planet_pos[1] - y
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            selected_planet = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging and selected_planet:
                x, y = event.pos
                planets[selected_planet]['pos'][0] = x + offset_x
                planets[selected_planet]['pos'][1] = y + offset_y

                # Update selected date based on planet's position
                if selected_planet == 'Mercury':
                    selected_year += 1
                elif selected_planet == 'Venus':
                    selected_month = (selected_month % 12) + 1
                elif selected_planet == 'Earth':
                    selected_day += 1

                update_display()

    # Update planet angles (for animation or interaction)
    for planet, data in planets.items():
        data['angle'] = math.degrees(math.atan2(sun_pos[1] - data['pos'][1], data['pos'][0] - sun_pos[0]))
        if data['angle'] < 0:
            data['angle'] += 360

    update_display()

# Quit pygame
pygame.quit()
sys.exit()
