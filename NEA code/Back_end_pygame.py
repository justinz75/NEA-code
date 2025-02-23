import random
import sys
import threading
import time
from math import degrees, atan2, sin, cos, radians, sqrt
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
        pygame.draw.circle(screen, WHITE, (screen_point.x, screen_point.y), 2)

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
        self.finish_line = None

    def draw_on_pygame(self, screen):
        #draws self onto the screen
        for ls in self._line_segments:
            #retrieves coordinates of the start and end points of the line segment
            screen_start = (ls.from_point.x, ls.from_point.y)
            screen_end = (ls.to_point.x, ls.to_point.y)
            pygame.draw.line(screen, (255, 0, 0), screen_start, screen_end, 2)


    def __str__(self):
        #return string representation of track
        returnStr = f"Track Name: {self.name}\n"
        for ls in self._line_segments:
            returnStr = returnStr + f"Line segment {str(ls)}\n"
        return returnStr
    
    def draw_checkered_pattern(self, screen, p1, p2):
        #number of checks
        num_checks = 5
        for i in range(num_checks):
            #alternates grey and white
            color = WHITE if i % 2 == 0 else GREY
            #interpolate positions
            t1 = i / num_checks
            t2 = (i + 1) / num_checks
            c1 = (p1[0] * (1 - t1) + p2[0] * t1, p1[1] * (1 - t1) + p2[1] * t1)
            c2 = (p1[0] * (1 - t2) + p2[0] * t2, p1[1] * (1 - t2) + p2[1] * t2)
            #draws checks
            pygame.draw.line(screen, color, c1, c2, 3)
    
    def draw_finish_line(self, screen):
        #gets first bezier point
        first_segment = self.get_all_line_segments()[0]
        start_bezier = first_segment.bezier_points[0]
        #next bezier point
        end_bezier = first_segment.bezier_points[1]  
        #calculates perpendicular direction
        dx = end_bezier.x - start_bezier.x
        dy = end_bezier.y - start_bezier.y
        length = sqrt(dx**2 + dy**2)
        perp_x = -dy / length
        perp_y = dx / length
        #width of the finish line is the width of the track
        finish_width = TRACK_WIDTH
        #define finish line endpoints
        p1 = (start_bezier.x + perp_x * finish_width, start_bezier.y + perp_y * finish_width)
        p2 = (start_bezier.x - perp_x * finish_width, start_bezier.y - perp_y * finish_width)
        #draws a checkered finish line
        self.draw_checkered_pattern(screen, p1, p2)
        self.finish_line = pygame.Rect(p1[0], p1[1], p2[0]-p1[0], p2[1]-p1[1])
        
    def draw_bridges(self, screen, bezier_bridges):
        for bridge_points in bezier_bridges:
            for i in range(len(bridge_points)-1):
                pygame.draw.circle(screen, (255, 0, 0), (bridge_points[i].x, SCREEN_HEIGHT-bridge_points[i].y), 2)
    
    def draw_track(self, screen):
        #draw track/bezier points on screen
        self.draw_on_pygame(screen)
        for ls in self.get_all_line_segments():
            bezier_points = ls.bezier_points
            for i in range(len(bezier_points)):
                pygame.draw.circle(screen, TRACK_COLOUR, (bezier_points[i].x, bezier_points[i].y), TRACK_WIDTH)

        self.draw_finish_line(screen)
    
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

