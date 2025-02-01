import random
from math import sqrt, cos, radians, sin
from random import randint
import sys
import pygame
from time import sleep as do_sleep


class Point:
    #initialise x and y coordinates
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x},{self.y})"
    
    def distance_to(self, another: 'Point') -> float:
        #returns the distance between two points using pythagoras theorem
        sum_of_squares = (self.x - another.x) ** 2 + (self.y - another.y) ** 2
        return sqrt(sum_of_squares)

class LineSegment:
    def __init__(self, from_point: 'Point', to_point: 'Point'):
        #initialise the start and end points of the line segment
        self.from_point = from_point
        self.to_point = to_point

    def __str__(self):
        return f"{str(self.from_point)} --> {str(self.to_point)}"
    
    def orientation(self, p:Point) -> int:
        #determinant of the line segment and the point
        orientation_dir = (self.to_point.y - self.from_point.y) * (p.x - self.to_point.x) - (self.to_point.x - self.from_point.x) * (p.y - self.to_point.y)
        #collinear (zero orientation)
        if orientation_dir == 0:
            return 0
        #clockwise orientation
        elif orientation_dir > 0:
            return 1
        #counter-clockwise orientation
        else:
            return 2

    def on_segment(self, p:Point) -> bool:
        #check if the point lies on the line segment
        return (max(self.from_point.x, self.to_point.x) >= p.x >= min(self.from_point.x, self.to_point.x) and
                max(self.from_point.y, self.to_point.y) >= p.y >= min(self.from_point.y, self.to_point.y))

    def intersects(self, another: 'LineSegment') -> bool:
        #orientations of the line segments
        o1 = self.orientation(another.from_point)
        o2 = self.orientation(another.to_point)
        o3 = another.orientation(self.from_point)
        o4 = another.orientation(self.to_point)
        #check general case
        if o1 != o2 and o3 != o4:
            #line segments intersect
            return True
        #check if they are colinear
        if o1 == 0 and self.on_segment(another.from_point):
            return True
        
        if o2 == 0 and self.on_segment(another.to_point):
            return True
        
        if o3 == 0 and another.on_segment(self.from_point):
            return True 

        if o4 == 0 and another.on_segment(self.to_point):    
            return True

#Data structures
class Vector:
    def __init__(self, x_displacement, y_displacement):
        #initialise x and y displacements
        self.displacement = (x_displacement, y_displacement)
    
    def add(self, another: 'Vector') -> 'Vector':
        #returns the sum of two vectors
        return Vector(self.displacement[0] + another.displacement[0], self.displacement[1] + another.displacement[1])
    
    def subtract(self, another: 'Vector') -> 'Vector':
        #returns the difference between two vectors
        return Vector(self.displacement[0] - another.displacement[0], self.displacement[1] - another.displacement[1])
    
    def cross_product(self, another: 'Vector') -> 'Vector':
        #returns the cross product of two vectors
        return self.displacement[0] * another.displacement[1] - self.displacement[1] * another.displacement[0]

class Position_Vector(Vector):
    def __init__(self, x_displacement, y_displacement, origin_x, origin_y):
        #calls the constructor of the superclass Vector
        super(Position_Vector, self).__init__(x_displacement, y_displacement)
        #initialise the origin
        self.origin = Point(origin_x, origin_y)

