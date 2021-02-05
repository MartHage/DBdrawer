import pygame
from objects import *
from util import *

n = 40
m = 40
width = 900
height = 900

edge_width = 2
dot_radius = 3

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


click_pos_1 = (0, 0)
click_pos_2 = (0, 0)

click = False

color = (150, 150, 150)
highlight_color = (100, 100, 100)

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
            for e in edges:
                e.active = True
                e.color = (150, 150, 150)
                e.complete_edge((100, 100, 100))

        if pressed[pygame.K_p]:
            for e in edges:
                if e.active and (e.color == (255, 0, 0) or e.color == (0, 0, 255)):
                    e.active = False

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


print("To play mode")

crashed = False

player = True
click_pos_1 = False

while not crashed:

    click = False

    p_color = (255, 0, 0)
    p_color_highlight = (150, 0, 0)
    if not player:
        p_color = (0, 0, 255)
        p_color_highlight = (0, 0, 255)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True

    gameDisplay.fill((50, 50, 50))

    mouse = pygame.mouse.get_pos()

    # draw boxes
    for j in range(n - 1):
        for i in range(n - 1):
            box(boxes[i][j])

    # draw edges
    for e in edges:
        if e.rect[0] <= mouse[0] <= e.rect[0] + e.rect[2] and e.rect[1] <= mouse[1] <= e.rect[1] + e.rect[3] and not e.active:
            e.color = p_color_highlight
            if click:
                e.active = not e.active

                if not e.complete_edge(p_color):
                    player = not player

        else:
            e.reset_color()

        edge(e)

    # draw dots
    for i in range(n):
        for j in range(n):
            dot(i, j)



    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()