class AI_car:
    def __init__(self, screen, difficulty, pygame_track: 'Pygame_Track'):
        self.pygame_track = pygame_track
        self.screen = screen
        #current bezier and straight index
        self.current_straight_index = 0
        self.current_bezier_index = 0
        self.difficulty = difficulty
        #gets previous position of car
        self.save_current_pos = None
        #gets current position of the car
        self.current_pos = self.get_next_pos()
        #ensures thread-safe operations
        self.lock = threading.Lock()
        #track if the thread is running
        self.running = False
        self.thread = None
        #scales the car
        scaled_car = self.scale_car(HUMAN_CAR, 0.3)
        self.width = scaled_car.get_rect().width
        self.height = scaled_car.get_rect().height

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

    def scale_car(self, img, factor):
        #calculates the new size of the image by multiplying its width and height by the scaling factor
        size = round(img.get_width() * factor), round(img.get_height() * factor)
        #scales the image
        return pygame.transform.scale(img, size)

    def animate_car(self):
        #continuously updates car while thread is running
        while self.running:
            with self.lock:
                #gets next position of the car
                new_position = self.get_next_pos()
                angle = self.get_angle(self.current_pos, new_position)
                self.current_pos = new_position
                #chooses what car to scale and display based on difficulty
                if self.difficulty == 0:
                    scaled_car = self.scale_car(HARD_AI_CAR, 0.3)
                elif self.difficulty == 1:
                    scaled_car = self.scale_car(MEDIUM_AI_CAR, 0.3)
                elif self.difficulty == 2:
                    scaled_car = self.scale_car(EASY_AI_CAR, 0.3) 
                #rotate car
                rotated_car = self.rotate_ai_car(scaled_car, angle)
                #gets correct position to draw the image
                car_rect = rotated_car.get_rect(center=(new_position.x, new_position.y))
                #draws car on screen
                self.screen.blit(rotated_car, car_rect.topleft)
            #control animation speed
            time.sleep(1/(FPS + 100 - self.difficulty * 50))

    def get_pos(self):
        #gets current position of the car
        with self.lock:
            return self.current_pos.x, self.current_pos.y

    def get_next_pos(self):
        straights = self.pygame_track.get_all_line_segments()
        current_straight = straights[self.current_straight_index] #type: 'Pygame_LineSegment'
        current_bezier = current_straight.bezier_points[self.current_bezier_index] #type: 'Pygame_Point'
        self.save_current_pos = current_bezier
        if current_bezier == current_straight.to_point:  #end of the current straight
            #reached the end of current line segment - go to the next set of bezier points
            self.current_straight_index = (self.current_straight_index + 1) % len(straights)
            self.current_bezier_index = 0
        else:
            self.current_bezier_index = (self.current_bezier_index + 1) % len(current_straight.bezier_points)
        return current_bezier

    def get_angle(self, current_pos, next_pos):
        #gets the change in angle
        dx = next_pos.x - current_pos.x
        dy = next_pos.y - current_pos.y
        #dy is negative because the y axis is inverted on Pygame
        return degrees(atan2(-dy, dx))

    def rotate_ai_car(self, img, angle):
        #rotates the image based on the angle that is passed in
        return pygame.transform.rotate(img, angle)

