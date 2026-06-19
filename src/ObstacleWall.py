from Draw import  DrawEntity
import pymunk
import pygame



class ObstacleWall(DrawEntity):
    def __init__(self, space, x, y, width, height):
        super().__init__(space, color=(70, 130, 180))
        self.width = width
        self.height = height

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body, (width, height))

        self.add_to_space(elasticity=0.3, friction=0.5)

    def draw(self, screen):
        rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)