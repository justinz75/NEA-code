import random
from math import sqrt, cos, radians, sin, atan2
from random import randint

from CONSTANTS import *

distance = randint(1, 5)



class Point:
    #initialise x and y coordinates
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other: 'Point'):
        return self.x == int(other.x) and self.y == int(other.y)

    def distance_to(self, another: 'Point') -> float:
        #returns the distance between two points using pythagoras theorem
        sum_of_squares = (self.x - another.x) ** 2 + (self.y - another.y) ** 2
        return sqrt(sum_of_squares)

#Data structures
class Vector:
    def __init__(self, from_point: 'Point', to_point: 'Point'):
        #initialise x and y displacements
        self.from_point = from_point
        self.to_point = to_point
        self.dx = self.to_point.x - self.from_point.x
        self.dy = self.to_point.y - self.from_point.y

    def add(self):
        #returns the sum of two vectors
        return Vector(self.self.from_point.x + self.to_point.x, self.from_point.y + self.to_point.y)

    def subtract(self):
        #returns the difference between two vectors
        return Vector(self.self.from_point.x - self.to_point.x, self.from_point.y - self.to_point.y)

    def dot_product(self, another: 'Vector'):
        #returns the dot product of two vectors
        return self.dx * another.dx + self.dy * another.dy

    def sum_squares(self):
        return self.dx ** 2 + self.dy ** 2

    def get_length(self):
        return sqrt(self.sum_squares())

    def cross_product(self, another: 'Vector'):
        #returns the cross product of two vectors
        return self.dx * another.dy - self.dy * another.dx

class Position_Vector(Vector):
    def __init__(self, x_displacement, y_displacement, origin_x, origin_y):
        #calls the constructor of the superclass Vector
        super(Position_Vector, self).__init__(x_displacement, y_displacement)
        #initialise the origin
        self.origin = Point(origin_x, origin_y)
