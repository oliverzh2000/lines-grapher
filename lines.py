import pygame
import sys
import datetime
from pygame import *
from pygame.locals import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
pygame.init()
clock = pygame.time.Clock()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = display.set_mode((width, height), FULLSCREEN)
# width, height = 800, 600
# screen = display.set_mode((width, height))

pygame.scrap.init()


def events():
    global camera_pan_x, camera_pan_y, camera_scale, trans_image_surf
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_EQUALS or event.key == K_MINUS:
                print("penis")
                if event.key == K_EQUALS and key.get_pressed()[K_EQUALS]:
                    camera_scale *= 1.4
                if event.key == K_MINUS and camera_scale > 1:
                    camera_scale /= 1.4
                transform_image()
                render()
            if event.key == K_HOME:
                camera_pan_x, camera_pan_y, camera_scale = 0, 0, 1
                transform_image()
                render()
            if event.key == K_z:
                if key.get_pressed()[K_LCTRL]:
                    undo_line()
        if event.type == MOUSEBUTTONDOWN and mouse.get_pressed()[0]:
            logic()
    if any(key.get_pressed()[button] for button in [K_RIGHT, K_LEFT, K_UP, K_DOWN]):
        if key.get_pressed()[K_RIGHT]:
            camera_pan_x -= 0.1 / camera_scale
        if key.get_pressed()[K_LEFT]:
            camera_pan_x += 0.1 / camera_scale
        if key.get_pressed()[K_UP]:
            camera_pan_y -= 0.1 / camera_scale
        if key.get_pressed()[K_DOWN]:
            camera_pan_y += 0.1 / camera_scale
        translate_image()
        render()


def render():
    screen.fill(WHITE)

    screen.blit(trans_image_surf, trans_image_rect)

    origin_x, origin_y = get_screen_coords(0, 0)
    draw.line(screen, RED, (0, origin_y), (width, origin_y))
    draw.line(screen, RED, (origin_x, 0), (origin_x, height))
    for line in lines:
        start, end = line
        draw.line(screen, GREEN, get_screen_coords(*start), get_screen_coords(*end), 5)
    display.update()


def transform_image():
    global trans_image_surf, trans_image_rect, camera_scale, max_camera_scale
    if max_camera_scale is None or camera_scale < max_camera_scale:
        try:
            trans_image_surf = transform.scale(image_surf, (int(image_width * image_scale * camera_scale),
                                                            int(image_height * image_scale * camera_scale)))
        except:
            camera_scale /= 1.4
            max_camera_scale = camera_scale
            transform_image()
        trans_image_rect = trans_image_surf.get_rect()
        trans_image_rect.center = get_screen_coords(0, 0)
    else:
        camera_scale = max_camera_scale


def translate_image():
    global trans_image_rect
    trans_image_rect.center = get_screen_coords(0, 0)


def logic():
    global prev_point
    x, y = get_original_coords(*mouse.get_pos())
    if prev_point and not key.get_pressed()[K_LSHIFT]:
        lines.append(((x, y), prev_point))
        scrap.put("text/plain", bytes(get_lin_equation(((x, y), prev_point), 0.001), encoding="UTF-8"))
        prev_point = x, y
    else:
        prev_point = x, y
    render()


def undo_line():
    if len(lines) > 0:
        lines.pop()
    render()


def export_lines():
    with open(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".txt", "w") as out_file:
        for line in lines:
            lin_equation = get_lin_equation(line, 0.001)
            if lin_equation:
                print(lin_equation)
                print(lin_equation, file=out_file)


def get_screen_coords(x, y):
    # Apply transformations.
    x = (x + camera_pan_x) * camera_scale
    y = (y + camera_pan_y) * camera_scale
    # Convert to screen co-ordinates (pixels).
    x = width / 2 + (x * height / 2)
    y = height / 2 - (y * height / 2)
    return x, y


def get_original_coords(x, y):
    # Convert pixels back to cartesian place co-ordinates.
    x = (x - width / 2) * 2 / height
    y = (-(y - height / 2)) * 2 / height
    # Undo transformations.
    x = x / camera_scale - camera_pan_x
    y = y / camera_scale - camera_pan_y
    return x, y


def get_lin_equation(line_seg, vertical_thres):
    start, end = line_seg
    x1, y1 = start
    x2, y2 = end
    if start != end:
        if abs(x2 - x1) < vertical_thres:
            avg_x, min_y, max_y = map(str, [round((x1 + x2) / 2, 4), round(min(y1, y2), 4), round(max(y1, y2), 4)])
            return "x=" + avg_x + "\left\{" + min_y + "<y<" + max_y + r"\right\}"
        else:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            m, b, min_x, max_x = map(str, [round(m, 4), round(b, 4), round(min(x1, x2), 4), round(max(x1, x2), 4)])
            return m + "x+" + b + "\left\{" + min_x + "<x<" + max_x + r"\right\}"
    return ""


try:
    image_surf = pygame.image.load(sys.argv[1]).convert()
except:
    print("Usage: python lines.py 'image name'")
    print("   or: lines.exe 'image name'")
    sys.exit()
image_width, image_height = image_surf.get_size()
trans_image_surf = image_surf
trans_image_rect = trans_image_surf.get_rect()

prev_point = None
lines = []
image_scale = height / image_height
camera_pan_x, camera_pan_y, camera_scale, max_camera_scale = 0, 0, 1, None

transform_image()
render()
try:
    while True:
        clock.tick(60)
        events()
finally:
    export_lines()
