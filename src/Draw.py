class DrawEntity:
    def __init__(self, space, color):
        self.space = space
        self.color = color
        self.body = None
        self.shape = None

    @property
    def x(self):
        return int(self.body.position.x)

    @property
    def y(self):
        return int(self.body.position.y)

    def add_to_space(self, elasticity, friction):
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.space.add(self.body, self.shape)

    def draw(self, screen):
        raise NotImplementedError("하위 클래스에서 draw() 메서드를 구현해야 합니다.")