class LineSegment:
    def __init__(self, from_point: 'Point', to_point: 'Point'):
        #initialise the start and end points of the line segment
        self.from_point = from_point
        self.to_point = to_point
        self.__get_mid_point()
        self.__control_point(distance)
        self.bezier_points = self.calculate_by_bezier()
        self.segment_vector = Vector(self.from_point, self.to_point)

    def __str__(self):
        return f"{str(self.from_point)} --> {str(self.to_point)}"

    def distance_to(self, p: 'Point'):
        Ap_Vector = Vector(self.from_point, p)
        Ap_dot_prod = Ap_Vector.dot_product(self.segment_vector)
        t = Ap_dot_prod // self.segment_vector.sum_squares()
        t = max(0, min(1, t))
        closest_x = self.from_point.x + t * (self.to_point.x - self.from_point.x)
        closest_y = self.from_point.y + t * (self.to_point.y - self.from_point.y)
        distance_x = closest_x - p.x
        distance_y = closest_y - p.y
        return sqrt(distance_x ** 2 + distance_y ** 2)

    def get_transform(self, screen_height):
        start_point = self.from_point.get_transform(screen_height)
        end_point = self.to_point.get_transform(screen_height)
        return (start_point, end_point)

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
        if o1 == 0 and self.on_segment(another.from_point) and another.from_point != self.to_point and another.from_point != self.from_point:
            return True
        if o2 == 0 and self.on_segment(another.to_point) and another.to_point != self.to_point and another.to_point != self.from_point:
            return True
        if o3 == 0 and another.on_segment(self.from_point) and self.from_point != another.to_point and self.from_point != another.from_point:
            return True
        if o4 == 0 and another.on_segment(self.to_point) and self.to_point != another.to_point and self.to_point != another.from_point:
            return True
        return False

    def direction(self):
        return Vector(self.from_point, self.to_point)
    
    def get_intersection_point(self, another: 'LineSegment'):
        dir_1 = self.direction()
        dir_2 = another.direction()
        cross_prod = dir_1.cross_product(dir_2)
        if cross_prod == 0:
            return None
        line_segment = Vector(self.from_point, another.from_point)
        t1 = line_segment.cross_product(dir_2) / cross_prod
        x_intersect = self.from_point.x + t1 * dir_1.dx
        y_intersect = self.from_point.y + t1 * dir_1.dy
        return Point(x_intersect, y_intersect)
    
    def __get_mid_point(self):
        #this returns the mid-point of the line segment
        mid_point_x = (self.from_point.x + self.to_point.x) // 2
        mid_point_y = (self.from_point.y + self.to_point.y) // 2
        self.mid_point = Point(mid_point_x, mid_point_y)
    
    def calculate_mid_point(self, p: 'Point', q: 'Point'):
        #this returns the mid-point of the line segment
        mid_point_x = (p.x + q.x) // 2
        mid_point_y = (p.y + q.y) // 2
        return Point(mid_point_x, mid_point_y)

    def calculate_by_bezier(self):
        mid_point = self.mid_point
        bezier_points = []
        #these find the quarter points
        self.temp_line_segment_mid_point = self.calculate_mid_point(self.from_point, mid_point)
        self.temp_line_segment_mid_point_2 = self.calculate_mid_point(mid_point, self.to_point)
        for i in range(MAX_SIZE + 1):
            t = i / MAX_SIZE
            #Bezier points are calculated and appended to the list of Bezier points
            new_Bezier_point = self.Bezier_point(t, self.control_points[0], self.control_points[1], self.control_points[2])
            bezier_points.append(new_Bezier_point)
        return bezier_points
    
    def calculate_control_points(self, distance, start_point: 'Point', end_point: 'Point'):
        mid_point = self.mid_point
        angle = atan2(end_point.y - start_point.y, end_point.x - start_point.x)
        control_point_1 = Point(mid_point.x - distance * sin(angle), mid_point.y + distance * cos(angle))
        control_point_2 = Point(mid_point.x + distance * sin(angle), mid_point.y - distance * cos(angle))
        return control_point_1, control_point_2

    def __control_point(self, distance):
        #this creates the midpoint and the control point list
        mid_point = self.mid_point
        control_points_list = []
        #control points are calculated
        self.temp_line_segment_mid_point = self.calculate_mid_point(self.from_point, mid_point)
        self.temp_line_segment_mid_point_2 = self.calculate_mid_point(mid_point, self.to_point)
        control_point_1, control_point_2 = self.calculate_control_points(distance, self.from_point, self.temp_line_segment_mid_point)
        #control points are added to the list
        control_points_list.append(control_point_1)
        control_points_list.append(mid_point)
        control_points_list.append(control_point_2)
        self.control_points = control_points_list
    
    def Bezier_point(self, t, q_1_point, middle_point, q_3_point):
        """
        Bezier point is (1-t)^4 * from_point + 4 * (1-t)^3 * t * q_1_point + 4 * t^3 * t * q_1_point + 6 * (1-t)^2 * t^2 * middle_point + 4 * (1-t) * t^3 * q_3_point + t^4 * to_point
        """
        x = (1 - t) ** 4 * self.from_point.x + 4 * (1 - t) ** 3 * t * q_1_point.x + 6 * (1 - t) ** 2 * t ** 2 * middle_point.x + 4 * (1 - t) * t ** 3 * q_3_point.x + t ** 4 * self.to_point.x
        y = (1 - t) ** 4 * self.from_point.y + 4 * (1 - t) ** 3 * t * q_1_point.y + 6 * (1 - t) ** 2 * t ** 2 * middle_point.y + 4 * (1 - t) * t ** 3 * q_3_point.y + t ** 4 * self.to_point.y
        return Point(x, y)

    def bezier_bridge_curve(self, t, p0, p1, p2):
        """
        Bezier point is (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2
        """
        x = (1 - t)**2 * p0.x + 2 * (1 - t) * t * p1.x + t**2 * p2.x
        y = (1 - t)**2 * p0.y + 2 * (1 - t) * t * p1.y + t**2 * p2.y
        return Point(x, y)

    def create_bezier_bridge(self, intersection_point: 'Point', another_line_segment: 'LineSegment', bridge_scaling_factor = 1.5, number_of_points = 100):
         # Find quarter points for smooth transition
        start_point = self.calculate_mid_point(self.from_point, intersection_point)
        end_point = self.calculate_mid_point(intersection_point, another_line_segment.to_point)

        # **Dynamic Control Point Calculation**
        # Distance between intersection and start/end determines bridge height
        dx = end_point.x - start_point.x
        dy = end_point.y - start_point.y
        intersection_size = sqrt(dx**2 + dy**2)  # Hypotenuse (Pythagorean theorem)

        # Adjust bridge height based on intersection size
        bridge_height = intersection_size * bridge_scaling_factor

        # Position the control point **above the intersection point**, perpendicular to the direction of the track
        angle = atan2(dy, dx)  # Angle of the segment
        control_point_x = intersection_point.x - bridge_height * sin(angle)  # Perpendicular shift
        control_point_y = intersection_point.y + bridge_height * cos(angle)

        control_point = Point(int(control_point_x), int(control_point_y))

        # Generate Bézier curve points
        bezier_points = []
        for i in range(number_of_points + 1):
            t = i / number_of_points
            bridge_point = self.bezier_bridge_curve(t, start_point, control_point, end_point)
            bezier_points.append(bridge_point)

        return bezier_points


