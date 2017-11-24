import struct
import sys
import os

import pygame
from pygame import *
from pygame.locals import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
pygame.init()
clock = pygame.time.Clock()

# width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
# screen = display.set_mode((width, height), FULLSCREEN)
width, height = 800, 600
screen = display.set_mode((width, height))
origin_x, origin_y = 0, 0

pygame.scrap.init()

image_surf = pygame.image.load(r"C:\Users\Oliver\Downloads\drawn-bulding-city-skyline-12.gif").convert()
trans_image_surf = image_surf

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
                if event.key == K_EQUALS:
                    camera_scale *= 1.4
                if event.key == K_MINUS:
                    camera_scale /= 1.4
        if event.type == MOUSEBUTTONDOWN and mouse.get_pressed()[0]:
            logic()
    if any(key.get_pressed()[button] for button in [K_RIGHT, K_LEFT, K_UP, K_DOWN]):
        if key.get_pressed()[K_RIGHT]:
            camera_pan_x -= 0.1
        if key.get_pressed()[K_LEFT]:
            camera_pan_x += 0.1
        if key.get_pressed()[K_UP]:
            camera_pan_y -= 0.1
        if key.get_pressed()[K_DOWN]:
            camera_pan_y += 0.1


def render_background():
    screen.fill(WHITE)

    image_width, image_height = image_surf.get_size()
    image_scale = min(width / image_width, height / image_height)
    trans_image_surf = transform.scale(image_surf, (int(image_width * image_scale * camera_scale),
                                                    int(image_height * image_scale * camera_scale)))
    trans_image_rect = trans_image_surf.get_rect()
    trans_image_rect.center = get_camera_coords(0, 0, width, height)
    screen.blit(trans_image_surf, trans_image_rect)
    origin_x, origin_y = get_camera_coords(0, 0, width, height)
    draw.line(screen, RED, (0, origin_y), (width, origin_y))
    draw.line(screen, RED, (origin_x, 0), (origin_x, height))
    for point in points:
        draw_point(*point)
    display.update()

def logic():
    print(get_original_coords(*mouse.get_pos(), width, height))

def draw_point(x, y):
    x, y = get_camera_coords(x, y, width, height)
    draw.circle(screen, GREEN, (int(x), int(y)), 3)

def get_camera_coords(x, y, width, height):
    # Apply transformations.
    x = (x + camera_pan_x) * camera_scale
    y = (y + camera_pan_y) * camera_scale
    # Convert to screen co-ordinates (pixels).
    x = width / 2 + (x * min(width, height) / 2)
    y = height / 2 - (y * min(width, height) / 2)
    return x, y

def get_original_coords(x, y, width, height):
    # Convert pixels back to cartesian place co-ordinates.
    x = (x - width / 2) * 2 / min(width, height)
    y = (-(y - height / 2)) * 2 / min(width, height)
    # Undo transformations.
    x = x / camera_scale - camera_pan_x
    y = y / camera_scale - camera_pan_y
    return x, y

# def transformed(x, y, width, height):
#     x = (x + camera_pan_x) * camera_scale
#     y = (y + camera_pan_y) * camera_scale
#     return x, y
# def untransformed(x, y, width, height):
#     x = x / camera_scale - camera_pan_x
#     y = y / camera_scale - camera_pan_y
#     return x, y
# def model_to_screen(x, y, width, height):
#     x = width / 2 + (x * min(width, height) / 2)
#     y = height / 2 - (y * min(width, height) / 2)
#     return x, y
# def screen_to_model(x, y, width, height):
#     x = (x - width / 2) * 2 / min(width, height)
#     y = (-(y - height / 2)) * 2 / min(width, height)
#     return x, y


points = [(0, 0), (1, 1), (2, 2), (4, 4), (0.1, 0.1), (0.5, 0.5), (0, 0.3), (0.5, 0.3), (1, 0.3), (1.5, 0.3), (2, 0.3)]
camera_pan_x, camera_pan_y, camera_scale = 0, 0, 1


render_background()

while True:
    clock.tick(60)
    render_background()
    # refactor origin mappgin and transformation
    events()
