#import libraries
import pygame
import sys
import random

#game window constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

#Track segment probabilities
STRAIGHT_PROBABILITY = 0.55
TURNS = ['TOP RIGHT', 'TOP LEFT', 'BOTTOM LEFT', 'BOTTOM RIGHT']

#Game class
class Game:
    def __init__(self):
        #initialise game
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        #initialise game states
        self.gameStateManager= GameStateManager('main menu')
        self.main_menu = Main_Menu(self.screen, self.gameStateManager)
        self.menu = Menu(self.screen, self.gameStateManager)
        self.game_controls = Game_Controls(self.screen, self.gameStateManager)
        self.pause = Pause(self.screen, self.gameStateManager)
        self.high_scores = High_Scores(self.screen, self.gameStateManager)
        self.results = Results(self.screen, self.gameStateManager)
        self.play = Playing(self.screen, self.gameStateManager)
        #initialise buttons for main menu
        self.play_button = pygame.Rect(855, 350, 170, 100)
        self.game_controls_button = pygame.Rect(633, 520, 615, 100)
        self.quit_button = pygame.Rect(856, 700, 157, 100)
        #dictionary of game states
        self.states = {'main menu': self.main_menu, 'menu': self.menu, 'game controls': self.game_controls, 'pause': self.pause, 'high scores': self.high_scores, 'results': self.results, 'play': self.play}
    
    def run(self):
        run = True
        while run:
            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #exit the game
                    run = False
                    pygame.quit()
                    sys.exit()
            #if the mouse is clicked and the current state is the main menu
            if event.type == pygame.MOUSEBUTTONDOWN and self.gameStateManager.get_state() == 'main menu':
                #get the mouse position
                mouse_pos = event.pos
                if self.play_button.collidepoint(mouse_pos):
                    #change the state to the menu
                    self.gameStateManager.set_state('menu')
                if self.game_controls_button.collidepoint(mouse_pos):
                    #change the state to the game controls
                    self.gameStateManager.set_state('game controls')
                if self.quit_button.collidepoint(mouse_pos):
                    #exit the game
                    run = False
                    pygame.quit()
                    sys.exit()
            self.key = pygame.key.get_pressed()
            if self.key[pygame.K_m] and (self.gameStateManager.get_state() == 'menu' or self.gameStateManager.get_state() == 'game controls'):
                self.gameStateManager.set_state('main menu')
            if self.key[pygame.K_c] and self.gameStateManager.get_state() == 'menu':
                self.gameStateManager.set_state('play')
                self.screen.fill((255, 255, 255))
                self.play.track.generate_track()
            #run game states
            self.states[self.gameStateManager.get_state()].run()
            #pygame.draw.rect(self.display, (0, 0, 0), self.results_button)
            #updates the display
            pygame.display.update()
            #ensures game runs at the correct fps
            self.clock.tick(FPS)

#Game state manager class
class GameStateManager:
    #initialise currentState
    def __init__(self, currentState):
        self.currentState = currentState
    #gets the current state of the program
    def get_state(self):
        return self.currentState
    #sets the current state of the program to the state needed
    def set_state(self, state):
        self.currentState = state

