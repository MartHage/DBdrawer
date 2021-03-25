import itertools

import pygame
from objects import *
from util import *
import pyperclip

n = 50
m = 50
width = 900
height = 900

edge_width = 1
dot_radius = 2

pygame.init()

gameDisplay = pygame.display.set_mode((width, height + 30))
pygame.display.set_caption("DotsAndBoxes")

pygame.font.init()
myfont = pygame.font.SysFont('Calibri', 20, bold=True)

clock = pygame.time.Clock()

crashed = False

boxes = [[Box(((i + 1) * width / (n + 1), (j + 1) * height / (n + 1), width / (n + 1), height / (n + 1))) for j in range(n - 1)] for i in range(n - 1)]

# for j in range(n - 1):
#     boxes.append([])
#     for i in range(n - 1):
#         boxes[j].append(Box(((i + 1) * width / (n + 1), (j + 1) * height / (n + 1))))

edges = []

# init edges
for j in range(n):
    for i in range(n-1):
        new_edge = Edge(((i + 1) * width / (n + 1), (j + 1) * height / (n + 1) - edge_width, width / (n + 1), 2*edge_width))
        edges.append(new_edge)

        if j < n-1:
            boxes[i][j].upper = new_edge
            new_edge.right_box = boxes[i][j]
        if j > 0:
            boxes[i][j - 1].bottom = new_edge
            new_edge.left_box = boxes[i][j - 1]

for j in range(n - 1):
    for i in range(n):
        new_edge = Edge(((i + 1) * width / (n + 1) - edge_width, (j + 1) * height / (n + 1), 2*edge_width, width / (n + 1)))
        edges.append(new_edge)

        if i < n - 1:
            boxes[i][j].left = new_edge
            new_edge.right_box = boxes[i][j]
        if i > 0:
            boxes[i - 1][j].right = new_edge
            new_edge.left_box = boxes[i - 1][j]


def dot(i, j):
    pygame.draw.circle(gameDisplay, (0, 0, 0), ((i + 1) * width / (n + 1), (j + 1) * height / (n + 1)), dot_radius)


def edge(e):
    pygame.draw.rect(gameDisplay, e.color, e.rect)


def box(b):
    pygame.draw.rect(gameDisplay, b.get_color(), b.rect)


def line(start, end):
    pygame.draw.line(gameDisplay, (0, 0, 0), start, end, width=10)


def export_latex():
    print("        ")

    size = 8

    min_x = 10000000
    min_y = 10000000

    body = ''

    active_boxes = []
    points = set()
    lines = set()

    for j in range(n - 1):
        for i in range(n - 1):
            if boxes[i][j].get_color() != (100, 100, 100):
                # draw points
                color_box = 'white'
                if boxes[i][j].get_color() == (0, 0, 150):
                    color_box = 'blue'
                elif boxes[i][j].get_color() == (150, 0, 0):
                    color_box = 'red'

                corners = []
                for off in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                    x = (i + off[0]) * size
                    y = (1000 - j - off[1]) * size
                    points.add((x, y))
                    corners.append((x, y))
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)

                if color_box != 'white':
                    active_boxes.append((corners, color_box))

                if boxes[i][j].left.get_color() != (40, 40, 40):
                    line_color = 'black'
                    if boxes[i][j].left.color == (255, 0, 0):
                        line_color = 'red'
                    if boxes[i][j].left.color == (0, 0, 255):
                        line_color = 'blue'

                    lines.add((((i * size, (1000 - j) * size), (i * size, (1000 - j - 1) * size)), line_color))

                if boxes[i][j].right.get_color() != (40, 40, 40):
                    line_color = 'black'
                    if boxes[i][j].right.color == (255, 0, 0):
                        line_color = 'red'
                    if boxes[i][j].right.color == (0, 0, 255):
                        line_color = 'blue'

                    lines.add(((((i + 1) * size, (1000 - j) * size), ((i + 1) * size, (1000 - j - 1) * size)), line_color))

                if boxes[i][j].upper.get_color() != (40, 40, 40):
                    line_color = 'black'
                    if boxes[i][j].upper.color == (255, 0, 0):
                        line_color = 'red'
                    if boxes[i][j].upper.color == (0, 0, 255):
                        line_color = 'blue'

                    lines.add(((((i) * size, (1000 - j) * size), ((i + 1) * size, (1000 - j) * size)), line_color))

                if boxes[i][j].bottom.get_color() != (40, 40, 40):
                    line_color = 'black'
                    if boxes[i][j].bottom.color == (255, 0, 0):
                        line_color = 'red'
                    if boxes[i][j].bottom.color == (0, 0, 255):
                        line_color = 'blue'

                    lines.add(((((i) * size, (1000 - j - 1) * size), ((i + 1) * size, (1000 - j - 1) * size)), line_color))

    body = f'<ipeselection pos="{min_x} {min_y}">'

    for corners, color_box in active_boxes:
        body += f'<path layer="alpha" fill="{color_box}" opacity="30%" stroke-opacity="opaque">\n'
        body += f'{corners[0][0]} {corners[0][1]} m\n'
        body += f'{corners[1][0]} {corners[1][1]} l\n'
        body += f'{corners[3][0]} {corners[3][1]} l\n'
        body += f'{corners[2][0]} {corners[2][1]} l\n'
        body += f'h\n'
        body += f'</path>\n'

    for line, line_color in lines:
        body += f'<path layer="alpha" stroke="{line_color}">\n'
        body += f'{line[0][0]} {line[0][1]} m\n'
        body += f'{line[1][0]} {line[1][1]} l\n'
        body += f'</path>\n'

    for point in points:
        body += f'<use layer="alpha" name="mark/disk(sx)" pos="{point[0]} {point[1]}" size="tiny" stroke="black"/>\n'

    body += f'</ipeselection>'

    pyperclip.copy(body)

    print(" Succesfully copied to clippboard ")


