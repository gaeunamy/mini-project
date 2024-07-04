import pygame
import sys
import math
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interactive Date Picker")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Date settings
start_date = datetime(2020, 1, 1)
current_date = datetime(2020, 8, 31)

# Orbital parameters
orbit_radius = 200
sun_pos = (width // 2, height // 2)
earth_radius = 20
dragging = False

def calculate_earth_position(date):
    days_in_year = 365
    day_of_year = (date - start_date).days % days_in_year
    angle = 2 * math.pi * day_of_year / days_in_year
    x = sun_pos[0] + orbit_radius * math.cos(angle)
    y = sun_pos[1] + orbit_radius * math.sin(angle)
    return (x, y)

def calculate_date_from_position(pos):
    angle = math.atan2(pos[1] - sun_pos[1], pos[0] - sun_pos[0])
    if angle < 0:
        angle += 2 * math.pi
    days_in_year = 365
    day_of_year = int(angle / (2 * math.pi) * days_in_year)
    return start_date + timedelta(days=day_of_year)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            earth_pos = calculate_earth_position(current_date)
            distance = math.hypot(mouse_pos[0] - earth_pos[0], mouse_pos[1] - earth_pos[1])
            if distance < earth_radius:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_pos = pygame.mouse.get_pos()
            current_date = calculate_date_from_position(mouse_pos)
    
    screen.fill(BLACK)  # Clear screen with black
    
    # Draw orbit path
    pygame.draw.ellipse(screen, WHITE, (sun_pos[0] - orbit_radius, sun_pos[1] - orbit_radius, 2 * orbit_radius, 2 * orbit_radius), 1)

    # Draw Sun
    pygame.draw.circle(screen, YELLOW, sun_pos, 40)

    # Calculate and draw Earth position
    earth_pos = calculate_earth_position(current_date)
    pygame.draw.circle(screen, BLUE, (int(earth_pos[0]), int(earth_pos[1])), earth_radius)
    
    # Render and draw the current date
    font = pygame.font.SysFont(None, 36)
    date_text = font.render(current_date.strftime("%b %d, %Y"), True, WHITE)
    screen.blit(date_text, (20, 20))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