class Track:
    def __init__(self, name, number_of_straights, start_x, start_y):
        #initialise the track
        self.__line_segments = []
        self.__name = name
        self.__num_straights = 0
        self.__circuit_completed = False
        self.__num_straights = number_of_straights
        self.__top_left = Point(0, 0)
        self.__bottom_right = Point(100,100)
        self.__start_finish_point = Point(start_x, start_y)

    def add_line_segment(self, line_segment: 'LineSegment'):
        if self.__circuit_completed:
            #circuit is already completed and the line segment cannot be added
            return False
        #add the line segment to the track and increment the number of straights
        self.__line_segments.append(line_segment)
        self.__num_straights += 1
        return True #if the line segment was added successfully
    
    def add_final_straight(self):
        #cannot complete an already completed circuit and must have at least 2 straights
        if not self.__circuit_completed and self.__num_straights >= 2:
            last_straight_added = self.__line_segments[-1] #type: LineSegment
            #create a line segment from the last point to the start point
            finishing_straight = LineSegment(last_straight_added.to_point, self.__start_finish_point)
            #add the finishing straight to the track
            self.add_line_segment(finishing_straight)
            #circuit is now completed
            return True
        else:
            #cannot add the finishing straight
            return False
    
    def get_all_line_segments(self):
        return self.__line_segments
    
    def clear_track(self):
        self.__line_segments = []
    
    def generate_random_point(self, line_segment: 'LineSegment'):
        valid_pt = False
        #new point is initialised
        newPt = None
        while not valid_pt:
            #new point is generated         
            newPt = Point(randint(0,100), randint(0,100))
            #checks if the point has a positive orientation
            valid_pt = line_segment.orientation(newPt) == 1
            if valid_pt:
                return newPt

    def contains_intersections(self, line_segment: 'LineSegment')->bool:
        for ls in self.__line_segments: #type: LineSegment
            if ls.intersects(line_segment):
                print(f"{line_segment} intersects {ls}")
                return True
        return False

    from math import cos, sin, radians

    def generate_track(self):
        #clear the track
        self.clear_track()
        #starting point is defined, which will be the same as the finish point
        current_point = self.__start_finish_point
        previous_angle = 0  #Start with an initial angle

        for _ in range(self.__num_straights - 1):  #Reserve one for the final straight
            valid_new_point = False
            new_point = None
            angle = None

            while not valid_new_point:
                #Pick a random length between 5 and 20
                length = random.randint(5, 20)

                #Determine a random clockwise angle step between 0 and 90 degrees
                angle_change = random.randint(1, 90)
                angle = (previous_angle - angle_change) % 360  #Ensure the angle remains within a full circle

                #Calculate new point using polar coordinates
                new_x = int(current_point.x + length * cos(radians(angle)))
                new_y = int(current_point.y + length * sin(radians(angle)))

                #Ensure the new point is within bounds
                new_x = max(self.__top_left.x, min(new_x, self.__bottom_right.x))
                new_y = max(self.__top_left.y, min(new_y, self.__bottom_right.y))

                new_point = Point(new_x, new_y)

                #Create a temporary line segment
                new_line_segment = LineSegment(current_point, new_point)

                self.add_line_segment(new_line_segment)
                valid_new_point = True  #Exit the loop when a valid segment is added
            
                #Check if this new segment intersects with any existing segment
                #TODO: if self.contains_intersections(new_line_segment):
                self.add_line_segment(new_line_segment)
                valid_new_point = True  #Exit the loop when a valid segment is added
            
            #Update for next iteration
            current_point = new_point
            previous_angle = angle

        #Add the final straight to the start-finish point
        self.add_final_straight()

    def get_topLeft(self):
        return self.__top_left

    def get_bottomRight(self):
        return self.__bottom_right

    def draw_on_pygame(self, screen, scale_factor):
        """
        Draws self onto the screen scaled by the given scale_factor
        :param screen:  pygame screen
        :param scale_factor: amount to scale (e.g. 5 will be mapping to the screen (0,0) to (500,500)
        """
        for ls in self.__line_segments:
            #scaling the coordinates
            screen_start = (ls.from_point.x * scale_factor, ls.from_point.y * scale_factor)
            screen_end = (ls.to_point.x * scale_factor, ls.to_point.y * scale_factor)
            pygame.draw.line(screen, (255, 0, 0), screen_start, screen_end, 2)
            #text colour and font
            text_colour = (0,0,0)
            font = pygame.font.Font(None, 20)
            #the coordinates are displayed 
            text_surface = font.render(f"{str(ls.to_point.x)}, {str(ls.to_point.y)})", True, text_colour)
            screen.blit(text_surface, screen_start)

    def __str__(self):
        returnStr = f"Track Name: {self.__name}\n"
        for ls in self.__line_segments:
            returnStr = returnStr + f"Line segment {str(ls)}\n"
        return returnStr

if __name__ == "__main__":

    # ls1 = LineSegment(Point(0,0),Point(10,10))
    # print(ls1.on_segment(Point(0,0)))
    # input("kajsdfasdf")
    #
    #
    # ls2 = LineSegment(Point(10,10),Point(20,20))
    # intersects = ls1.intersects(ls2)
    # print(str(ls1),"does","not" if not intersects else "", "intersect",str(ls2))
    # input("Press Enter")

    pygame.init()

    #track is defined
    test_track = Track('Silverstone', 10, 0, 0)
    scale_factor = 10  # how much to scale the grid of points making line segments
    #track is generated
    test_track.generate_track()
    #width and height are defined using the boundaries 
    w, h = test_track.get_bottomRight().x  - test_track.get_topLeft().x, test_track.get_bottomRight().y - test_track.get_topLeft().y
    w, h = w * scale_factor, h * scale_factor  # scale to pygame
    #screen size is set
    screen = pygame.display.set_mode((w, h), flags=pygame.FULLSCREEN)
    print(test_track)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #screen is filled white
        screen.fill((255,255,255))
        #track is drawn
        test_track.draw_on_pygame(screen, scale_factor)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

