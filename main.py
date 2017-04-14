import pygame
import sys
import os
import tkinter as tk
from tkinter import filedialog

pygame.init()

running = True

sw, sh = (650,900)
screen = pygame.display.set_mode((sw, sh), pygame.DOUBLEBUF)

clock = pygame.time.Clock()

res_folder = "res"
folders = ["Onesies", "Headgear", "Hair", "Glasses", "Beards", "Tops", "Shoes", "Bottoms", "Underfoot"]
button_pos_l = [(75,515), (105,365), (75,390), (115,410), (85,430), (105,485), (90,660), (105,550), (60,685)]
button_pos_r = [(545,515), (515,365), (545,390), (505,410), (535, 430), (515,485), (530,660), (515,550), (560,685)]
character_pos = (176,325)
light_pos = (100,115)
logo_pos = (35,20)
reset_pos = (130,790)
light_button_pos = (85,810)
male_pos = (455,810)
female_pos = (530,810)
photo_pos = (270,790)
stage_pos = (175,630)

title_button_pos = (445,365)

root = tk.Tk()
root.withdraw()

accessories = {}
acc_folder = os.path.join(res_folder, "Accessoirs")
for gender in ("Male", "Female", "Genderfck"):
    accs = {}
    for folder in folders:
        imgs = []
        fol = os.path.join(acc_folder, gender, folder)
        if os.path.exists(fol):
            for filename in os.listdir(fol):
                imgs.append(pygame.image.load(os.path.join(fol, filename)).convert_alpha())
        accs[folder] = imgs
    accessories[gender] = accs

male_character = pygame.image.load(os.path.join(acc_folder, "Male", "Character.png")).convert_alpha()
female_character = pygame.image.load(os.path.join(acc_folder, "Female", "Character.png")).convert_alpha()

for k, v in accessories["Genderfck"].items():
    accessories["Male"][k].extend(v)
    accessories["Female"][k].extend(v)

interface = {}
int_folder = os.path.join(res_folder, "Interface")
for filename in os.listdir(int_folder):
    interface[filename[:-4]] = pygame.image.load(os.path.join(int_folder, filename)).convert_alpha()

gender = "Male"
selected = [None] * len(folders)
onesie_index = folders.index("Onesies")
lights = True

button_rects = []
button_size = interface["Pfeil-rechts"].get_size()
for pos_l, pos_r in zip(button_pos_l, button_pos_r):
    button_rects.append((pygame.Rect(pos_l, button_size), pygame.Rect(pos_r, button_size)))

light_rect = pygame.Rect(light_button_pos, interface["Light"].get_size())
reset_rect = pygame.Rect(reset_pos, interface["Reset"].get_size())
photo_rect = pygame.Rect(photo_pos, interface["Photo"].get_size())
male_rect = pygame.Rect(male_pos, interface["Gender-m"].get_size())
female_rect = pygame.Rect(female_pos, interface["Gender-f"].get_size())


def render_character(target, pos):
    if gender == "Male":
        target.blit(male_character, pos)
    else:
        target.blit(female_character, pos)

    #if selected[onesie_index] is not None:
    #    target.blit(accessories[gender]["Onesies"][selected[onesie_index]], pos)
    #else:
    for folder, sel in reversed(list(zip(folders, selected))):
        if sel is None:
            continue
        target.blit(accessories[gender][folder][sel], pos)


def draw_button(target, name, rect, mousepos, buttondown):
    final_name = name
    if rect.collidepoint(mousepos):
        if buttondown:
            final_name += "-click"
        else:
            final_name += "-hover"
    target.blit(interface[final_name], rect.topleft)

titlescreen = True
timer = 0
blink_ms = 600
blink_on = False
while titlescreen:
    dt = clock.tick(60)

    if pygame.event.get(pygame.QUIT):
        titlescreen = False
        running = False

    if pygame.event.get(pygame.MOUSEBUTTONDOWN):
        titlescreen = False

    screen.blit(interface["Titlescreen-Back"], (0,0))

    timer += dt
    if timer > blink_ms:
        blink_on = not blink_on
        timer = 0
    if blink_on:
        screen.blit(interface["Title-Arrow-blink01"], title_button_pos)
    else:
        screen.blit(interface["Title-Arrow-blink02"], title_button_pos)

    pygame.event.clear()

    pygame.display.flip()


while running:
    dt = clock.tick(60)

    if pygame.event.get(pygame.QUIT):
        running = False

    screen.fill((0,0,0))

    mx, my = pygame.mouse.get_pos()

    mousedown = False
    downevents = pygame.event.get(pygame.MOUSEBUTTONDOWN)
    pygame.event.clear()
    for down in downevents:
        if not down.button == 1:
            continue
        mousedown = True
        for i, (folder, (butt_l, butt_r)) in enumerate(zip(folders, button_rects)):
            diff = 1
            if butt_l.collidepoint(down.pos):
                diff = -1
            elif not butt_r.collidepoint(down.pos):
                continue
            l = len(accessories[gender][folder])
            if selected[i] is None and l != 0:
                if diff == 1:
                    selected[i] = 0
                else:
                    selected[i] = l-1
            elif (selected[i] == 0 and diff == -1) or (selected[i] == l-1 and diff == 1):
                selected[i] = None
            else:
                selected[i] += diff

        if light_rect.collidepoint(down.pos):
            lights = not lights
        if reset_rect.collidepoint(down.pos):
            selected = [None] * len(folders)
        if photo_rect.collidepoint(down.pos):
            filename = filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"),))
            if not filename.endswith(".png"):
                filename += ".png"
            path = os.path.normpath(filename)
            out = pygame.Surface(male_character.get_size(), pygame.SRCALPHA)
            render_character(out, (0,0))
            pygame.image.save(out, path)
            del out
        if male_rect.collidepoint(down.pos) and not gender == "Male":
            gender = "Male"
            selected = [None] * len(folders)
        if female_rect.collidepoint(down.pos) and not gender == "Female":
            gender = "Female"
            selected = [None] * len(folders)


    screen.blit(interface["Logo"], logo_pos)
    if lights:
        screen.blit(interface["Light-left"], light_pos)
        screen.blit(interface["Light-right"], light_pos)
        screen.blit(interface["Light-click"], light_button_pos)
    else:
        draw_button(screen, "Light", light_rect, (mx, my), mousedown)

    if gender == "Male":
        screen.blit(interface["Stage-m"], stage_pos)
        screen.blit(interface["Gender-m-click"], male_pos)
        draw_button(screen, "Gender-f", female_rect, (mx, my), mousedown)
    else:
        screen.blit(interface["Stage-f"], stage_pos)
        screen.blit(interface["Gender-f-click"], female_pos)
        draw_button(screen, "Gender-m", male_rect, (mx, my), mousedown)

    draw_button(screen, "Reset", reset_rect, (mx, my), mousedown)
    draw_button(screen, "Photo", photo_rect, (mx, my), mousedown)

    render_character(screen, character_pos)

    for left, right in button_rects:
        draw_button(screen, "Pfeil-links", left, (mx, my), mousedown)
        draw_button(screen, "Pfeil-rechts", right, (mx, my), mousedown)

    pygame.display.flip()

pygame.quit()
