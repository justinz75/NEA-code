import random
import sys
import threading
import time

import pygame.sprite

from Back_end import Point, LineSegment, Track
import pygame
from CONSTANTS import *

class Pygame_Point(Point):
    def __init__(self, x, y, screen_height):
        #initialise Pygame_Point with x, y coordinates and screen height
        super().__init__(x, y)
        self.screen_height = screen_height
        pygame_coords = self.pygame_coordinates()
        self.x, self.y = pygame_coords[0], pygame_coords[1]

    def pygame_coordinates(self):
        #convert mathematical coordinates to Pygame coordinates (invert y-axis)
        return self.x, self.screen_height - self.y
    
    def map_view_port(self, screen_top_left: 'Point', screen_bottom_right: 'Point', x_offset, y_offset):
        #this calculates the scale factor needed for the x and y coordinates
        scale_factor_x = (screen_bottom_right.x - screen_top_left.x)/100
        scale_factor_y = (screen_bottom_right.y - screen_top_left.y)/100
        #this adds the scale factor to the coordinates and creates a border around the track
        new_x = self.x * scale_factor_x + x_offset
        new_y = self.y * scale_factor_y + y_offset
        return Pygame_Point(new_x, new_y)
    
    def draw_on_screen(self, screen, screen_top_left, screen_bottom_right, x_offset, y_offset):
        #draws point on the screen
        screen_point = self.map_view_port(screen_top_left, screen_bottom_right, x_offset, y_offset)
        pygame.draw.circle(screen, (255, 255, 255), (screen_point.x, screen_point.y), 2)

class Pygame_LineSegment(LineSegment):
    def __init__(self, from_point, to_point, screen_height):
        #initialise Pygame_LineSegment with start and end points and screen height
        pygame_start_point = Pygame_Point(from_point.x, from_point.y, screen_height)
        pygame_end_point = Pygame_Point(to_point.x, to_point.y, screen_height)
        super().__init__(pygame_start_point, pygame_end_point)

    def scale_line_segment(self, screen_top_left, screen_bottom_right, x_offset, y_offset):
        #this scales the line segment to fit the screen
        new_start_point = self.from_point.map_view_port(screen_top_left, screen_bottom_right, x_offset, y_offset)
        new_finish_point = self.to_point.map_view_port(screen_top_left, screen_bottom_right, x_offset, y_offset)
        return Pygame_LineSegment(new_start_point, new_finish_point)

    def calculate_by_bezier(self):
        #calculates Bezier points for the line segment
        return_points = super().calculate_by_bezier()
        return return_points

class Pygame_Track(Track):
    def __init__(self, name, number_of_straights, start_x, start_y, screen_height):
        #initialise Pygame_Track with name, number_of_straights, start point and screen height
        super().__init__(name, number_of_straights, start_x, start_y)
        self.screen_height = screen_height

    def draw_on_pygame(self, screen):
        """
        Draws self onto the screen scaled by the given scale_factor
        :param screen:  pygame screen
        :param scale_factor: amount to scale (e.g. 5 will be mapping to the screen (0,0) to (500,500)
        """
        for ls in self._line_segments:
            #scaling the coordinates
            screen_start = (ls.from_point.x, ls.from_point.y)
            screen_end = (ls.to_point.x, ls.to_point.y)
            pygame.draw.line(screen, (255, 0, 0), screen_start, screen_end, 2)

            #text colour and font
            #text_colour = (0,0,0)
            #font = pygame.font.Font(None, 20)
            #the coordinates are displayed
            #text_surface = font.render(f"{str(ls.to_point.x)}, {str(ls.to_point.y)})", True, text_colour)
            #screen.blit(text_surface, screen_start)
            # points = ls.calculate_by_bezier()
            # for i in range(101):
            #     if points:
            #         pygame.draw.circle(screen, (255, 255, 0), (points[i].x, points[i].y), 2)

    def __str__(self):
        #return string representation of track
        returnStr = f"Track Name: {self.name}\n"
        for ls in self._line_segments:
            returnStr = returnStr + f"Line segment {str(ls)}\n"
        return returnStr
    
    def draw_bridges(self, screen, bezier_bridges):
        for bridge_points in bezier_bridges:
            for i in range(len(bridge_points)-1):
                pygame.draw.circle(screen, (255, 0, 0), (bridge_points[i].x, SCREEN_HEIGHT-bridge_points[i].y), 2)
    
    def draw_track(self, screen):
        #draw track/bezier points on screen
        self.draw_on_pygame(screen)
        for ls in self.get_all_line_segments(): #type: 'LineSegment'
            bezier_points = ls.bezier_points
            for i in range(len(bezier_points)):
                pygame.draw.circle(screen, BLACK, (bezier_points[i].x, bezier_points[i].y), TRACK_WIDTH)
            
    # def draw_bezier_track(self, screen):
    #     for ls in self._line_segments:
    #         for i in range(len(ls.control_points)-2):
    #             Point.draw_on_screen(screen, Point(TOP_LEFT[0], TOP_LEFT[1]), Point(BOTTOM_RIGHT[0], BOTTOM_RIGHT[1]), X_OFFSET, Y_OFFSET)
    #             b_points = (ls.from_point, ls.control_points[i], ls.control_points[i+1], ls.to_point)
    
class Track_Factory:
    @staticmethod
    def create_pygame_track(track, screen_height):
        #create Pygame_Track from a Track object
        pygame_track = Pygame_Track(track.name, track.get_num_straights(), track.get_start_finish_point().x,
                                    track.get_start_finish_point().y, screen_height)
        for ls in track.get_all_line_segments():
            pygame_line_segment = Pygame_LineSegment(ls.from_point, ls.to_point, screen_height)
            pygame_track.add_line_segment(pygame_line_segment)
        return pygame_track

