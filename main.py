import pygame
pygame.font.init()

# Window properties
WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pyong")
FPS = 60
FONT = pygame.font.SysFont("comicsans", 50)

# Screen colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle properties
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

# Ball properties
BALL_RADIUS = 10

# Game properties
WIN_SCORE = 3


class Paddle:
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VELOCITY = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0
        self.x_velocity *= -1


def draw_centerline(window):
    segment_height = HEIGHT // 20
    segment_width = 10

    for i in range(10, HEIGHT, segment_height * 2):
        pygame.draw.rect(window, WHITE, (WIDTH // 2 - segment_width // 2, i, segment_width, segment_height))


def draw(window, paddles, ball, left_score, right_score):
    window.fill(BLACK)
    left_score_text = FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = FONT.render(f"{right_score}", 1, WHITE)
    window.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    window.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))
    draw_centerline(window)

    for paddle in paddles:
        paddle.draw(window)

    ball.draw(window)
    pygame.display.update()


def handle_paddle_collision(ball, paddle):
    # The ball has hit the paddle, now change its direction and y_velocity
    ball.x_velocity *= -1

    # Calculate the new y_velocity based on where the ball hits the paddle
    middle_y = paddle.y + paddle.height / 2
    difference_in_y = middle_y - ball.y
    reduction_factor = (paddle.height / 2) / ball.MAX_VELOCITY
    y_vel = difference_in_y / reduction_factor
    ball.y_velocity = -1 * y_vel


def handle_collision(ball, left_paddle, right_paddle):
    # Check for collision with top or bottom walls
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_velocity *= -1

    # Handle collision with left paddle
    if ball.x_velocity < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                handle_paddle_collision(ball, left_paddle)

    # Handle collision with right paddle
    else:  # ball.x_velocity > 0
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                handle_paddle_collision(ball, right_paddle)


def handle_keys(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def end_game(ball, left_paddle, right_paddle, left_score, right_score):
    winner = "Right" if left_score < right_score else "Left"
    win_text = FONT.render("Game Over " + winner + " Wins!", 1, WHITE)
    WINDOW.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
    ball.reset()
    left_paddle.reset()
    right_paddle.reset()


def main():
    clock = pygame.time.Clock()
    left_score = right_score = 0
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    run = True
    while run:
        clock.tick(FPS)  # Regulate the speed of the game
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_keys(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x <= 0:
            right_score += 1
            ball.reset()
        elif ball.x >= WIDTH:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WIN_SCORE or right_score >= WIN_SCORE:
            won = True
        if won:
            draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)
            end_game(ball, left_paddle, right_paddle, left_score, right_score)
            left_score = right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()
