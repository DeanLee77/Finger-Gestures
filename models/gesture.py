
class Gesture:
    """ This is a basic class for modelling a single gesture. A gesture may consist of both left and right hands data or
    only of right or left-hand data. Also a gesture consists of multiple frames
    (i.e., a collection of Frame class objects).
    The length of this collection could be different for each gesture.

    at the time of instantiation, it only takes a gesture name for its constructor
    """

    # set class(static) private constant variables to implement encapsulation concept.
    # These variables represent right_hand and left_hand side gesture respectively
    # these variables will be used to get each hand side frames.
    # don't need to use literal string values by having them as class(static) values
    __RIGHT_HAND = 'R'
    __LEFT_HAND = 'L'
    __BOTH_HAND = 'B'

    # class(static) method to retrieve a private constant variable of '__RIGHT_HAND'
    @classmethod
    def right_hand(cls):
        return cls.__RIGHT_HAND

    # class(static) method to retrieve a private constant variable of '__LEFT_HAND'
    @classmethod
    def left_hand(cls):
        return cls.__LEFT_HAND

    # class(static) method to retrieve a private constant variable of '__BOTH_HAND'
    @classmethod
    def both_hand(cls):
        return cls.__BOTH_HAND

    def __init__(self, gesture_name):
        # gesture_name should be the same as the file name. For example Right_Hand_Gesture_7.csv data file represents
        # gesture_name 'Gesture 7'.
        self.gesture_name = gesture_name
        self.__frame_number = 0

        # A gesture could involve either only one hand or both hands at the same time
        # Hence, dictionary would be a better option than just list due to the fact that
        # dictionary could store each hand frames separately with hands name as a key
        # then retrieval of each hand side frame from a dictionary would be much faster than
        # finding each hand side frame by iterating a list of frames
        self.__frames = dict() # private variable

    def set_frames_data(self, frame):
        """ Add the given frame into frames dictionary

        Parameters:
            frame(Frame) : a Frame object

        Returns:
            void

        it takes a frame data and adding it to '__frames' dictionary.
        if the dictionary is empty, then the dictionary is populated with an empty list(array)
        for each hand side keys, and add a frame to '__frames' dictionary for an appropriate hand side
        """
        if len(self.__frames) == 0: # '__frames' dictionary has no items in it yet
            initial_dict = {self.right_hand(): [], self.left_hand(): []} # initialise dictionary for each hands
            self.__frames.update(initial_dict)

        if frame.hand_type == self.right_hand():
            self.__frames[self.right_hand()].append(frame)
        elif frame.hand_type == self.left_hand():
            self.__frames[self.left_hand()].append(frame)

    # getter for entire frames in the gesture
    def get_frames_data_in_dict(self) -> dict:
        return self.__frames

    # getter for entire list of frames in the gesture
    # an element at index zero is for a left hand, and the on at index one is for a right hand
    def get_frames_data_in_list(self) -> list:
        return list(self.__frames.values())

    # getter for right-hand side frames in dict type
    def get_right_hand_frame_data_in_dict(self) -> dict:
        return {self.right_hand(): self.get_frames_data_in_dict()[self.right_hand()]}

    # getter for right-hand side frames only
    def get_right_hand_frame_data(self) -> list:
        return list(self.get_frames_data_in_dict()[self.right_hand()])

    # setter for right-hand side frames only
    def set_right_hand_frame_data(self, right_hand_frame_data: list):
        self.__frames[self.right_hand()] += right_hand_frame_data

    # getter for left-hand side frames in dict type
    def get_left_hand_frame_data_in_dict(self) -> dict:
        return {self.left_hand(): self.get_frames_data_in_dict()[self.left_hand()]}

    # getter for left-hand side frames only
    def get_left_hand_frame_data(self) -> list:
        return list(self.get_frames_data_in_dict()[self.left_hand()])

    # setter for left-hand side frames only
    def set_left_hand_frame_data(self, left_hand_frame_data: list):
        self.__frames[self.left_hand()] += left_hand_frame_data

    def add_more_hands(self, gesture):
        """ Adding more frames data for another hand side
        Parameters:
            gesture(Gesture) : input Gesture object

        Returns:
            void

        adding more hands gesture. this method does not have a mechanism to check
        if this gesture has already hand gesture on right or left hand side, hence it requires more caution
        when call this method
        """
        if len(list(gesture.get_right_hand_frame_data())) != 0:
            self.set_right_hand_frame_data(gesture.get_right_hand_frame_data())
        if len(list(gesture.get_left_hand_frame_data())) != 0:
            self.set_left_hand_frame_data(gesture.get_left_hand_frame_data())

    # getter for '__frame_number'
    def get_frame_number(self):
        if self.__frame_number == 0:
            self.set_frame_number()
        return self.__frame_number

    # setter for '__frame_number'
    def set_frame_number(self):
        """ Setting frame numbers

        Parameters:

        Returns:
            void

        even this method is a setter for '__frame_number', it does not take any parameter to set '__frame_number'
        because the object will not know the total frame number until the main method finished with reading
        Dataset. Hence, this method will be call when a getter for '__frame_number' is called
        """

        for frames in self.get_frames_data_in_list():
            if len(frames) != 0:
                self.__frame_number = len(frames)
