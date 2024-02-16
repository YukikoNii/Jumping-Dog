#IMPORTED MODULES
import pygame
import random


#Initialize
pygame.init()


#screen with width of 400 and height of 700
screen = pygame.display.set_mode((400,700))
#Set font
def font_size(int):
    return pygame.font.Font("myfont.ttf", int) #DESIGN CREDIT:wepfont

font = font_size(30)


#Title and icon - CREDIT to Freecodecamp
pygame.display.set_caption("Jumping Dog")
icon = pygame.image.load("dog.tiff")
pygame.display.set_icon(icon)


#Background Music CREDIT: ArturAravidiMusic from Pixabay
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)


#VARIABLES-------------------------------------------------
WIDTH, HEIGHT = screen.get_size()
score = 0
num_of_poss = 12
BLACK = (0,0,0)


#SPRITES---------------------------------------------------

#Blocks sprite

class Block(pygame.sprite.Sprite): #CREDIT to Clear Code (YouTube Channel) for basic structure of sprite.
     def __init__(self,x,y):
        super().__init__()
        self.image = load_image("grass.png") #IMAGE CREDIT: Kenney.nl


        self.image = pygame.transform.scale(self.image,(80,40))
        #Draws a rectangle around the image.
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]

     def move(self,x,y):
        self.rect.x += x
        self.rect.y -= y


#Player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = load_image("dog.tiff") #IMAGE CREDIT: http://mtsids.com/

        self.image = pygame.transform.scale(self.image,(50,50))
         #Draws a rectangle around the image.
        self.rect = self.image.get_rect()

        self.rect.bottomleft = [x,y]

    def move(self,x,y):
        self.rect.x += x
        self.rect.y -= y

    def imgchange(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(50,50))



class Rock(pygame.sprite.Sprite):
        def __init__(self,x,y):
            super().__init__()
            self.image = load_image("Rock Pile.png")#IMAGE CREDIT: FunwithPixels on Opengamearts.org

            self.image = pygame.transform.scale(self.image,(50,50))
            #Draws a rectangle around the image.
            self.rect = self.image.get_rect()

            self.rect.bottomleft = [x,y]


            self.original_x = x
            self.original_y = y

            self.rock_fall_y = 0

        def move(self,x,y):
            self.rect.x += x
            self.rect.y -= y



#OTHER FUNCTIONS ------------------------------------------------------------------------

#show gameover text
def gameover_text():
    #CREDIT to freecodecamp  (same for show_score())
    text = font.render("Game Over", True, BLACK)
    screen.blit(text,(120,350))


#Format score
def format_score(score):
    return "Score: "+ str(score)

#show score
def show_score(color=BLACK, x=10,y=20):
    score_num = font.render(format_score(score), True, color)
    screen.blit(score_num,(x,y))


#show button
def show_button():
    #Image credit: smashingstocks
    button_image = pygame.image.load("play_button.png") #ICON CREDIT: smashingstocks on Flaticon
    button_image = pygame.transform.scale(button_image,(50,50))
    smaller_font = font_size(15)
    button_text = smaller_font.render("sound", True, BLACK)
    screen.blit(button_image,(340,20))
    screen.blit(button_text,(340,10))

#Produce possible x_positions of blocks
def produce_positions(num_of_poss):
    list = []
    for i in range(num_of_poss):
        list.append(round(i*330/(num_of_poss-1),1))
    return list 

def load_image(filename):
    return pygame.image.load(filename).convert_alpha()


