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
                self.play.track.generate_track()
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
        self.track = Track(self.display, self.track_size)
    #displays the results
    def run(self):
        pass
        
#Track class
class Track:
    #initialises display
    def __init__(self, display, track_size):
        self.display = display
        self.track_size = track_size
    
    #generates the track
    def generate_track(self):
        #defining track coordinates
        x_offset = 740
        y_offset = 810
        start_x = x_offset
        start_y = y_offset
        path_positions = [start_x, start_y]
        #initialising direction
        direction = "right"
        STRAIGHT_PROBABILITY = 0.55
        TURNS = ['TOP RIGHT', 'TOP LEFT', 'BOTTOM LEFT', 'BOTTOM RIGHT']
        #starting track segments
        for _ in range(2):
            tracks = pygame.image.load('C:/NEA/NEA sprites/Straight horizontal.png').convert_alpha()
            #incrementing x_offset (allowing the track segments to connect to each other)
            x_offset += 110
            self.display.blit(tracks, (x_offset, y_offset))
            
            
        #Generate track segments based on pre-defined probabilities
        while (x_offset, y_offset) != (start_x, start_y):
            #random float number between 0 and 1
            probability = random.random()
            #if the probability is less than the straight probability
            if probability < STRAIGHT_PROBABILITY:
                #creating a right horizontal track segment
                if direction == "right":
                    #checking if the next track segment will collide with the pre-determined size of the track
                    if not self.track_size.collidepoint(x_offset + 200, y_offset):
                        #loading the bottom left track segment
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Bottom left turn.png').convert_alpha()  
                        #changing the y offset to allow the track segments to connect to each other
                        y_offset -= 41               
                        self.display.blit(tracks, (x_offset, y_offset))
                        #changing the direction that the straight track segments will face
                        direction = "up"
                        #changing the x and y offsets to allow the track segments to connect to each other
                        x_offset += 32
                        path_positions.append(x_offset, y_offset) 
                    else:
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Straight horizontal.png').convert_alpha()
                        #incrementing x offset, allowing the track segments to connect to each other
                        x_offset += 110
                        self.display.blit(tracks, (x_offset, y_offset))  
                        path_positions.append((x_offset, y_offset))
                #creating a left horizontal track segment
                elif direction == "left":
                    #checking if the next track segment will collide with the pre-determined size of the track
                    if not self.track_size.collidepoint(x_offset - 200, y_offset):
                        #loading the top right track segment
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Top right turn.png').convert_alpha()
                        #changing the x and y offset to allow the track segments to connect to each other
                        x_offset -= 41
                        y_offset -= 32
                        self.display.blit(tracks, (x_offset, y_offset))
                        #changing the direction that the next track segments will face
                        direction = "down" 
                        path_positions.append(x_offset, y_offset) 
                    else:
                        #decrementing x offset, allowing the track segments to connect to each other
                        x_offset -= 110
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Straight horizontal.png').convert_alpha()
                        self.display.blit(tracks, (x_offset, y_offset))
                        path_positions.append(x_offset, y_offset) 
                #creating a vertical upward track segment
                elif direction == "up":
                    #checking if the next track segment will collide with the pre-determined size of the track
                    if not self.track_size.collidepoint(x_offset, y_offset - 200):
                        #loading the top left track segment
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Top left turn.png').convert_alpha()
                        #changing the x and y offset to allow the track segments to connect to each other
                        x_offset -= 41
                        y_offset -= 32
                        self.display.blit(tracks, (x_offset, y_offset))
                        #changing the direction that the next track segments will face
                        direction = "left"
                        path_positions.append(x_offset, y_offset) 
                    else:
                        #decrementing y offset, allowing the track segments to connect to each other
                        y_offset -= 110
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Straight vertical.png').convert_alpha()
                        self.display.blit(tracks, (x_offset, y_offset))
                        path_positions.append(x_offset, y_offset) 
                #if direction == "down", creating a vertical downward track segment
                else:
                    #checking if the next track segment will collide with the pre-determined size of the track
                    if not self.track_size.collidepoint(x_offset, y_offset + 200):
                        #loading the bottom right track segment
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Bottom right turn.png').convert_alpha()
                        #changing the y offset to allow the track segments to connect to each other
                        y_offset += 32
                        self.display.blit(tracks, (x_offset, y_offset))
                        #changing the direction that the straight track segments will face
                        direction = "right"
                        #changing the x offset to allow the track segments to connect to each other
                        x_offset += 41 
                    else:
                        #incrementing y offset, allowing the track segments to connect to each other
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Straight vertical.png').convert_alpha()
                        y_offset += 110 
                        self.display.blit(tracks, (x_offset, y_offset))
            else:
                #randomly choose a track segment from the list of turns
                selected_track_element = random.choice(TURNS)
                #this limits the number of turns that can be placed
                TURNS.remove(selected_track_element)
                if len(TURNS) == 0:
                    STRAIGHT_PROBABILITY = 1
                #creating a top right turn track segment
                elif selected_track_element == 'TOP RIGHT': 
                    if direction == "left":
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Top right turn.png').convert_alpha()
                        #changing the x and y offsets to allow the track segments to connect to each other
                        x_offset -= 32
                        self.display.blit(tracks, (x_offset, y_offset))
                        y_offset += 41
                        #changing the direction that the next track segments will face
                        direction = "down"
                        #connect a straight downward vertical track segment
                        y_offset += 110
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Straight vertical.png').convert_alpha() 
                        self.display.blit(tracks, (x_offset, y_offset))

                #creating a top left turn track segment
                elif selected_track_element == 'TOP LEFT': 
                    if direction == "up":
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Top left turn.png').convert_alpha()
                        #changing the x and y offset to allow the track segments to connect to each other
                        x_offset -= 32
                        y_offset -= 41
                        self.display.blit(tracks, (x_offset, y_offset))
                        #changing the direction that the next track segments will face
                        direction = "left" 
                        #connect a straight left horizontal track segment
                        x_offset -= 110
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Straight horizontal.png').convert_alpha()
                        self.display.blit(tracks, (x_offset, y_offset))                    
                
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
                        #connect a straight vertical track segment
                        y_offset -= 110
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Straight vertical.png').convert_alpha()
                        self.display.blit(tracks, (x_offset, y_offset))
                
                #creating a bottom right turn track segment
                elif selected_track_element == 'BOTTOM RIGHT':
                    if direction == "down":
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Bottom right turn.png').convert_alpha()
                        #changing the y offset to allow the track segments to connect to each other
                        y_offset += 41
                        self.display.blit(tracks, (x_offset, y_offset))
                        #changing the direction that the straight track segments will face
                        direction = "right"
                        #changing the x offset to allow the track segments to connect to each other                      
                        x_offset += 32
                        #connect a straight horizontal track segment
                        tracks = pygame.image.load('C:/NEA/NEA sprites/Straight horizontal.png').convert_alpha()
                        x_offset += 110
                        self.display.blit(tracks, (x_offset, y_offset))
            if (x_offset, y_offset) in path_positions:
                break
            path_positions.append(x_offset, y_offset)  

