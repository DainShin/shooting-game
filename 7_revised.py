import pygame
import os

#######################################################################
# initialise
pygame.init()

# setting the screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# title
pygame.display.set_caption("Popping Game")

# FPS
clock = pygame.time.Clock()
#######################################################################

# 1.basic settings (backround, character, speed, direction etc)
# os.path.join(): join the routes
current_path = os.path.dirname(__file__)  # return the current file directory
image_path = os.path.join(current_path, "images")  # return the images folder directory

# background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = (screen_height - stage_height - character_height)

# direction
character_to_x = 0

# speed of the character
character_speed = 5

# weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# you can make many shoots at the same time
weapons = []

# speed of the weapon
weapon_speed = 10

# 공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# the speed of balls are differenct according to the size
ball_speed_y = [-18, -15, -12, -9]  # index 0,1,2,3에 해당하는 값

# list for the information of the ball
balls = []

# the information of the biggest ball at the very first
balls.append({
    "pos_x": 50,   # x position
    "pos_y": 50,   # y position
    "img_idx": 0,   # image index
    "to_x": 3,      # move to x direction
    "to_y": -6,     # move to y direction
    "init_spd_y": ball_speed_y[0]  # the initial speed of ball
})

# weapons and ball that are going to be removed
weapon_to_remove = -1
ball_to_remove = -1

# font 
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()  # 시작 시간 정의

# Messages : Time out Mission Complete, Game Over
game_result = "Game Over"

running = True
while running:
    dt = clock.tick(30)

   # 2. event management (keyboard)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # move the character to the left
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:  #  move the character to the right
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:  # using the wepon 
                weapon_x_pos = character_x_pos + \
                    (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. position of the character
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # position of the weapon
    # 100, 200 -> 180, 160, 140, ... 
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]  

    # if the position of the weapon is greater than the heigth of the screen, it will diappeear
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # position of the ball
    # enumerate brings the index number as well
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # if the position of balls is greater than the screen size, we will change the direction of the balls
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        
        # if the balll is within the screen, the ball speed will increase
        else:  
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. confliction

    # update character rect
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # update ball rect
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # check if the ball has confliction with the weapon
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # check the confliction
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # update the weapon rect
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # check the confliction: when the weapon and balls have a confilition, the indcies of the weapon and ball will be stored
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # if the the ball is not the smallest one, the ball size will be smllaer
                if ball_img_idx < 3:
                    # current ball
                    ball_width = ball_rect.size[0]
                    ball_heigth = ball_rect.size[1]

                    # splited ball
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # smaller ball to the left
                    balls.append({
                        # 공의 중간위치에서 작은공 넓이의 반만큼 왼쪽으로 이동
                        "pos_x": ball_pos_x + (ball_width/2) - (small_ball_width/2),
                        "pos_y": ball_pos_y + (ball_height/2) - (small_ball_height/2),
                        "img_idx": ball_img_idx + 1,
                        "to_x": -3,
                        "to_y": -6,
                        "init_spd_y": ball_speed_y[ball_img_idx+1]
                    })

                    # smaller ball to the right
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width/2) - (small_ball_width/2),
                        "pos_y": ball_pos_y + (ball_height/2) - (small_ball_height/2),
                        "img_idx": ball_img_idx + 1,
                        "to_x": 3,
                        "to_y": -6,
                        "init_spd_y": ball_speed_y[ball_img_idx+1]
                    })

                break  
        else: # continueing the game
            continue # if in the inner for statement the condition is not correspond, it will go to the outer for statement 
        break # if in the inner for statement it meets break, the code will be here ( to escape the both for statements)

        """
            for 바깥조건:
                바깥동작
                for 안쪽조건:
                    안쪽동작
                    if 충돌하면:
                        break
                else:
                    continue
                break           
        """


    # If the index of the stored ball or weapon is greater than -1, remove it from the 'balls' list -> Reset the 'ball_to_remove' index to -1.
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # if balls comopeletely disappear, the game will be over
    if len(balls) == 0:
        game_result = "Mission Complete"
        running =False

    # 5. add the images in the screen
    screen.blit(background, (0, 0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # set the time limit
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time: {}".format(
        int(total_time-elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # if time is over
    if total_time-elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()

# message when game is over
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# wait for 2 sec to show the message properly
pygame.time.delay(2000)

# pygame ends
pygame.quit()
