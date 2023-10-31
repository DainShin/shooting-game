import pygame
import os
#######################################################################
# 기본 초기화 (반드시 해야하는 것들)
pygame.init()

# setting the screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# title
pygame.display.set_caption("Pang")

# FPS
clock = pygame.time.Clock()
#######################################################################

# 1. 사용자 게임 초기화 (배경화면, 게임 이밎, 좌표, 속도, 폰트 등)
# os.path.join(): 여러 경로 구성 요소를 결합하여 하나의 경로로 만들어주는 함수. 슬래시 또는 역슬래시를 올바르게 처리하여 경로를 만들어줌
current_path = os.path.dirname(__file__) # 현재파일의 위치를 반환
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = (screen_height - stage_height - character_height)

# 캐릭터 이동방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]


# 무기는 한 번에 여러발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10


running = True 
while running:
    dt = clock.tick(30)

   # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT : # 캐릭터를 왼쪽으로
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:  # 캐릭터를 오른쪽으로
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:  # 무기발사
                weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0


    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    # 100, 200 -> 180, 160, 140, ... : x 좌표는 그대로 두고 y를 speed 만큼 빼준후 
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons ] # 무기 위치를 위로 

    # 천장에 닿은 무기 없애기 : y좌표가 0보다 큰 것
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0 ]   

    # 4. 충돌 처리
    
    # 5. 화면에 그리기 
    screen.blit(background, (0,0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage, (0,screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    
   
    pygame.display.update()

# pygame ends
pygame.quit()