# Jumping Dog
### Video Demo https://youtu.be/aW94jHjtCpE
### Description
My project is a simple game in which a player controls a dog to go up the blocks as high as possible, while avoiding the falling rocks. I decided to make this game because I remembered the game "Doodle Jump" being popular in middle school and I wanted to create a similar but simpler game on my own.

I only have one file for the project called "project.py". I first imported two modules: Pygame and random. The Pygame module was needed for me to load different elements of game such as music and sprites and to update the screen. The random module was needed to randomize the position of the rocks.

#### Screen Size
The screen size of the game is 400 in width and 700 in height, which is fairly small. I chose this size because
 A. Small size limits the spaces available for player and makes the game more challenging
 B. if it takes small space, people can easily play the game during small breaks.

#### Images
I downloaded most of the images from a website where people post game images. I used images specifically designed for games instead of generic images because I wanted to make it more realistic.

#### Music and sound
I wanted the mood of the game to be overall cheerful and relaxed, so I used an upbeat music.
I implemented a sound button to meet the demand of the audience who wants to play the game silently.
There is a sound effect played every time the dog jumps, as I thought that this adds to the joyful mood and also make the game play more enjoyable.

#### Sprites
I created Sprites (player, blocks, and rocks) using what I had learned from object-oriented programming lesson. At first I was planning to use the normal objects, but I realized that it's more convenient to use Sprites. By using  objects, I was able to combine a lot of functionality in one place, making the code more concise.


#### Random
I wanted to include an element of randomness to avoid predictability, so I randomized the position of the blocks and the rocks, as well as their starting position (for rocks).

#### Centering the dog
At first the position of the blocks remained the same while the dog moved (on the screen), however I soon realized that this does not really work, since the dog will eventually move out of the screen. So, I fixed the dog at the center and moved everything else whever the dog jumped or moved to the sides.

#### Speed of falling down
I experimented with this quite a few times(altering some coefficients in the kinematics equation) to find the most "realistic" function.


