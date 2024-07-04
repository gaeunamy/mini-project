import pygame
import sys
import math
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Date settings
start_date = datetime(2020, 1, 1)
current_date = datetime(2020, 8, 31)

# Orbital parameters
orbit_radius = 200
sun_pos = (width // 2, height // 2)

def calculate_earth_position(date):
    days_in_year = 365
    day_of_year = (date - start_date).days % days_in_year
    angle = 2 * math.pi * day_of_year / days_in_year
    x = sun_pos[0] + orbit_radius * math.cos(angle)
    y = sun_pos[1] + orbit_radius * math.sin(angle)
    return (x, y)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_date -= timedelta(days=1)
            elif event.key == pygame.K_RIGHT:
                current_date += timedelta(days=1)
    
    screen.fill((0, 0, 0))  # Clear screen with black
    
    # Draw orbit path
    pygame.draw.circle(screen, (255, 255, 255), sun_pos, orbit_radius, 1)

    # Draw Sun
    pygame.draw.circle(screen, (255, 255, 0), sun_pos, 50)

    # Calculate and draw Earth position
    earth_pos = calculate_earth_position(current_date)
    pygame.draw.circle(screen, (0, 0, 255), (int(earth_pos[0]), int(earth_pos[1])), 20)
    
    # Render and draw the current date
    font = pygame.font.SysFont(None, 36)
    date_text = font.render(current_date.strftime("%b %d, %Y"), True, (255, 255, 255))
    screen.blit(date_text, (20, 20))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