class Car_Sprite(pygame.sprite.Sprite):
    def __init__(self, colour, initial_pos: 'Point'):
        super().__init__()
        self.colour = colour
        self.screen_height = SCREEN_HEIGHT
        self.screen_width = SCREEN_WIDTH
        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.initial_pos = initial_pos
        self.rect.x = self.initial_pos.x
        self.rect.y = self.initial_pos.y

    def update(self, new_pos: 'Point'):
        self.rect.x = new_pos.x
        self.rect.y = new_pos.y

class AI_car:
    def __init__(self, difficulty, colour, pygame_track: 'Pygame_Track', screen):
        self.pygame_track = pygame_track
        self.screen = screen
        #current bezier and straight index
        self.current_straight_index = 0
        self.current_bezier_index = 0
        self.colour = colour
        self.difficulty = difficulty
        #gets current position of the car
        self.current_pos = self.get_next_pos()
        #ensures thread-safe operations
        self.lock = threading.Lock()
        #track if the thread is running
        self.running = False
        self.thread = None
        self.sprite = Car_Sprite(colour, self.current_pos)

    def start_animation(self):
        #start thread and animation of car
        self.running = True
        self.thread = threading.Thread(target=self.animate_car)
        self.thread.start()

    def stop_animation(self):
        #stops animation thread
        self.running = False
        if self.thread is not None:
            self.thread.join()

    def animate_car(self):
        #continuously updates car while thread is running
        while self.running:
            with self.lock:
                #gets next position of the car
                new_position = self.get_next_pos()
                self.current_pos = new_position
                #draws car at the new position
                pygame.draw.circle(self.screen, self.colour, (new_position.x, new_position.y), 2, 2)
            #control animation speed
            time.sleep(1/(FPS + 20 - self.difficulty * 10))


    def get_pos(self):
        #gets current position of the car
        with self.lock:
            return self.current_pos

    def get_next_pos(self):
        straights = self.pygame_track.get_all_line_segments()
        current_straight = straights[self.current_straight_index] #type: 'Pygame_LineSegment'
        current_bezier = current_straight.bezier_points[self.current_bezier_index] #type: 'Pygame_Point'
        if current_bezier == current_straight.to_point:  #end of the current straight
            #reached the end of current line segment - go to the next set of bezier points
            self.current_straight_index = (self.current_straight_index + 1) % len(straights)
            self.current_bezier_index = 0
        else:
            self.current_bezier_index = (self.current_bezier_index + 1) % len(current_straight.bezier_points)

        #depending on the difficult, go off track a little
        if self.difficulty == 0: #hard
            return current_bezier
        elif self.difficulty == 1: #medium
            if random.randint(1,50) == 1:
                return Point(current_bezier.x + 3, current_bezier.y + 3)
            else:
                return current_bezier
        else: #easy
            if random.randint(1,25) == 1:
                return Point(current_bezier.x + 3, current_bezier.y + 3)
            else:
                return current_bezier



class Race:
    def __init__(self, screen, screen_height, laps, difficulty):
        self.screen = screen
        self.screen_height = screen_height
        self.cars = []
        track = Track.generate_track('Track', 10, 800, 500)
        self.pygame_track = Track_Factory.create_pygame_track(track, self.screen_height)
        if difficulty == 0: # hard race
            self.cars.append(AI_car(0, RED, self.pygame_track, self.screen))
            self.cars.append(AI_car(1, BLUE, self.pygame_track, self.screen))
            self.cars.append(AI_car(1, BLUE, self.pygame_track, self.screen))
            self.cars.append(AI_car(2, GREEN, self.pygame_track, self.screen))
        elif difficulty == 1:
            self.cars.append(AI_car(1, BLUE, self.pygame_track, self.screen))
            self.cars.append(AI_car(1, BLUE, self.pygame_track, self.screen))
            self.cars.append(AI_car(2, GREEN, self.pygame_track, self.screen))
            self.cars.append(AI_car(2, GREEN, self.pygame_track, self.screen))
        else:
            self.cars.append(AI_car(2, GREEN, self.pygame_track, self.screen))
            self.cars.append(AI_car(2, GREEN, self.pygame_track, self.screen))
        self.laps = laps
        self.running = False
        self.difficulty = difficulty

    def begin_race(self):
        #starts race by drawing track and animating AI cars
        self.pygame_track.draw_track(self.screen)
        for car in self.cars:
            car.start_animation()

    def stop_race(self):
        #stops race by stopping all car animations
        for car in self.cars:
            car.stop_animation()

    def run_game(self):
        #runs game loop to update display and handle events
        #pygame clock controls FPS
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            #handle user input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            #draw each AI car at its current position
            for AI_car in self.cars:
                x_pos, y_pos = AI_car.current_pos.x, AI_car.current_pos.y
                pygame.draw.circle(screen, AI_car.colour, (x_pos, y_pos), 5, 2)
            #updates screen
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    #set screen dimensions and create screen
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(DARK_GREEN)
    #create and start race
    race = Race(screen, SCREEN_HEIGHT, 3, 0)
    race.begin_race()
    #run main game loop
    try:
        race.run_game()
    #ensures all animations are stopped properly
    finally:
        race.stop_race()

    # while run:
    #     # event handler
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             # exit the game
    #             run = False
    #             pygame.quit()
    #             sys.exit()
    #     pygame.display.flip()

