#IMPORTED MODULES
import pygame
import random


#Initialize
pygame.init()



#VARIABLES-------------------------------------------------
WIDTH, HEIGHT = 400, 700
BLACK = (0,0,0)
sound_button = pygame.Rect(340, 20, 50, 50)
POSITION_COUNT = 12
ROCK_COUNT = 2
PLAYER_INIT_X, PLAYER_INIT_Y = 170, 400
BLOCK_WIDTH, BLOCK_HEIGHT = 80, 40
BLOCKS_PER_FLOOR = 3
ROCK_WIDTH, ROCK_HEIGHT = 50, 50
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
ROCK_Y_MIN, ROCK_Y_MAX = -330, -50
FLOORS = 7
JUMP_DURATION = 100
ACCELERATION = -1/7
VOLUME = 0.5
high_score = 0
screen = pygame.display.set_mode((WIDTH,HEIGHT))


#Set font
def font_size(size):
    return pygame.font.Font("myfont.ttf", size) # DESIGN CREDIT: wepfont

font = font_size(30)
font_small = font_size(15)


# Title and icon - CREDIT to Freecodecamp
pygame.display.set_caption("Jumping Dog")
icon = pygame.image.load("dog_tail_down.tiff")
pygame.display.set_icon(icon)


# Background Music CREDIT: ArturAravidiMusic from Pixabay
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1) # -1 means infinite loop 
pygame.mixer.music.set_volume(VOLUME)



#SPRITES---------------------------------------------------

#Blocks sprite

class Block(pygame.sprite.Sprite): # CREDIT to Clear Code (YouTube Channel) for basic structure of sprite.
     def __init__(self,x,y):
        super().__init__()
        img = load_image("grass.png") # IMAGE CREDIT: Kenney.nl
        self.image = pygame.transform.scale(img,(BLOCK_WIDTH, BLOCK_HEIGHT))
        #Draw a rectangle around the image.
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]

     def move(self, dx,dy):
        self.rect.x += dx
        self.rect.y -= dy


#Player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        img = load_image("dog_tail_down.tiff") # IMAGE CREDIT: http://mtsids.com/
        self.image = pygame.transform.scale(img,(PLAYER_WIDTH, PLAYER_HEIGHT))
         # Draw a rectangle around the image.
        self.rect = self.image.get_rect()

        self.rect.bottomleft = [x,y]

    def move(self,x,y):
        self.rect.x += x
        self.rect.y -= y

    def imgchange(self, image_path):
        img = pygame.image.load(image_path).convert_alpha() # convert_alpha preserves transparency, improves performance  
        self.image = pygame.transform.scale(img,(PLAYER_WIDTH, PLAYER_HEIGHT))



class Rock(pygame.sprite.Sprite):
        def __init__(self,x,y):
            super().__init__()
            img = load_image("Rock Pile.png")  # IMAGE CREDIT: FunwithPixels on Opengamearts.org

            self.image = pygame.transform.scale(img,(ROCK_WIDTH, ROCK_WIDTH))
            #Draw a rectangle around the image.
            self.rect = self.image.get_rect()
            self.rect.bottomleft = [x,y]
            self.original_x = x
            self.original_y = y
            self.rock_fall_y = 0

        def move(self,x,y):
            self.rect.x += x
            self.rect.y -= y

        def reset(self, x, y):
            self.rect.x = x
            self.rect.y = y
            self.rock_fall_y = 0



#OTHER FUNCTIONS ------------------------------------------------------------------------

#show gameover text
def gameover_text():
    # CREDIT to freecodecamp  (same for show_score())
    text = font.render("Game Over", True, BLACK)
    screen.blit(text,(120,350))


#Format score
def format_score(label, score):
    return label + ": " + str(score)

#show score
def show_score(score, color=BLACK, x=10,y=20):
    score_text = font.render(format_score("Score", score), True, color)
    high_score_text = font.render(format_score("High Score", high_score), True, color)
    screen.blit(score_text,(x,y))
    screen.blit(high_score_text,(x,y+60))


def set_high_score(high_score, score):
    return max(high_score, score)


#show button
def show_sound_control():
    # Image credit: smashingstocks
    button_image = pygame.image.load("play_button.png") # ICON CREDIT: smashingstocks on Flaticon
    button_image = pygame.transform.scale(button_image,(50,50))
    text = font_small.render("sound", True, BLACK)
    screen.blit(text,(340,10))
    screen.blit(button_image,(340,20))

#Produce possible x_positions of blocks
def produce_positions(positions):
    list = []
    for i in range(positions):
        list.append(round(i*330/(positions-1),1))
    return list 

def load_image(filename):
    return pygame.image.load(filename).convert_alpha()


# Difficulty between 1 to 5, 1 being the easiest and 5 being the hardest. 
# If reset height is high, it means that more time passes between the consecutive "waves" of rocks, making it easier for players to avoid the rock. 
def reset_height(difficulty=1): 
    return 700+250*(5-difficulty)
        