class Track:
    def __init__(self, name, number_of_straights, start_x, start_y):
        #initialise the track
        self._line_segments = []
        self.name = name
        self._num_straights = 0
        self._circuit_completed = False
        self._number_straights = number_of_straights
        self._start_finish_point = Point(start_x, start_y)

    def get_num_straights(self):
        return self._number_straights

    def get_start_finish_point(self):
        return self._start_finish_point
    
    def add_line_segments(self, line_segments):
        for line_segment in line_segments:
            self.add_line_segment(line_segment)

    def add_line_segment(self, line_segment: 'LineSegment'):
        if self._circuit_completed:
            #circuit is already completed and the line segment cannot be added
            return False
        #add the line segment to the track and increment the number of straights
        self._line_segments.append(line_segment)
        self._num_straights += 1
        return True #if the line segment was added successfully

    # def find_all_final_intersections(self, line_segment: 'LineSegment'):
    #     intersection_data = {}
    #     for ls in self.get_all_line_segments():
    #         if ls.intersects(line_segment):
    #             #finds the intersection points
    #             intersection_point = ls.get_intersection_point(line_segment)
    #             intersection_data[intersection_point] = (ls, line_segment)
    #     #removes the to and from points that would have otherwise counted as intersections
    #     true_intersections = {k: v for i, (k, v) in enumerate(intersection_data.items()) if 0 < i < len(intersection_data) - 1}
    #     return true_intersections
    
    def add_final_straight(self):
        #adds a final segment but creates bridges if required
        #cannot complete an already completed circuit and must have at least 2 straights
        if not self._circuit_completed and self._num_straights >= 2:
            last_straight_added = self._line_segments[-1] #type: LineSegment
            #create a line segment from the last point to the start point
            finishing_straight = LineSegment(last_straight_added.to_point, self._start_finish_point)
            #check for intersections
            # intersection_data = self.find_all_final_intersections(finishing_straight)
            # if intersection_data:
            #     bezier_bridges = []
            #     for intersection_point, (line_segment_1, line_segment_2) in intersection_data.items():
            #         bezier_bridge_points = line_segment_1.create_bezier_bridge(intersection_point, line_segment_2)
            #         bezier_bridges.append(bezier_bridge_points)
            #     self.add_line_segment(finishing_straight)
            #     self._circuit_completed = True
            #     return bezier_bridges
            #add the finishing straight to the track
            self.add_line_segment(finishing_straight)
            #circuit is now completed
            self._circuit_completed = True

    def get_all_line_segments(self):
        return self._line_segments

    def clear_track(self):
        self._line_segments = []

    def generate_random_point(self, line_segment: 'LineSegment'):
        valid_pt = False
        #new point is initialised
        newPt = None
        while not valid_pt:
            #new point is generated
            newPt = Point(randint(0, MAX_SIZE), randint(0, MAX_SIZE))
            #checks if the point has a positive orientation
            valid_pt = line_segment.orientation(newPt) == 1
            if valid_pt:
                return newPt

    def contains_intersections(self, line_segment: 'LineSegment') -> bool:
        #checks each line segment for intersections except the last line segment added
        for i in range(len(self._line_segments)-1):
            #do not check if line_segment intersects
            if not self._line_segments[i] == line_segment:
                if self._line_segments[i].intersects(line_segment):
                    print(f"{line_segment} intersects {self._line_segments[i]}")
                    #returns true if line segment does intersect
                    return True
        #returns false if line segment does not intersect
        return False

    def is_valid_next_segment(temp_track, current_point, previous_angle):
        #ensure the track doesn't hit a dead end
        test_point = current_point
        for _ in range(6): #look ahead 6 steps
            #randomly choose a length and angle
            length = random.randint(MIN_STRAIGHT_LENGTH, MAX_STRAIGHT_LENGTH)
            angle_change = random.randint(-120, 120) 
            angle = (previous_angle + angle_change) % 360

            #x and y coordinates are calculated
            new_x = int(test_point.x + length * cos(radians(angle)))
            new_y = int(test_point.y + length * sin(radians(angle)))

            new_x = max(TOP_LEFT[0], min(new_x, BOTTOM_RIGHT[0]))
            new_y = max(TOP_LEFT[1], min(new_y, BOTTOM_RIGHT[1]))

            new_test_point = Point(new_x, new_y)
            new_test_segment = LineSegment(test_point, new_test_point)

            #if this segment intersects or goes out of bounds, return False
            if temp_track.contains_intersections(new_test_segment):
                return False
            test_point = new_test_point #moves forward in the test
        return True
    
    @staticmethod
    def generate_track(name, number_of_straights, start_x, start_y):
        temp_track = Track(name, number_of_straights, start_x, start_y)
        #clear the track
        temp_track.clear_track()
        #starting point is defined, which will be the same as the finish point
        current_point = temp_track._start_finish_point
        previous_angle = 0  #Start with an initial angle

        for _ in range(temp_track._number_straights - 1):  #Reserve one for the final straight
            valid_new_point = False
            new_point = None
            angle = None

            while not valid_new_point:
                #Pick a random length between 5 and 20
                length = random.randint(MIN_STRAIGHT_LENGTH, MAX_STRAIGHT_LENGTH)

                #Determine a random clockwise angle step between 0 and 90 degrees
                angle_change = random.randint(-120, 120)
                angle = (previous_angle + angle_change) % 360  #Ensure the angle remains within a full circle

                #Calculate new point using polar coordinates
                new_x = int(current_point.x + length * cos(radians(angle)))
                new_y = int(current_point.y + length * sin(radians(angle)))

                #Ensure the new point is within bounds
                new_x = max(TOP_LEFT[0], min(new_x, BOTTOM_RIGHT[0]))
                new_y = max(TOP_LEFT[1], min(new_y, BOTTOM_RIGHT[1]))

                new_point = Point(new_x, new_y)

                #Create a temporary line segment
                new_line_segment = LineSegment(current_point, new_point)

                #Check if this new segment intersects with any existing segment
                if not temp_track.contains_intersections(new_line_segment) and temp_track.is_valid_next_segment(new_point, angle):
                    temp_track.add_line_segment(new_line_segment)
                    valid_new_point = True  #Exit the loop when a valid segment is added

            #Update for next iteration
            current_point = new_point
            previous_angle = angle

        #Add the final straight to the start-finish point
        temp_track.add_final_straight()
        return temp_track
    
    def get_track_points(self):
        points = []
        for ls in self._line_segments:
            points.append(ls.from_point)
        if self._line_segments:
            points.append(self._line_segments[-1].to_point)
        return points

    def get_closest_line_segment(self, p:'Point'):
        distances = [ls.distance_to(p) for ls in self.get_all_line_segments()]
        return min(distances)

#
# ls = LineSegment(Point(0,0), Point(100, 0))
# ls1 = LineSegment(Point(100,0), Point(100, 100))
# ls2 = LineSegment(Point(100, 100), Point(0, 100))
# test_track = Track('name', 4, 0, 0)
# ls4 = [ls, ls1, ls2]
# test_track.add_line_segments(ls4)
# test_track.add_final_straight()
# print(test_track.get_closest_line_segment(Point(100, 150)))