class Position_Vector:
    def __init__(self, start_point, displacement_vector):
        self.start_point = start_point
        self.displacement_vector = displacement_vector

class Track:
    def __init__(self, startPos):
        self.startPos = startPos
        #adds the starting position to the list of points
        self.points = []#.append(self.startPos)

    #point is a tuple of x and y coordinates which gives the x and y displacements
    def add_Position_Vector(self, aVector, join_to_vector):

def is_point_on_segment(A,B,C):
    if C[0] <= max(A[0], B[0]) and C[0] >= min(A[0], B[0]) and C[1] <= max(A[1], B[1]) and C[1] >= min(A[1], B[1]):
        return True
    return False
#the line segments P1 to P2 and Q1 to Q2
def orientation(A, B, C):
    """"
    calculates the orientation for the line segment AB to the point C
        Args: 
            A: a point in 2D-space
            B: a point in 2D-space
            C: a point in 2D-space
    if the result is 0, then we have a straight line (C lies on AB)
    """
    return (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])

def line_segments_intersect(P1, P2, Q1, Q2):
    o1 = orientation(P1, P2, Q1)
    o2 = orientation(P1, P2, Q2)
    o3 = orientation(Q1, Q2, P1)
    o4 = orientation(Q1, Q2, P2)

    if o1*o2 < 0 and o3*o4 < 0:
        return True
    if o2 == 0 and 
#the orientation(A,B,C) of the line segment AB and point C. A(x1, y1), B(x2, y2), C(x3, y3)
#Orientation(A,B,C) = (x2 - x1)(y3 - y1) - (y2 - y1)(x3 - x1)
#can do it this way or calculate 1/2(abSinC)
#the line segments P1 to P2 and Q1 to Q2

if __name__ == '__main__':
    #creates object 'game' of class Game
    game = Game()
    #runs the game
    game.run()

https://www.geeksforgeeks.org/car-race-game-in-pygame/
https://stackoverflow.com/questions/66753321/best-way-to-create-a-2d-top-down-race-track-procedurally