#Main function ---------------------------------------------------------------------------
def main():

    #VARIABLES -----------------------------------------------------------
    running = True
    playing = True
    jumping = False
    gameover = False
    effect_on = True
    jump_t = 0
    fall_y = 0
    background = pygame.image.load("background.png").convert() #IMAGE CREDIT: Zenyu Ren
    score = 0
    global high_score
    pygame.mixer.music.unpause()

    #SPRITES -----------------------------------------------------------
    #Create instance of player
    player = Player(PLAYER_INIT_X, PLAYER_INIT_Y)
    player_group = pygame.sprite.Group()
    player_group.add(player)


    #Create instance of block, grouping them
    block_group = pygame.sprite.Group()
    for i in range(FLOORS):
        #Randomly choosing the x-position
        choices = random.sample(produce_positions(POSITION_COUNT), BLOCKS_PER_FLOOR)
        for j in range(BLOCKS_PER_FLOOR):
            new_block = Block(choices[j],100*i)
            block_group.add(new_block)


    #Create instance of rock, grouping them
    rock_group = pygame.sprite.Group()
    for i in range(ROCK_COUNT):
        #Randomly choosing the x-position
        new_rocks = Rock(random.randint(0, WIDTH - ROCK_WIDTH), random.randint(ROCK_Y_MIN,ROCK_Y_MAX))
        rock_group.add(new_rocks)


    clock = pygame.time.Clock()


    #GAME LOOP -----------------------------------------------------------
    while running:

        clock.tick(200)

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button.collidepoint(mouse):
                    if playing:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

                    effect_on = not effect_on
                    playing = not playing 
                    
                    
        #Move the player in x direction
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.move(-1,0)

        if keys[pygame.K_RIGHT]:
            player.move(1,0)

        if player.rect.x > WIDTH:
                player.rect.x = 0

        if player.rect.x < -PLAYER_WIDTH:
                player.rect.x = WIDTH - PLAYER_WIDTH


        # Create block rectangles for collision detection
        blocks = [block.rect for block in block_group.sprites()]

        # Create rock rectangles for collision detection
        rocks = [rock.rect for rock in rock_group.sprites()]
        
        # collsion with the rock
        if player.rect.inflate(-18,0).collideobjects(rocks): # shrink the width by 18 pixels 
            gameover = True


        # Only allow the player to jump if it's not already jumping.
        if not jumping:
            player.imgchange("dog_tail_down.tiff") # IMAGE CREDIT: http://mtsids.com/
            if keys[pygame.K_SPACE]:
                jumping = True

                if effect_on:
                    sound_effect = pygame.mixer.Sound("sound_effect.mp3") # AUDIO CREDIT: Pixabay
                    channel = pygame.mixer.find_channel()
                    if channel:
                        channel.play(sound_effect)
                    sound_effect.set_volume(VOLUME)
        else:
            player.imgchange("dog_tail_up.tiff") # IMAGE CREDIT: http://mtsids.com/
            if 0 <= jump_t <= JUMP_DURATION:
                 #If it's jumping, move all the blocks according to a function
                for block in block_group:
                    block.move(0,-(ACCELERATION * jump_t +(JUMP_DURATION // 2) * (-ACCELERATION)))
                jump_t += 1
            else:
                jump_t = 0
                jumping = False

        # y-direction
        if jumping:
            jump_t += 1

            next = player.rect.collideobjects(blocks) # Returns object of the first collision 
            
            # If increasing jump_t by 1 makes the player collide with a block 
            if next:
                # the player is falling and it is at the top of a block 
                if JUMP_DURATION > jump_t > JUMP_DURATION // 2 and 0 <= player.rect.bottom - next.top <= 6: 
                    # land on the block
                    fall_y = 0
                    jumping = False
                    jump_t = 0
           
            jump_t -= 1


        # Simulate falling 
        if not jumping:
            if not player.rect.inflate(-18,0).collideobjects(blocks):
                for block in block_group:
                    block.move(0,1/40*fall_y)
                fall_y += 1

                # If player falls a certain distance, the player itself moves down and eventually goes out of the screen
                if fall_y > 500:
                    player.move(0,-1/40*(fall_y-500))



        # If a block disappears, delete it and create another one at the top, with random x position.
            for block in block_group:
                if block.rect.y > HEIGHT and not jumping:
                    block_group.remove(block)
                    new_target1 = Block(random.choice(produce_positions(POSITION_COUNT)),100)
                    block_group.add(new_target1)
                    score += 1



        # if the dog goes out of screen, game over  
        if player.rect.y > HEIGHT:
            gameover = True # CREDIT to "Rabbit76" on stackoverflow.


        # Rocks start to fall if a score is over a certain number 
        if score > 10:
            for rock in rock_group:
                rock.move(0, -1/80*(rock.rock_fall_y**2 - (rock.rock_fall_y-1)**2))
                rock.rock_fall_y += 1
                if rock.rect.y > reset_height():
                    rock.reset(random.randint(0, WIDTH - ROCK_WIDTH), -random.randint(100,400))
    

        # clear the display
        screen.blit(background,(0,0))

        # Update elements
        player_group.update()
        block_group.update()
        block_group.draw(screen)
        player_group.draw(screen)
        rock_group.draw(screen)
        rock_group.update(screen)


        show_score(score)
        show_sound_control()

        #If dog falls out of screen, display gameover message.
        if gameover:
            high_score = set_high_score(high_score, score)
            gameover_text()
            pygame.mixer.music.pause()


        #Update
        pygame.display.flip()

#---------------------------------------------------------------------(main)

if __name__ == "__main__":
    main()
