import pygame


# Setup
# Setup the display

SCREEN_TITLE = "Crossy"

SCREEN_WIDTH = 900

SCREEN_HEIGHT = 700

WHITE_COLOR = (255, 255, 255)

BLACK_COLOR = (0, 0, 0)

# Clock used to update game events and frames
# It determines how many times per second this loop will run
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class Game:

    TICK_RATE = 60 # Typical rate of 60, equivalent to FPS

    # Main game loop, used to update all gameplay such as movement, checks, and graphics
    # Runs until is_game_over = True

    def __init__(self, image_path, title, width, height):
        """
        Initializer for the game class to set up the width, height, and title
        """
        self.title = title
        self.width = width
        self.height = height

        # Create the window of specified size in white to display the game
        self.game_screen = pygame.display.set_mode((self.width, self.height))
        # Set the game window color to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(self.title)
        
        # Se the game's background
        background_img = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_img, (self.width, self.height))
    
    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0

        player_character = PlayerCharacter('player.png', self.width/2 - 25, self.height - 100, 50, 50)
        
        # Adding Enemies
        # Move and draw more enemies when we reach higher levels of difficulty   
        enemy_0 = NonPlayerCharacter('enemy.png', 20, 500, 50, 50)
        enemy_1 = NonPlayerCharacter('enemy.png', 20, 350, 50, 50)
        enemy_2 = NonPlayerCharacter('enemy.png', 20, 150, 50, 50)
        enemies = [enemy_0, enemy_1, enemy_2]
        
        treasure = GameObject('treasure.png', self.width/2 - 25, 50, 50, 50)

        # Speed increased as we advance in difficulty
        enemy_0.speed *= level_speed * 0.25
        enemy_1.speed *= level_speed * 0.30
        enemy_2.speed *= level_speed * 0.10

        while not is_game_over:

            # A loop to get all of the events occuring at any given time
            # Events are most often mouse movement, mouse and button clicks, or 
            # exit events
            for event in pygame.event.get():
                # If we have a quite type event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    is_game_over = True
                # Detect if any key is pressed down
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
            
                # Draw objects to the screen
                # pygame.draw.rect(game_screen, BLACK_COLOR, [350, 350, 100, 100])
                # pygame.draw.circle(game_screen, BLACK_COLOR, (400, 300), 50) 
                
                # Draw images to the screen
                # Images are treated like rectangles
                #self.game_screen.blit(player_image, (350, 350))

            # Redraw the screen
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0, 0))
            # Update the player position
            player_character.move(direction, self.height)
            # Draw the player at the new position
            player_character.draw(self.game_screen)

            # Move and draw the enemy character
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)
            if level_speed > 2:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if level_speed > 4:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            # Draw the treasure
            treasure.draw(self.game_screen)

            # End game Logic
            # Close game if we lose
            # Restart game loop if we win
            if player_character.detect_collision(treasure):
                is_game_over = True   
                did_win = True  
                text = font.render('You win! :)', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break  
            else:
                for enemy in enemies:
                    if player_character.detect_collision(enemy):
                        is_game_over = True
                        text = font.render('You lose! :(', True, BLACK_COLOR)
                        self.game_screen.blit(text, (300, 350))
                        pygame.display.update()
                        clock.tick(1)
                        break
                    
            # Update all game graphics
            pygame.display.update()
            # Tick the clock to update everything within the game and go to
            #  the next frame
            clock.tick(self.TICK_RATE)
        
        if did_win:
            self.run_game_loop(level_speed + 1)
        else:
            return


class GameObject:
    """Generic game object class"""

    def __init__(self, image_path, x, y, width, height):
        # Load images
        object_image = pygame.image.load(image_path)
        # Resize images
        self.image = pygame.transform.scale(object_image, (width, height))
        
        self.x_pos = x
        self.y_pos = y
        
        self.width = width
        self.height = height
    
    # Draw the object by blitting it onto the background (game screen)
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):
    """Character controled by the player"""

    speed = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.speed
        elif direction < 0:
            self.y_pos += self.speed
        
        if self.y_pos >= max_height - self.height:
            self.y_pos = max_height - self.height
    
    def detect_collision(self, other_body):
        """
        Returns False (no collision) if y positions and x positions do not overlap
        Returns True if x and y positions overlap
        """
        # We actually detect all situation the bodies DON'T collide
        if self.y_pos > other_body.y_pos + other_body.height:
            # We are below the other body
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            # We are above the other body
            return False
            
        if self.x_pos > other_body.x_pos + other_body.width:
            # We are to the right of the other body
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            # We are to the left of the other body
            return False
            
        return True
            

class NonPlayerCharacter(GameObject):
    """Character controled by the player"""

    speed = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, max_width):
        if self.x_pos <= self.width:
            self.speed = abs(self.speed)
        elif self.x_pos >= max_width - 2 * self.width:
            self.speed = -abs(self.speed)
        self.x_pos += self.speed
        

pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

# Quit pygame and the program
pygame.quit()
quit()