#Main menu class
class Main_Menu:
    #initialises display and gameStateManager
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        #load the background image
        self.background_image = pygame.image.load('C:/NEA/NEA sprites/Main menu.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    #displays the main menu
    def run(self):
        self.display.blit(self.background_image, (0, 0))

#Menu class
class Menu:
    #initialises display and gameStateManager
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        #load the background image
        self.background_image = pygame.image.load('C:/NEA/NEA sprites/Menu.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    #displays the menu
    def run(self):
        self.display.blit(self.background_image, (0, 0))

#Game controls description class
class Game_Controls:
    #initialises display and gameStateManager
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        #load the background image
        self.background_image = pygame.image.load('C:/NEA/NEA sprites/Game control description.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    #displays the game controls description
    def run(self):
        self.display.blit(self.background_image, (0, 0))

#Pause class
class Pause:
    #initialises display and gameStateManager
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        #load the background image
        self.background_image = pygame.image.load('C:/NEA/NEA sprites/Paused.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    #displays the pause menu
    def run(self):
        self.display.blit(self.background_image, (0, 0))

#High scores class
class High_Scores:
    #initialises display and gameStateManager
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        #load the background image
        self.background_image = pygame.image.load('C:/NEA/NEA sprites/High scores.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    #displays the high scores
    def run(self):
        self.display.blit(self.background_image, (0, 0))

#Results class
class Results:
    #initialises display and gameStateManager
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        #load the background image
        self.background_image = pygame.image.load('C:/NEA/NEA sprites/Results.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    #displays the results
    def run(self):
        self.display.blit(self.background_image, (0, 0))

#Playing class
class Playing:
    #initialises display and gameStateManager
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.track = Track(self.display)
    #displays the results
    def run(self):
        pass
        

#Track class
class Track:
    #initialises display
    def __init__(self, display):
        self.display = display
    
    #generates the track
    def generate_track(self):
        #defining track coordinates
        x_offset = 740
        y_offset = 540
        #initialising direction
        direction = "right"
        #starting track segments
        for _ in range(2):
            tracks = pygame.image.load('C:/NEA/NEA sprites/Straight horizontal.png').convert_alpha()
            x_offset += 110
            self.display.blit(tracks, (x_offset, y_offset))
            #incrementing x_offset (allowing the track segments to connect to each other)
            
        #Generate track segments based on pre-defined probabilities
        for _ in range(20):
            #random float number between 0 and 1
            probability = random.random()
            #if the probability is less than the straight probability
            if probability < STRAIGHT_PROBABILITY:
                #creating a right horizontal track segment
                if direction == "right":
                    tracks = pygame.image.load('C:/NEA/NEA sprites/Straight horizontal.png').convert_alpha()
                    #incrementing x offset, allowing the track segments to connect to each other
                    x_offset += 110
                    self.display.blit(tracks, (x_offset, y_offset))   
                #creating a left horizontal track segment
                elif direction == "left":
                    #decrementing x offset, allowing the track segments to connect to each other
                    x_offset -= 110
                    tracks = pygame.image.load('C:/NEA/NEA sprites/Straight horizontal.png').convert_alpha()
                    self.display.blit(tracks, (x_offset, y_offset))
                #creating a vertical upward track segment
                elif direction == "up":
                    #decrementing y offset, allowing the track segments to connect to each other
                    y_offset -= 110
                    tracks = pygame.image.load('C:/NEA/NEA sprites/Straight vertical.png').convert_alpha()
                    self.display.blit(tracks, (x_offset, y_offset))
                #if direction == "down", creating a vertical downward track segment
                else:
                    #incrementing y offset, allowing the track segments to connect to each other
                    y_offset += 110
                    tracks = pygame.image.load('C:/NEA/NEA sprites/Straight vertical.png').convert_alpha() 
                    self.display.blit(tracks, (x_offset, y_offset))
            else:
                #randomly choose a track segment from the list of turns
                selected_track_element = random.choice(TURNS)
                #creating a top right turn track segment
                if selected_track_element == 'TOP RIGHT': 
                    if direction == "left":
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Top right turn.png').convert_alpha()
                        #changing the x and y offsets to allow the track segments to connect to each other
                        x_offset -= 32
                        y_offset += 41
                        self.display.blit(tracks, (x_offset, y_offset))
                        #changing the direction that the next track segments will face
                        direction = "down"
                
                #creating a top left turn track segment
                elif selected_track_element == 'TOP LEFT': 
                    if direction == "up":
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Top left turn.png').convert_alpha()
                        #changing the x and y offset to allow the track segments to connect to each other
                        x_offset -= 41
                        y_offset -= 32
                        self.display.blit(tracks, (x_offset, y_offset))
                        #changing the direction that the next track segments will face
                        direction = "left"                     
                
                #creating a bottom left turn track segment
                elif selected_track_element == 'BOTTOM LEFT':
                    #if the number of left turns that have occurred is even and the direction is horizontal 
                    if direction == "right":
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Bottom left turn.png').convert_alpha()  
                        #changing the y offset to allow the track segments to connect to each other
                        y_offset -= 41               
                        self.display.blit(tracks, (x_offset, y_offset))
                        #changing the direction that the straight track segments will face
                        direction = "up"
                        #changing the x and y offsets to allow the track segments to connect to each other
                        x_offset += 32                     
                
                #creating a bottom right turn track segment
                elif selected_track_element == 'BOTTOM RIGHT':
                    if direction == "down":
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Bottom right turn.png').convert_alpha()
                        #changing the y offset to allow the track segments to connect to each other
                        y_offset += 32
                        self.display.blit(tracks, (x_offset, y_offset))
                        #changing the direction that the straight track segments will face
                        direction = "right"
                        #changing the x offset to allow the track segments to connect to each other                      
                        x_offset += 41

if __name__ == '__main__':
    #creates object 'game' of class Game
    game = Game()
    #runs the game
    game.run()
https://www.geeksforgeeks.org/car-race-game-in-pygame/
https://stackoverflow.com/questions/66753321/best-way-to-create-a-2d-top-down-race-track-procedurally
