import pygame
import sys
import math
from datetime import datetime, timedelta
import imageio

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
current_date = datetime.now()
years_passed = current_date.year - start_date.year
days_in_year = (current_date - datetime(current_date.year, 1, 1)).days

# Orbital parameters
sun_pos = (width // 2, height // 2)
sun_radius = 40

earth_orbit_radius = 200
earth_radius = 20

moon_orbit_radius = 50
moon_radius = 10

# Interaction variables
dragging = False
prev_angle = 0

def calculate_earth_position(years, days):
    angle = 2 * math.pi * days / 365 - math.pi/2  # Changed sign and initial angle
    x = sun_pos[0] + earth_orbit_radius * math.cos(angle)
    y = sun_pos[1] + earth_orbit_radius * math.sin(angle)  # Changed to addition
    return (x, y)

def calculate_moon_position(years, days):
    earth_pos = calculate_earth_position(years, days)
    moon_angle = 2 * math.pi * (days % (365 / 12)) / (365 / 12) - math.pi/2  # Changed sign and initial angle
    moon_x = earth_pos[0] + moon_orbit_radius * math.cos(moon_angle)
    moon_y = earth_pos[1] + moon_orbit_radius * math.sin(moon_angle)  # Changed to addition
    return (moon_x, moon_y)

def calculate_angle_from_position(pos):
    dx = pos[0] - sun_pos[0]
    dy = pos[1] - sun_pos[1]  # Changed to match new coordinate system
    angle = math.atan2(dy, dx)
    return angle

def update_date(years, days):
    return start_date.replace(year=start_date.year + years) + timedelta(days=int(days))

# Main loop
running = True
frames = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            earth_pos = calculate_earth_position(years_passed, days_in_year)
            if math.hypot(mouse_pos[0] - earth_pos[0], mouse_pos[1] - earth_pos[1]) < earth_radius:
                dragging = True
                prev_angle = calculate_angle_from_position(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_pos = pygame.mouse.get_pos()
            current_angle = calculate_angle_from_position(mouse_pos)
            angle_diff = current_angle - prev_angle
            
            # Adjust for angle wrap-around
            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            elif angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            days_change = angle_diff / (2 * math.pi) * 365
            days_in_year += days_change
            
            if days_in_year >= 365:
                years_passed += 1
                days_in_year -= 365
            elif days_in_year < 0:
                years_passed -= 1
                days_in_year += 365
            
            current_date = update_date(years_passed, days_in_year)
            prev_angle = current_angle

    screen.fill(BLACK)  # Clear screen with black
    
    # Draw Sun
    pygame.draw.circle(screen, YELLOW, sun_pos, sun_radius)
    
    # Draw Earth orbit path
    pygame.draw.ellipse(screen, WHITE, (sun_pos[0] - earth_orbit_radius, sun_pos[1] - earth_orbit_radius, 2 * earth_orbit_radius, 2 * earth_orbit_radius), 1)
    
    # Calculate and draw Earth position
    earth_pos = calculate_earth_position(years_passed, days_in_year)
    pygame.draw.circle(screen, BLUE, (int(earth_pos[0]), int(earth_pos[1])), earth_radius)
    
    # Draw Moon orbit path around Earth
    pygame.draw.ellipse(screen, GRAY, (earth_pos[0] - moon_orbit_radius, earth_pos[1] - moon_orbit_radius, 2 * moon_orbit_radius, 2 * moon_orbit_radius), 1)
    
    # Calculate and draw Moon position relative to Earth
    moon_pos = calculate_moon_position(years_passed, days_in_year)
    pygame.draw.circle(screen, GRAY, (int(moon_pos[0]), int(moon_pos[1])), moon_radius)
    
    # Render and draw the current date
    font = pygame.font.SysFont(None, 36)
    date_text = font.render(current_date.strftime("%b %d, %Y"), True, WHITE)
    screen.blit(date_text, (20, 20))
    
    # Capture current frame
    pygame.display.flip()
    pygame.image.save(screen, "frame.png")  # Save frame as PNG image
    frames.append(imageio.imread("frame.png"))  # Append frame to list

# Save frames as GIF using imageio
imageio.mimsave('solar_system_simulation.gif', frames)

pygame.quit()
sys.exit()
