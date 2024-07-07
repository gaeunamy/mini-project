import pygame

pygame.init()

WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("English Keyboard")

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

keys = [
    ['esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', '🔒'],
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '←'],
    ['tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
    ['caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'enter'],
    ['shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'shift'],
    ['fn', 'control', 'option', 'command', ' ', 'command', 'option', '◀', '▲', '▼', '▶']
]

def draw_key(screen, x, y, width, height, text):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 1)
    font = pygame.font.Font(None, int(height * 0.4))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surface, text_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    num_rows = len(keys)
    num_cols = max(len(row) for row in keys)
    
    key_width = WIDTH / num_cols
    key_height = HEIGHT / num_rows
    
    for row_index, row in enumerate(keys):
        y = row_index * key_height
        x = 0
        row_width = 0
        for key in row:
            if key == 'shift':
                width = key_width * 2.3 if row_index == 4 else key_width * 1.5
            elif key == 'tab':
                width = key_width * 1.3  # Reduced tab key size
            elif key in ['caps', 'fn', 'control', 'option', 'command']:
                width = key_width * 1.5
            elif key == ' ':
                width = key_width * 5
            elif key == 'enter':
                width = key_width * 2
            else:
                width = key_width
            row_width += width

        # Adjust keys to fill the row
        extra_space = WIDTH - row_width
        if row_index == 4:  # Shift key row
            shift_extra = extra_space / 2
            for i, key in enumerate(row):
                if key == 'shift':
                    width = key_width * 2.3 + shift_extra
                else:
                    width = key_width
                draw_key(screen, x, y, width, key_height, key)
                x += width
        else:
            extra_per_key = extra_space / len(row)
            for key in row:
                if key == 'shift':
                    width = key_width * 2.3
                elif key == 'tab':
                    width = key_width * 1.3
                elif key in ['caps', 'fn', 'control', 'option', 'command']:
                    width = key_width * 1.5
                elif key == ' ':
                    width = key_width * 5
                elif key == 'enter':
                    width = key_width * 2
                else:
                    width = key_width
                width += extra_per_key
                draw_key(screen, x, y, width, key_height, key)
                x += width

    pygame.display.flip()

pygame.quit()