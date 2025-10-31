import pygame
import threading
import queue

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

result_queue = queue.Queue()
running = True

def make_surface(color, size):
    surf = pygame.Surface(size)
    surf.fill(color)
    return surf

def worker_thread():
    # Create surface off-main-thread
    surf = make_surface((255, 0, 0), (100, 100))
    result_queue.put(surf)

threading.Thread(target=worker_thread, daemon=True).start()

surface_to_draw = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if the thread produced a result
    try:
        surface_to_draw = result_queue.get_nowait()
    except queue.Empty:
        pass

    screen.fill((30, 30, 30))

    if surface_to_draw:
        screen.blit(surface_to_draw, (150, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
