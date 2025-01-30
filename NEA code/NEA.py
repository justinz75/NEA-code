#import libraries
import pygame
import sys
from Track_controller import Track_controller

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
        self.track_size = pygame.Rect(260, 140, 1400, 800)
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
                track = Track_maker()
                track.draw_track(self.screen)
            #run game states
            self.states[self.gameStateManager.get_state()].run()
            #pygame.draw.rect(self.screen, (0, 0, 0), self.track_size)
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
        #initialise racetrack size
        self.track_size = pygame.Rect(260, 140, 1400, 800)
    #displays the results
    def run(self):
        pass
        
class Track_maker():
    def __init__(self):
        #initialise the track controller in the track maker
        self.__track_controller = Track_controller()
    
    def draw_track(self, display):
        #draw the track
        self.__track_controller.generate_track()
        line_segments = self.__track_controller.get_all_line_segments()
        for segment in line_segments:
            pygame.draw.line(display, (255, 0, 0), (segment.from_point.x, segment.from_point.y), (segment.to_point.x, segment.to_point.y), 5)

if __name__ == '__main__':
    #creates object 'game' of class Game
    game = Game()
    #runs the game
    game.run()
