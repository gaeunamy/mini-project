import pygame
import sys
import math
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interactive Solar System")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)

# Date settings
start_date = datetime(2020, 1, 1)
current_date = datetime.now()  # Set the current date to today's date
days_per_year = 365.25  # Average days per year, accounting for leap years

# Orbital parameters
sun_pos = (width // 2, height // 2)
sun_radius = 40

earth_orbit_radius = 200
earth_radius = 20
earth_initial_angle = math.radians(45)  # Start Earth at a 45-degree angle

moon_orbit_radius = 50
moon_radius = 10
moon_initial_angle = math.radians(90)  # Start Moon at a 90-degree angle

# Interaction variables
dragging = False

def calculate_earth_position(total_days):
    angle = -2 * math.pi * (total_days % days_per_year) / days_per_year + math.pi/2
    x = sun_pos[0] + earth_orbit_radius * math.cos(angle)
    y = sun_pos[1] - earth_orbit_radius * math.sin(angle)
    return (x, y)

def calculate_moon_position(total_days):
    earth_pos = calculate_earth_position(total_days)
    moon_angle = -2 * math.pi * (total_days % (days_per_year / 12)) / (days_per_year / 12) + math.pi/2
    moon_x = earth_pos[0] + moon_orbit_radius * math.cos(moon_angle)
    moon_y = earth_pos[1] - moon_orbit_radius * math.sin(moon_angle)
    return (moon_x, moon_y)

def calculate_days_from_position(pos, is_moon=False):
    dx = pos[0] - sun_pos[0]
    dy = sun_pos[1] - pos[1]
    angle = math.atan2(dy, dx)
    if angle < 0:
        angle += 2 * math.pi
    angle = (math.pi/2 - angle) % (2 * math.pi)
    days = angle / (2 * math.pi) * days_per_year
    
    if is_moon:
        earth_pos = calculate_earth_position(total_days)
        dx = pos[0] - earth_pos[0]
        dy = pos[1] - earth_pos[1]
        angle = math.atan2(dy, dx)
        if angle < 0:
            angle += 2 * math.pi
        angle = (math.pi/2 - angle) % (2 * math.pi)
        days = angle / (2 * math.pi) * (days_per_year / 12)
    
    return days

def update_date(total_days):
    return start_date + timedelta(days=int(total_days))

# Main loop
total_days = (current_date - start_date).days
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            earth_pos = calculate_earth_position(total_days)
            moon_pos = calculate_moon_position(total_days)
            
            # Check if the mouse is clicking on the Earth or Moon
            if math.hypot(mouse_pos[0] - earth_pos[0], mouse_pos[1] - earth_pos[1]) < earth_radius:
                dragging = True
            elif math.hypot(mouse_pos[0] - moon_pos[0], mouse_pos[1] - moon_pos[1]) < moon_radius:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_pos = pygame.mouse.get_pos()
            days_in_orbit = calculate_days_from_position(mouse_pos)
            years_passed = int(total_days // days_per_year)
            total_days = years_passed * days_per_year + days_in_orbit
            current_date = update_date(total_days)
    
    screen.fill(BLACK)  # Clear screen with black
    
    # Draw Sun
    pygame.draw.circle(screen, YELLOW, sun_pos, sun_radius)
    
    # Draw Earth orbit path
    pygame.draw.ellipse(screen, WHITE, (sun_pos[0] - earth_orbit_radius, sun_pos[1] - earth_orbit_radius, 2 * earth_orbit_radius, 2 * earth_orbit_radius), 1)
    
    # Calculate and draw Earth position
    earth_pos = calculate_earth_position(total_days)
    pygame.draw.circle(screen, BLUE, (int(earth_pos[0]), int(earth_pos[1])), earth_radius)
    
    # Draw Moon orbit path around Earth
    pygame.draw.ellipse(screen, GRAY, (earth_pos[0] - moon_orbit_radius, earth_pos[1] - moon_orbit_radius, 2 * moon_orbit_radius, 2 * moon_orbit_radius), 1)
    
    # Calculate and draw Moon position relative to Earth
    moon_pos = calculate_moon_position(total_days)
    pygame.draw.circle(screen, GRAY, (int(moon_pos[0]), int(moon_pos[1])), moon_radius)
    
    # Render and draw the current date
    font = pygame.font.SysFont(None, 36)
    date_text = font.render(current_date.strftime("%b %d, %Y"), True, WHITE)
    screen.blit(date_text, (20, 20))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