#Difficulty between 1 to 5, 1 being the easiest and 5 being the hardest. 
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
    jump_y = 0
    fall_y = 0
    background = pygame.image.load("background.png").convert() #IMAGE CREDIT: Zenyu Ren
    global score

    #SPRITES -----------------------------------------------------------
    #Create instance of player
    player = Player(170,400)
    player_group = pygame.sprite.Group()
    player_group.add(player)



    #Create instance of block, grouping them
    block_group = pygame.sprite.Group()
    for i in range(7):
        #Randomly choosing the x-position
        choices = random.sample(produce_positions(num_of_poss),2)
        new_block1 = Block(choices[0],100*i)
        new_block2= Block(choices[1],100*i)
        block_group.add(new_block1)
        block_group.add(new_block2)


    #Create instance of rock, grouping them
    rock_group = pygame.sprite.Group()
    for i in range(3):
        #Randomly choosing the x-position
        x_choice = random.randint(0,330)
        y_choice= random.randint(-300,-50)
        new_rocks = Rock(x_choice,y_choice)
        rock_group.add(new_rocks)


    clock = pygame.time.Clock()



    #GAME LOOP -----------------------------------------------------------
    while running:

        clock.tick(200)


        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 340 < mouse[0] < 390 and 20 < mouse[1] < 70:
                    if playing == True:
                        effect_on = False
                        pygame.mixer.music.pause()
                        playing = False
                    else:
                        pygame.mixer.music.unpause()
                        playing = True
                        effect_on = True



        #Move the player in x direction
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.move(-1,0)

        if keys[pygame.K_RIGHT]:
            player.move(1,0)

        if player.rect.x > 400:
                player.rect.x = 0

        if player.rect.x < -50:
                player.rect.x = 350





        #Create block rectangles for collision detection
        rect_list = [block.rect for block in block_group.sprites()]

        #Create rock rectangles for collision detection
        rock_rect_list = [rock.rect for rock in rock_group.sprites()]
        #collsion with the rock

        if player.rect.inflate(-18,0).collideobjects(rock_rect_list):
            gameover = True


        #Only allow the player to jump if it's not already jumping.
        if not jumping:
            player.imgchange("dog.tiff") #IMAGE CREDIT: http://mtsids.com/
            if keys[pygame.K_SPACE]:
                jumping = True
                #Sound Effect from Pixabay
                if effect_on == True:
                    sound_effect = pygame.mixer.Sound("sound_effect.mp3") #AUDIO CREDIT: Pixabay
                    pygame.mixer.find_channel().play(sound_effect)
                    sound_effect.set_volume(0.5)


        else:
            player.imgchange("dog2.tiff") #IMAGE CREDIT: http://mtsids.com/
            if 0 <= jump_y <= 100:
                #If it's jumping, move all the blocks according to a function
                for block in block_group:
                    block.move(0,-(-1/7*jump_y+50/7))
                jump_y += 1
            else:
                jump_y = 0
                jumping = False

        #y-direction
        if jumping:
            jump_y += 1
            next = player.rect.collideobjects(rect_list)
            if next is not None:
                if 100 > jump_y > 49 and 0 <= player.rect.bottom - next.top <= 6:
                        fall_y = 0
                        jumping = False
                        jump_y = 0

            jump_y -= 1


        #collsion detection and coordinate calculation
        if not jumping:
            #Code: Credits to a user "import random"(on stackoverslow) on the use
            if not player.rect.inflate(-18,0).collideobjects(rect_list):
                for block in block_group:
                    block.move(0,1/40*fall_y)
                fall_y += 1
                if fall_y > 500:
                    player.move(0,-1/40*(fall_y-500))



        #If a block disappears, delete it and create another one, with random x position.
            for block in block_group:
                if block.rect.y > HEIGHT:
                    if not jumping:
                        block_group.remove(block)
                        new_target1 = Block(random.choice(produce_positions(num_of_poss)),100)
                        block_group.add(new_target1)
                        score += 1



        #if the dog goes out of screen, "Game Over" = True
        if player.rect.y > HEIGHT:
            gameover = True #CREDIT to "Rabbit76" on stackoverflow.

        #If the score exceeds 50
        if score > 10:
            for rock in rock_group:
                rock.move(0, -1/80*rock.rock_fall_y)
                rock.rock_fall_y += 1
                if rock.rect.y > reset_height():
                    rock.rect.y = -random.randint(100,400)
                    rock.rect.x = random.randint(0,330)
                    rock.rock_fall_y = 0


        #clear the display
        screen.blit(background,(0,0))

        #Update elements
        player_group.update()
        block_group.update()
        block_group.draw(screen)
        player_group.draw(screen)
        rock_group.draw(screen)
        rock_group.update(screen)


        show_score()
        show_button()

        #If dog falls out of screen, display gameover message.
        if gameover:
            gameover_text()
            show_score(BLACK,120,300)

        #Update
        pygame.display.flip()

#---------------------------------------------------------------------(main)


if __name__ == "__main__":
    main()
