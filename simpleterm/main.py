#!/usr/bin/env python
# This is literally the pygame hello world example.

import os
import pty
import select

import pygame
import pyte

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
done = False
font = pygame.font.SysFont("Source Code Pro", 12)

term = pyte.Screen(80, 24)
stream = pyte.ByteStream(term)

p_pid, master_fd = pty.fork()
if p_pid == 0:  # Child process
    os.execvpe("./thingie.py", ["./thingie.py"], env=dict(TERM="linux", COLUMNS="80", LINES="24", LC_ALL="en_US.UTF-8"))

p_out = os.fdopen(master_fd, "w+b", 0)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            p_out.write(chr(event.key).encode('utf-8'))

    screen.fill((0, 127, 127))

    ready, _, _ = select.select([p_out], [], [], 0)
    if ready:
        data = p_out.read(1024)
        if data:
            stream.feed(data)

    for i, row in enumerate(term.display):
        text = font.render(row, True, (0, 0, 0))
        screen.blit(text, (0, 20 * i))

    pygame.display.flip()
    clock.tick(30)