click_pos_1 = (0, 0)
click_pos_2 = (0, 0)

click = False

color = (150, 150, 150)
highlight_color = (100, 100, 100)

save_edges = [False] * len(edges)

while not crashed:
    click_pos_2 = click_pos_1
    click_pos_1 = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True

        if event.type == pygame.MOUSEBUTTONUP:
            click = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q]:
            color = (150, 150, 150)
            highlight_color = (100, 100, 100)
        if pressed[pygame.K_w]:
            color = (255, 0, 0)
            highlight_color = (150, 0, 0)
        if pressed[pygame.K_e]:
            color = (0, 0, 255)
            highlight_color = (0, 0, 150)

        if pressed[pygame.K_o]:
            first = False
            for i in range(len(edges)):
                if not edges[i].active:
                    first = True
                    break

            if first:
                for i in range(len(edges)):
                    save_edges[i] = edges[i].active

            for e in edges:
                e.active = True
                e.color = (150, 150, 150)
                e.complete_edge((100, 100, 100))

        if pressed[pygame.K_p]:
            for i in range(len(edges)):
                save_edges[i] = edges[i].active

            for e in edges:
                if e.active and (e.color == (255, 0, 0) or e.color == (0, 0, 255)):
                    e.active = False

        if pressed[pygame.K_z]:
            for i in range(len(edges)):
                edges[i].color = (150, 150, 150)
                edges[i].active = save_edges[i]


        if pressed[pygame.K_c]:
            export_latex()


    gameDisplay.fill((50, 50, 50))

    mouse = pygame.mouse.get_pos()

    trudi = 0
    falsic = 0

    # draw boxes
    for j in range(n - 1):
        for i in range(n - 1):
            if boxes[i][j].get_color() == (150, 0, 0):
                trudi += 1
            if boxes[i][j].get_color() == (0, 0, 150):
                falsic += 1
            box(boxes[i][j])

    # draw edges
    for e in edges:
        edge(e)

    # draw dots
    for i in range(n):
        for j in range(n):
            dot(i, j)

    text_surface = myfont.render(f'Trudi: {trudi}', False, (255, 200, 200))
    gameDisplay.blit(text_surface, (50, height - 10))

    text_surface = myfont.render(f'Falsic: {falsic}', False, (200, 200, 200))
    gameDisplay.blit(text_surface, (200, height - 10))

    pygame.display.update()
    clock.tick(30)

    if click:
        for e in edges:
            if intersect(click_pos_1, click_pos_2, (e.rect[0], e.rect[1]), (e.rect[0] + e.rect[2], e.rect[1] + e.rect[3])):
                e.active = not e.active
                e.color = color
                if e.active:
                    e.complete_edge(highlight_color)

            else:
                e.reset_color(color)

    else:
        for e in edges:
            e.reset_color(color)


pygame.quit()
quit()