class Frame:
    """ This is a basic class for modelling a single hand and single frame data in the given data file.
    A single frame is represented by 25 rows in the given data file. Each frame has data relevant to all five fingers

    At the time of its instantiation, it takes hand_type, frame_number and root_pos for its constructor"""

    # these variable are set as a private constant to encapsulate the access
    # to the variable keeping the control of the object status.
    # Not allowing external objects to change the status of the object.
    # these variables represent each finger name
    __THUMB_FINGER = 'THUMB'
    __INDEX_FINGER = 'INDEX'
    __MIDDLE_FINGER = 'MIDDLE'
    __RING_FINGER = 'RING'
    __PINKY_FINGER = 'PINKY'

    @classmethod
    def get_thumb_finger(cls):
        return cls.__THUMB_FINGER

    @classmethod
    def get_index_finger(cls):
        return cls.__INDEX_FINGER

    @classmethod
    def get_middle_finger(cls):
        return cls.__MIDDLE_FINGER

    @classmethod
    def get_ring_finger(cls):
        return cls.__RING_FINGER

    @classmethod
    def get_pinky_finger(cls):
        return cls.__PINKY_FINGER

    # for each private variables (leading with two underscores) has its own setters and getters
    def __init__(self, hand_type, frame_number, root_pos):
        self.hand_type = hand_type
        self.frame_number = frame_number
        self.wrist_position = root_pos  # This is ths RootPos value in each frame
        self.__thumb = dict()  # For example {Thumb0:(x,y,z), Thumb1:(x1,y1,z1), Thumb2:(x2,y2,z2), Thumb3:(x3,y3,z3)}
        self.__index_finger = dict()
        self.__middle_finger = dict()
        self.__ring_finger = dict()
        self.__pinky = dict()

    # setter for thumb_finger_data
    def set_thumb_data(self, thumb_data):
        self.__thumb = thumb_data

    # getter for thumb_finger_data
    def get_thumb_data(self) -> dict:
        return self.__thumb

    # setter for index_finger_data
    def set_index_finger_data(self, index_finger):
        self.__thumb = index_finger

    # getter for index_finger_data
    def get_index_finger_data(self) -> dict:
        return self.__index_finger

    # setter for middle_finger_data
    def set_middle_finger_data(self, middle_finger_data):
        self.__middle_finger = middle_finger_data

    # getter for middle_finger_data
    def get_middle_finger_data(self) -> dict:
        return self.__middle_finger

    # setter for ring_finger
    def set_ring_finger(self, ring_finger_data):
        self.__ring_finger = ring_finger_data

    # getter for ring_finger
    def get_ring_finger_data(self) -> dict:
        return self.__ring_finger

    # setter for pinky finger
    def set_pinky(self, pinky_data):
        self.__pinky = pinky_data

    # getter for pinky finger
    def get_pinky_data(self) -> dict:
        return self.__pinky
