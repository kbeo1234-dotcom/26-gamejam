from Draw import  DrawEntity
import pymunk
import pygame


class Ball(DrawEntity):
    def __init__(self, space, x, y, radius=7):
        super().__init__(space, color=(255, 50, 50))
        self.radius = radius

        self.body = pymunk.Body(mass=1, moment=100)
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, radius)

        self.add_to_space(elasticity=0.6, friction=0.1)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)