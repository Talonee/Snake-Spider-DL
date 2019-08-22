from PIL import Image
from resizeimage import resizeimage
import pygame, random, time, numpy as np

####### Display
def display_snake(snake_position):
    for position in snake_position:
        # draw rectangle corresponding to given args
        pygame.draw.rect(display, white, pygame.Rect(position[0], position[1], 10, 10)) 

def display_apple(display, apple_position, apple):
    # show apple image
    display.blit(apple, (apple_position[0], apple_position[1]))

def display_final_score(display_text, final_score):
    text = pygame.font.Font('freesansbold.ttf', 35)
    TextSurf = text.render(display_text, True, white)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((width / 2), (height / 2))
    display.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)

####### Collide
def collide_apple(apple_position, score):
    apple_position = [random.randrange(1, 50)*10, random.randrange(1, 50)*10]
    score += 1
    return apple_position, score

def collide_wall(snake_head):
    if snake_head[0] >= width or snake_head[0] >= height or snake_head[0] < 0 or snake_head[1] >= width or snake_head[1] >= height or snake_head[1] < 0:
        return 1
    else:
        return 0

def collide_self(snake_position):
    snake_head = snake_position[0]
    if snake_head in snake_position[1:]:
        return 1
    else:
        return 0


####### Direction blocked (?)
def blocked(snake_position, vector):
    next = snake_position[0] + vector
    snake_head = snake_position[0]

    # Check if game is still going (1 = yes, 2 = no)
    if collide_wall(snake_head) == 1 or collide_self(snake_position) == 1:
        return 1
    else:
        return 0


####### Generate
def generate_snake(snake_head, snake_position, apple_position, btn_dir, score):
    if btn_dir == 1:
        snake_head[0] += 10
    elif btn_dir == 0:
        snake_head[0] -= 10
    elif btn_dir == 2:
        snake_head[1] += 10
    elif btn_dir == 3:
        snake_head[1] -= 10
    else:
        pass

    if snake_head == apple_position:
        # reset apple pos and catch the score
        apple_position, score = collide_apple(apple_position, score) 
        # elongate the snek because of food
        snake_position.insert(0, list(snake_head))
    else:
        # move the snek
        snake_position.insert(0, list(snake_head))
        snake_position.pop()
    
    return snake_position, apple_position, score


####### Play
def play(snake_head, snake_position, apple_position, btn_dir, apple, score):
    crashed = False
    prev_dir = 1
    btn_dir = 1
    vector = np.array(snake_position[0]) - np.array(snake_position[1])

    while crashed is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_LEFT and prev_dir != 1:
                    btn_dir = 0
                elif event.key == pygame.K_RIGHT and prev_dir != 0:
                    btn_dir = 1
                elif event.key == pygame.K_UP and prev_dir != 2: 
                    btn_dir = 3
                elif event.key == pygame.K_DOWN and prev_dir != 3:
                    btn_dir = 2
                else:
                    btn_dir = btn_dir

        prev_dir = btn_dir 

        display.fill(window_color)    
        display_apple(display, apple_position, apple)
        display_snake(snake_position)      

        snake_position, apple_position, score = generate_snake(snake_head, snake_position, apple_position, btn_dir, score)
        pygame.display.set_caption("Snake Game" + " SCORE: " + str(score)) 
        pygame.display.update()
        
        if blocked(snake_position, vector) == 1:
            crashed = True

        # clock.tick(20)

    return score


if __name__ == "__main__":
    with open('apple.png', 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [10, 10], validate = False)
            cover.save('apple-resize.png', image.format)


    width = 500
    height = 500
    black = (0, 0, 0)
    white = (255, 255, 255)
    window_color = black
    apple = pygame.image.load('apple-resize.png')
    clock = pygame.time.Clock()

    snake_head = [250, 250]
    snake_position = [[250, 250], [240, 250], [230, 250]]
    apple_position = [random.randrange(1, 50)*10, random.randrange(1, 50)*10] # generate random coor
    score = 0

    pygame.init()

    display = pygame.display.set_mode((width, height))
    display.fill(window_color)
    pygame.display.update()

    final_score = play_game(snake_head, snake_position, apple_position, 1, apple, score)
    display = pygame.display.set_mode((display_width,display_height))
    display.fill(window_color)
    pygame.display.update()

    
    display_text = 'Your Score is: ' + str(final_score)
    display_final_score(display_text, final_score)

    pygame.quit()