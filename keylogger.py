import pygame

pygame.init()

WIDTH, HEIGHT = 800, 400  # Height를 조금 높임
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive English Keyboard")

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

keys = [
    ['esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', '🔒'],
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '←'],
    ['tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
    ['caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'enter'],
    ['shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'shift'],
    ['fn', 'control', 'option', 'command', ' ', 'command', 'option', '◀', '▲', '▼', '▶']
]

typed_text = ""
caps_on = False

def draw_key(screen, x, y, width, height, text, is_active=False):
    color = RED if is_active else GRAY
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 1)
    font = pygame.font.Font(None, int(height * 0.4))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

def draw_text(screen, text, x, y, font, color=BLACK, max_width=None):
    lines = text.split('\n')
    line_height = font.get_height()
    for line in lines:
        words = line.split(' ')
        if max_width is None:
            rendered_line = ' '.join(words)
            text_surface = font.render(rendered_line, True, color)
            screen.blit(text_surface, (x, y))
            y += line_height
        else:
            rendered_line = ''
            for word in words:
                test_line = f"{rendered_line} {word}".strip()
                if font.size(test_line)[0] <= max_width:
                    rendered_line = test_line
                else:
                    text_surface = font.render(rendered_line, True, color)
                    screen.blit(text_surface, (x, y))
                    y += line_height
                    rendered_line = word
            if rendered_line:
                text_surface = font.render(rendered_line, True, color)
                screen.blit(text_surface, (x, y))
                y += line_height

running = True
key_rects = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, text in key_rects:
                if rect.collidepoint(event.pos):
                    if text == '←':
                        typed_text = typed_text[:-1]  # Backspace
                    elif text == 'caps':
                        caps_on = not caps_on  # Toggle Caps Lock
                    elif text == 'enter':
                        typed_text += '\n'  # Enter key
                    elif text not in ['esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', '🔒', 'tab', 'shift', 'fn', 'control', 'option', 'command', '◀', '▲', '▼', '▶']:
                        if text.isalpha():
                            typed_text += text.upper() if caps_on else text.lower()
                        else:
                            typed_text += text

    screen.fill(WHITE)

    # 모니터 프레임 그리기
    monitor_x = 50
    monitor_y = 20
    monitor_width = WIDTH - 100
    monitor_height = 100
    pygame.draw.rect(screen, BLACK, (monitor_x, monitor_y, monitor_width, monitor_height), 5)
    pygame.draw.rect(screen, GRAY, (monitor_x + 5, monitor_y + 5, monitor_width - 10, monitor_height - 10))

    # 모니터 안에 텍스트 표시
    font = pygame.font.Font(None, 36)
    draw_text(screen, typed_text, monitor_x + 10, monitor_y + 10, font, BLACK, monitor_width - 20)

    num_rows = len(keys)
    num_cols = max(len(row) for row in keys)
    
    key_width = WIDTH / num_cols
    key_height = (HEIGHT - 150) / num_rows  # 모니터 영역을 감안하여 키 높이를 조정
    
    key_rects.clear()

    for row_index, row in enumerate(keys):
        y = monitor_height + 50 + row_index * key_height
        x = 0
        row_width = 0
        for key in row:
            if key == 'shift':
                width = key_width * 2.3 if row_index == 4 else key_width * 1.5
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
            row_width += width

        extra_space = WIDTH - row_width
        if row_index == 4:  # Shift key row
            shift_extra = extra_space / 2
            for i, key in enumerate(row):
                if key == 'shift':
                    width = key_width * 2.3 + shift_extra
                else:
                    width = key_width
                rect = draw_key(screen, x, y, width, key_height, key, key == 'caps' and caps_on)
                key_rects.append((rect, key))
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
                rect = draw_key(screen, x, y, width, key_height, key, key == 'caps' and caps_on)
                key_rects.append((rect, key))
                x += width

    pygame.display.flip()

pygame.quit()
