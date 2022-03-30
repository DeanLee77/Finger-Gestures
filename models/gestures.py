from models.gesture import Gesture


class Gestures:
    """ this Gestures object is to store all Gesture objects """

    # Gesture constructor
    def __init__(self):
        self.__list_of_gestures = dict()

    def get_gesture(self, list_of_gesture_name: list) -> list:
        """ Getting a list of gestures for a given list of gesture names

        Parameters:
            list_of_gesture_name(list) : list of Gesture names

        Returns:
            list of gesture objects(list) : list of Gesture objects

        get all gesture object for gesture names in the given list
        """
        return [value for (k, value) in self.__list_of_gestures.items() if k in list_of_gesture_name]

    # getter for '__list_of_gestures'
    def get_list_of_gesture(self):
        return self.__list_of_gestures

    def add_gesture(self, gesture: Gesture):
        """ Adding a gesture object to a list of gestures
        Parameters:
            gesture(Gesture) : input Gesture object

        Returns:
            void

        adding an object to '__list_of_gesture' dictionary. Even it is named as 'list' but it is actually a dictionary type.
        dictionary type has a O(1) to retrieve an element
        """
        if gesture.gesture_name not in self.__list_of_gestures.keys():
            self.__list_of_gestures.update({gesture.gesture_name: gesture})
        else:
            self.__list_of_gestures[gesture.gesture_name].add_more_hands(gesture)
