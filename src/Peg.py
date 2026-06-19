from Draw import  DrawEntity
import pymunk
import pygame

class Peg(DrawEntity):
    def __init__(self, space, x, y, radius=5):
        super().__init__(space, color=(200, 200, 200))
        self.radius = radius

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, radius)

        self.add_to_space(elasticity=0.7, friction=0.2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)