class Human_Car:
    def __init__(self, screen, speed, rotation, position: 'Pygame_Point', pygame_track: 'Pygame_Track', upgrade_speed = 15):
        #set screen, speed, upgrade_speed, position and pygame track
        self.screen = screen
        self.speed = speed
        self.upgrade_speed = upgrade_speed
        self.position = position
        self.pygame_track = pygame_track
        #ensures thread-safe operations
        self.lock = threading.Lock()
        #initialises running and thread
        self.running = False
        self.thread = None
        #tells us direction in x and y, with 0, 0
        self.direction = [0, 0]
        self.rotation = rotation
        #initialises angle of car
        self.angle = 0
        #scale image
        scaled_car = self.scale_car(HUMAN_CAR, 0.3)
        self.width = scaled_car.get_rect().width
        self.height = scaled_car.get_rect().height
        #initialise boost_active
        self.boost_active = False
        #track last boost time
        self.last_boost_time = time.time()
        #initialise boost duration (in seconds)
        self.boost_duration = 5
        #initialise boost time remaining
        self.boost_time_remaining = 30
        #initialise boost start time
        self.boost_start_time = 0

    def rotate(self, left=False, right=False):
        #increment or decrement angle by its rotation
        if left:
            self.angle += self.rotation
        elif right:
            self.angle -= self.rotation
        self.angle %= 360

    def rotate_centre(self, image, top_left, angle):
        #rotate image
        rotated_image = pygame.transform.rotate(image, angle)
        #display image without changing the x and y coordinates of the image
        new_car = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
        self.screen.blit(rotated_image, new_car.topleft)

    def update_pos(self):
        #continuously update position of car while thread is running
        while self.running:
            #ensures thread-safe operations
            with self.lock:
                dx, dy = self.direction[0], self.direction[1]
                if dx != 0 or dy != 0:
                    #calculate angle based on direction
                    self.angle = degrees(atan2(-dy, dx))
                #convert degrees to radians
                rad_angle = radians(self.angle)
                #calculate new position of car with speed and angle
                new_position_x = self.position.x + self.speed * cos(rad_angle)
                new_position_y = self.position.y + self.speed * -sin(rad_angle)   
                #check if car is on track
                if self.can_move(Point(new_position_x, new_position_y)):
                    self.position.x = new_position_x
                    self.position.y = new_position_y            
            #control speed of car
            time.sleep(1/(FPS+self.upgrade_speed))
                      
    def set_direction(self, new_direction):
        #sets a new direction
        with self.lock:
            self.direction = new_direction

    def get_pos(self):
        #gets the position of the car
        with self.lock:
            return self.position.x, self.position.y

    def scale_car(self, img, factor):
        #calculates the new size of the image by multiplying its width and height by the scaling factor
        size = round(img.get_width() * factor), round(img.get_height() * factor)
        #scales image
        return pygame.transform.scale(img, size)

    def draw(self):
        #draws and rotates the human car
        scaled_car = self.scale_car(HUMAN_CAR, 0.3)
        self.rotate_centre(scaled_car, self.get_pos(), self.angle)

    def start(self):
        #start thread of human car
        self.running = True
        self.thread = threading.Thread(target=self.update_pos)
        self.thread.start()

    def stop(self):
        #stops thread of human car
        self.running = False
        if self.thread:
            self.thread.join()

    def is_car_on_track(self, p: 'Pygame_Point'):
        for ls in self.pygame_track.get_all_line_segments():
            for bezier_point in ls.bezier_points:
                if p.distance_to(bezier_point) < (TRACK_WIDTH+10)//2:
                    #found a bezier point where the car is on the track
                    return True
        return False

    def can_move(self, p: 'Pygame_Point'):
        return self.is_car_on_track(p)

    def can_boost(self):
        #allow boost if 30 seconds have passed since last boost
        return time.time() - self.last_boost_time >= 30 and not self.boost_active

    def boost_speed(self):
        if self.can_boost():
            self.boost_active = True
            #double speed
            self.speed *= 2
            #update last boost time
            self.last_boost_time = time.time()
            #start timer to end boost in 5 seconds
            self.boost_end_time = time.time() + self.boost_duration

    def update_boost(self):
        if self.boost_active:
            if time.time() - self.boost_end_time:
                #reset speed
                self.speed /= 2 
                #end boost
                self.boost_active = False 
                self.boost_time_remaining = 30      
        else:
            #check if boost duration is not already available
            if self.boost_time_remaining > 0:
                #check if one second has past since last update
                if time.time() - self.boost_start_time >= 1:
                    #boost time is decremented
                    self.boost_time_remaining -= 1
                    self.boost_start_time = time.time() 
                
