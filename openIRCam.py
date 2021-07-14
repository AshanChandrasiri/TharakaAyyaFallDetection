import pygame.camera

pygame.init()
pygame.camera.init()
cam_list = pygame.camera.list_cameras()
cam = None
if cam_list:
    cam = pygame.camera.Camera(cam_list[0], (640, 480))
    cam.start()

window_surface = pygame.display.set_mode((640, 480))

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    if cam is not None:
        image = cam.get_image()
        window_surface.blit(image, (0, 0))

    pygame.display.update()