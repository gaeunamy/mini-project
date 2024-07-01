import pygame
import math
import time
import imageio

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Number Hand Clock")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)  # 추가: 빨간색

# Clock parameters
center = (width // 2, height // 2)
radius = 250

# Font settings
font = pygame.font.SysFont(None, 36)

def draw_hand(angle, length, number, color, segments):
    for i in range(1, segments + 1):
        x = center[0] + length * math.cos(math.radians(angle)) * (i / segments)
        y = center[1] - length * math.sin(math.radians(angle)) * (i / segments)
        if angle == 90:  # 추가: 초침이 0초일 때
            text_color = red  # 빨간색으로 설정
        else:
            text_color = color
        text = font.render(str(number), True, text_color)
        text_rect = text.get_rect(center=(x, y))
        window.blit(text, text_rect)

def draw_clock():
    window.fill(white)
    
    # Get current time
    current_time = time.localtime()
    hours = current_time.tm_hour % 12
    minutes = current_time.tm_min
    seconds = current_time.tm_sec
    
    # Calculate angles
    second_angle = 90 - (seconds * 6)
    minute_angle = 90 - (minutes * 6 + seconds * 0.1)
    hour_angle = 90 - (hours * 30 + minutes * 0.5)
    
    # Draw hands with numbers
    draw_hand(hour_angle, radius * 0.3, hours, black, 3)  # 시침 길이 조정
    draw_hand(minute_angle, radius * 0.6, minutes, black, 5)  # 분침 길이 조정
    draw_hand(second_angle, radius * 0.7, seconds, black, 6)  # 초침 길이 조정
    
    # Draw clock border
    pygame.draw.rect(window, black, (center[0] - radius, center[1] - radius, radius * 2, radius * 2), 3)
    
    pygame.display.update()
    
    return pygame.surfarray.array3d(window)

# Main loop
running = True
clock = pygame.time.Clock()

# List to store frames for the video
frames = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get current second
    current_time = time.localtime()
    seconds = current_time.tm_sec
    
    frame = draw_clock()
    frames.append(frame)
    
    # Check if seconds is between 51 and 0 to change color
    if seconds >= 51 or seconds == 0:
        draw_hand(90, radius * 0.7, seconds, black, 6)  # 초침 길이 조정 및 빨간색 설정
    
    clock.tick(1)

pygame.quit()

# Save frames to a video file
imageio.mimsave('clock.mp4', frames, fps=1)