class Race:
    def __init__(self, screen, screen_height, laps, difficulty):
        #screen and screen height are initialised
        self.screen = screen
        self.screen_height = screen_height
        #list of ai cars is initially empty
        self.ai_cars = []
        #track is generated
        track = Track.generate_track('Track', 10, 800, 500)
        self.pygame_track = Track_Factory.create_pygame_track(track, self.screen_height)
        #human car is initialised
        self.human_car = Human_Car(screen, 0.42, 2, Pygame_Point(self.pygame_track.get_start_finish_point().x, self.pygame_track.get_start_finish_point().y, SCREEN_HEIGHT), self.pygame_track)
        #lap counter for each car
        self.car_laps = {}
        #laps of the track needed
        self.laps = laps + 1
        #add the human car to the laps
        self.car_laps[self.human_car] = self.laps
        if difficulty == 0: #hard race
            self.ai_cars.append(AI_car(self.screen, 0, self.pygame_track))
            self.ai_cars.append(AI_car(self.screen, 1, self.pygame_track))
            self.ai_cars.append(AI_car(self.screen, 2, self.pygame_track))
        elif difficulty == 1: #medium race
            self.ai_cars.append(AI_car(self.screen, 1, self.pygame_track))
            self.ai_cars.append(AI_car(self.screen, 2, self.pygame_track))
        elif difficulty == 2: #easy race
            self.ai_cars.append(AI_car(self.screen, 2, self.pygame_track))
        #this adds the cars to the laps dictionary
        self.add_ai_cars_to_laps()
        #the game is initially not running
        self.running = False
        #difficulty initialised
        self.difficulty = difficulty
        self.just_crossed = set()
        #initialise dictionary for lap times
        self.car_lap_times = {}  
        #initialise dictionary for lap start times
        self.car_lap_start_times = {} 
        #initialise human car inside the car_lap_times and car_lap_start_times
        self.car_lap_times[self.human_car] = []
        self.car_lap_start_times[self.human_car] = time.time()
        self.first_lap_removed = False

    def check_ai_finish(self, car: 'AI_car'):
        #position of car is retrieved
        car_pos = car.get_pos()
        #car is defined as a Rect
        car_rect = pygame.Rect(car_pos[0], car_pos[1], car.width, car.height)
        #assumes the finish line is a Rect
        finish_line = self.pygame_track.finish_line
        #checks for collision and if the car had just crossed
        if car_rect.colliderect(finish_line) and car not in self.just_crossed:
            #lap is decremented
            self.car_laps[car] -= 1
            #prints which car completed the lap
            print(f"AI Car {self.ai_cars.index(car) + 1} completed a lap! Remaining laps: {self.car_laps[car]}")
            #this prevents multiple decrements of the car
            self.just_crossed.add(car)
            #returns true if the AI has finished the race  
            if self.car_laps[car] <= 0:
                return True
        #resets if the car moves away from the finish line
        elif not car_rect.colliderect(finish_line):
            self.just_crossed.discard(car)  

    def check_human_finish(self):
        #position of car is retrieved
        car_pos = self.human_car.get_pos()
        #car is defined as a Rect
        car_rect = pygame.Rect(car_pos[0], car_pos[1], self.human_car.width, self.human_car.height)
        #assumes finish line is a Rect
        finish_line = self.pygame_track.finish_line
        if car_rect.colliderect(finish_line) and self.human_car not in self.just_crossed:
            #lap is decremented
            self.car_laps[self.human_car] -= 1
            #prints when the human car completes the lap
            print(f"Human Car completed a lap! Remaining laps: {self.car_laps[self.human_car]}")
            self.just_crossed.add(self.human_car)
            #update lap times only when the car crosses the finish line
            current_time = time.time()
            lap_time = current_time - self.car_lap_start_times[self.human_car]
            #only valid times appended
            self.car_lap_times[self.human_car].append(lap_time)
            #reset start time for the next lap
            self.car_lap_start_times[self.human_car] = current_time
            #remove the first lap time 
            if self.car_laps[self.human_car] == 3 and not self.first_lap_removed:
                del self.car_lap_times[self.human_car][0]
                #ensures only one lap is removed
                self.first_lap_removed = True
            #returns true if the human has finished the race 
            if self.car_laps[self.human_car] <= 0:
                return True
            else:
                return False
        #resets if the car moves away from the finish line
        elif not car_rect.colliderect(finish_line):
            self.just_crossed.discard(self.human_car) 
    
    def display_lap(self):
        #display lap counter
        font = pygame.font.Font(None, 36)
        lap_counter_text = f"Laps: {self.car_laps[self.human_car]}"
        lap_text = font.render(lap_counter_text, True, WHITE)
        #displayed at the top left
        screen.blit(lap_text, (10, 50))  
    
    def add_ai_cars_to_laps(self):
        #adds the ai_car 
        for ai_car in self.ai_cars:
            self.car_laps[ai_car] = self.laps

    def begin_race(self):
        #starts race by drawing track and animating AI cars
        self.pygame_track.draw_track(self.screen)
        for car in self.ai_cars:
            car.start_animation()

    def stop_race(self):
        #stops race by stopping all car animations
        for car in self.ai_cars:
            car.stop_animation()
    
    def display_time(self, race_start_time):
        #calculate elapsed time
        elapsed_time = time.time() - race_start_time
        #set font and size
        font = pygame.font.Font(None, 36)
        #convert time to minutes and seconds
        #get total seconds
        elapsed_seconds = int(elapsed_time)
        #calculate minutes
        minutes = elapsed_seconds // 60
        #calculate seconds
        seconds = elapsed_seconds % 60
        #render timer
        elapsed_time_str = f"{minutes}:{seconds:02d}"
        timer_text = font.render(elapsed_time_str, True, WHITE)
        #display timer on the top left of the screen
        self.screen.blit(timer_text, (10, 10))

    def announce_winner(self, winner, time):
        #fills the screen dark blue
        screen.fill(DARK_BLUE)
        #set font and size
        font = pygame.font.Font(None, 50)
        if winner in self.ai_cars:
            winner_text = font.render(f"AI car Wins!", True, WHITE)
        else:
            winner_text = font.render(f"User Wins!", True, WHITE)
        #convert time to minutes and seconds
        minutes = int(time) // 60
        seconds = int(time) % 60
        time_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, WHITE)
        self.screen.blit(winner_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        self.screen.blit(time_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100))
        pygame.display.flip()
        #displays for 3 seconds
        pygame.time.delay(3000)  
            
    def display_place(self, place):
        #set font and size
        font = pygame.font.Font(None, 36)
        #render place with its appropriate suffix
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(place if place < 4 else 0, "th")
        place_text = font.render(f"Place: {place}{suffix}", True, WHITE)    
        #display text in the top right of the screen
        self.screen.blit(place_text, (SCREEN_WIDTH - 200, 10))

    def get_player_place(self):
        #starts in last place
        place = min(len(self.ai_cars) + 1, 4)    
        #compare laps completed with each AI car
        for car in self.ai_cars:
            if self.car_laps[car] > self.car_laps[self.human_car]:  
                #if an AI car has more laps, decrease the player's position
                place = max(place - 1, 0) 
            #limit to first place
            elif self.car_laps[car] < self.car_laps[self.human_car]:  
                #if the AI car has fewer laps, the player moves up and limits last place to 4
                place = min(place + 1, 4)  
        #return final place
        return place

    def display_fastest_lap(self):
        font = pygame.font.Font(None, 36)
        #ensures lap time exists and only updates after a lap is complete
        if not self.car_lap_times[self.human_car] or self.car_laps[self.human_car] == 3: 
            fastest_lap_text = "Fastest Lap: N/A"
        else:
            #takes the quickest time
            fastest_lap_time = min(self.car_lap_times[self.human_car])
            #convert time to minutes and seconds
            minutes = int(fastest_lap_time) // 60
            seconds = int(fastest_lap_time % 60) 
            fastest_lap_text = f"Fastest Lap: {minutes}:{seconds:02d}"
        #render fastest lap text
        text_surface = font.render(fastest_lap_text, True, WHITE)
        self.screen.blit(text_surface, (SCREEN_WIDTH - 250, 50))
    
    def display_boost(self):
        boost_time_remaining = self.human_car.boost_time_remaining
        #remaining boost time is a string
        boost_time_str = f"Boost: {boost_time_remaining}s"
        #set font and size
        font = pygame.font.Font(None, 36)
        #render time for boost text
        boost_time_text = font.render(boost_time_str, True, WHITE)
        #display boost time on the bottom right of the screen
        self.screen.blit(boost_time_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40))

    def run_game(self):
        #runs game loop to update display and handle events
        #pygame clock controls FPS
        clock = pygame.time.Clock()
        self.human_car.start()
        self.running = True
        #start race timer
        start_time = time.time()
        #save start of race time
        race_start_time = start_time
        while self.running:
            #clear screen
            self.screen.fill(DARK_GREEN)
            #redraw track
            self.pygame_track.draw_track(self.screen)
            #display lap counter
            self.display_lap()
            #display race time
            self.display_time(race_start_time)
            #display fastest lap time
            self.display_fastest_lap()
            #determine user's current place
            user_place = self.get_player_place()
            self.display_place(user_place)
            #update boost of car
            self.human_car.update_boost()
            #display boost time
            self.display_boost()

            #handle user input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    #detects if a key is pressed
                    keys = pygame.key.get_pressed()
                    #move upwards
                    if keys[pygame.K_w]:
                        self.human_car.set_direction([0, -1])
                    #moves downwards
                    elif keys[pygame.K_s]:
                        self.human_car.set_direction([0, 1])
                    #moves and rotates left
                    elif keys[pygame.K_a]:
                        self.human_car.set_direction([-1, 0])
                        self.human_car.rotate(left=True)
                    #moves and rotates right
                    elif keys[pygame.K_d]:
                        self.human_car.set_direction([1, 0])
                        self.human_car.rotate(right=True)
                    #boosts the car
                    elif keys[pygame.K_SPACE] and self.human_car.can_boost():
                        self.human_car.boost_speed()
                    else:
                        self.human_car.set_direction([0, 0])
            #draws user car
            self.human_car.draw()

            #check if any AI car has finished
            for car in self.ai_cars:
                if self.check_ai_finish(car):
                    #stops race and AI thread
                    self.stop_race()
                    #stops human car thread
                    self.human_car.stop()
                    self.running = False
                    #announce AI as winner along with its time
                    elapsed_ai_time = time.time() - race_start_time
                    self.announce_winner(car, elapsed_ai_time)

            #check if user finished
            if self.check_human_finish():
                #stops the thread
                self.human_car.stop()
                #stops race and AI thread
                self.stop_race()
                self.running = False
                #announce user as winner along with their time
                elapsed_human_time = time.time() - race_start_time
                self.announce_winner(self.human_car, elapsed_human_time)

            #updates screen
            pygame.display.flip()
            clock.tick(FPS)

