from Back_end import Track, LineSegment

class Track_controller:
    def __init__(self):
        #initialise the track in the track controller
        self.__model = Track()
    
    def add_straight(self, straight: 'LineSegment'):
        #checks if it is possible to add a straight to the track
        return self.__model.add_line_segment(straight)
    
    def get_all_line_segments(self):
        #gets all the line segments of the track
        return self.__model.get_all_line_segments()
    
    def add_finishing_straight(self):
        #adds the finishing straight to the track
        return self.__model.add_final_straight()
    
