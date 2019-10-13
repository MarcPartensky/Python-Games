import pygame



pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0],(1280,720))
cam.start()
time.sleep(1)
webcamImage = cam.get_image()