def display_countdown(screen, font, countdown_time, screen_width, screen_height):
    #record start time of countdown
    start_time = time.time()
    countdown_finished = False
    #loop until countdown finishes
    while not countdown_finished:
        #calculate the elapsed time since the start of the countdown
        elapsed_time = time.time() - start_time
        #calculate the remaining time for the countdown
        remaining_time = countdown_time - int(elapsed_time)
        #check if countdown has finished
        if remaining_time <= 0:
            remaining_time = 0
            countdown_finished = True
        else:
            #render remaining time as text
            countdown_text = font.render(str(remaining_time), True, WHITE)
            #centre text on screen
            text_rect = countdown_text.get_rect(center=(screen_width // 2, screen_height // 2))
            #clear screen before countdown
            screen.fill(BLACK)
            #display countdown
            screen.blit(countdown_text, text_rect)
            pygame.display.flip()
        if remaining_time == 0:
            #fills the screen black and renders displays "Go!" in the middle of the screen
            screen.fill(BLACK)
            go_text = font.render("Go!", True, WHITE)
            go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(go_text, go_rect)
            pygame.display.flip()
            #shows 'Go!' for one second
            pygame.time.delay(1000)
        #updates every second
        else:
            pygame.time.delay(1000)


if __name__ == '__main__':
    pygame.init()
    #set screen dimensions and create screen
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 74)
    countdown_time = 3
    #create and start race
    display_countdown(screen, font, countdown_time, SCREEN_WIDTH, SCREEN_HEIGHT)
    race = Race(screen, SCREEN_HEIGHT, 3, 0)
    race.begin_race()
    #run main game loop
    race.run_game()


