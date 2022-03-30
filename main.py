import os, glob, sys, pathlib

from models.frame import Frame
from models.gesture import Gesture
from models.gestures import Gestures
from visualisation import Visualization


def set_finger_data(finger_type: str, finger_data: tuple, frame: Frame):
    """ Setting a finger data for the frame in accordance with finger type
    Parameters:
        finger_type(str),
        finger_data(tuple) ,
        frame(Frame)

    Returns:
        void

    adding a finger data to an argument of frame based on the argument value of finger type
    """
    if finger_type.find('Thumb') != -1:
        frame.get_thumb_data()[finger_type] = finger_data
    elif finger_type.find('Index') != -1:
        frame.get_index_finger_data()[finger_type] = finger_data
    elif finger_type.find('Middle') != -1:
        frame.get_middle_finger_data()[finger_type] = finger_data
    elif finger_type.find('Ring') != -1:
        frame.get_ring_finger_data()[finger_type] = finger_data
    elif finger_type.find('Pinky') != -1:
        frame.get_pinky_data()[finger_type] = finger_data


def is_root_pos(text_line: str):
    """ Checking if the given line is for RootPos or not
    Parameters:
        text_line(str) : a line string

    Returns:
        boolean : True or False

    takes a string line. if the line is about 'RootPos' return True, False otherwise
    """

    return text_line.find('RootPos') != -1


def adding_frame(hand_frame_list: list, finger_name_list: list) -> list:
    """ Adding frames for fingers in the given finger name list to an empty list
    Parameters:
        hand_frame_list(list) : list of frames data for a hand side e.g left_hand_side_frames_data,
        finger_name_list(list) : list of finger names to extract its frame data ,

    Returns:
        list : list of frames of tuples for an interest finger(s)

    generates a list of frames of tuples for an interest finger(s)
    each index of the list represents frame number.
    Note: index starts from zero hence actual frame number is index +1
    """

    return_list = []
    for frame in hand_frame_list:
        frame_list = []
        for finger in finger_name_list:
            if finger == Frame.get_thumb_finger():
                frame_list.append(frame.get_thumb_data())
            elif finger == Frame.get_index_finger():
                frame_list.append(frame.get_index_finger_data())
            elif finger == Frame.get_middle_finger():
                frame_list.append(frame.get_middle_finger_data())
            elif finger == Frame.get_ring_finger():
                frame_list.append(frame.get_ring_finger_data())
            elif finger == Frame.get_pinky_finger():
                frame_list.append(frame.get_pinky_data())
        return_list.append(frame_list)
    return return_list


def extract_finger_frame(gesture_name: str, hand_side: str, finger_name_list: list,
                         gestures: Gestures) -> dict:
    """ Extract a list of Fingers' Data in all the frames of a list of hands for a gesture name
    Parameters:
        gesture_name(str) : input gesture name e.g Gesture 4,
        hand_side(str) : hand side e.g 'R', 'L', or 'B',
        finger_name_list(list) : list of finger names to extract its frame data ,
        gestures(Gestures) : all gesture data

    Returns:
        dict : right hand index finger frame data list

    this function extracts a list of Fingers' Data in all the frames of a list of hands for a gesture name
    then adds the extracted list of fingers' data into a dictionary for its hand side
    it finally returns the dictionary
    """
    gesture = gestures.get_list_of_gesture()[gesture_name]
    # 'return_dict' represents each interest finger data in interest hand sides
    # each hand sides value represents interest finger data in each frames
    # each index of each hand side value represents each frame
    # it will looks like below
    # {'R': [[{Thumb0:(),Thumb1:(),..,Thumb3:()}, {Index1:(), .., Index3:()}], [{}], [{}]], 'L': [[],[],[]]}
    return_dict = dict()
    if hand_side == Gesture.left_hand():
        left_hand_frame_list = gesture.get_left_hand_frame_data()
        return_list = adding_frame(left_hand_frame_list, finger_name_list)
        return_dict.update({Gesture.left_hand(): return_list})
    elif hand_side == Gesture.right_hand():
        right_hand_frame_list = gesture.get_right_hand_frame_data()
        return_list = adding_frame(right_hand_frame_list, finger_name_list)
        return_dict.update({Gesture.right_hand(): return_list})
    elif hand_side == Gesture.both_hand():
        left_hand_frame_list = gesture.get_left_hand_frame_data()
        left_return_list = adding_frame(left_hand_frame_list, finger_name_list)
        return_dict.update({Gesture.left_hand(): left_return_list})

        right_hand_frame_list = gesture.get_right_hand_frame_data()
        right_return_list = adding_frame(right_hand_frame_list, finger_name_list)
        return_dict.update({Gesture.right_hand(): right_return_list})

    return return_dict


def read_gesture(file_name: str) -> Gesture:
    """ Read a text file for a gesture
    Parameters:
        file_name(str): file name string

    Returns:
        Gesture : an instance of Gesture object

    this function is to read a given file line by line and generates a frame instance in accordance with finger type
    then store the frame instance in the gesture instance
    """

    # 'pathlib.Path(file_name).stem' will remove extension from the file_name
    file_name_array = pathlib.Path(file_name).stem.split('_')
    gesture_name = file_name_array[2] + ' ' + file_name_array[3]
    gesture = Gesture(gesture_name)
    hand_type = Gesture.left_hand() if file_name_array[0] == 'Left' else Gesture.right_hand()

    import re
    # this pattern will be used extract hands coordinate data from each lines of the given file
    pattern = re.compile('(.*)(\s*,\s*)(\(.*\))')

    with open(file_name) as fopen:
        lines = fopen.readlines()
        frame_number = 0
        for line in lines:
            match = pattern.search(line)
            if match:  # line is in a format of '<finger_type>, (<coordinate data>)'
                finger_type = match.group(1).strip()
                # eval method will convert a string of '(<coordinate data>)' to a tuple
                finger_data = eval(match.group(3).strip())
                if is_root_pos(finger_type):  # the line is about 'RootPos'
                    frame_number += 1  # a new frame starts so increase the frame number
                    root_pos = finger_data
                    frame = Frame(hand_type, frame_number, root_pos)  # declare and initialise an instance of Frame
                    gesture.set_frames_data(frame)  # add the frame into a Gesture instance

                # skip the line if it starts with 'Hand_Start' or 'Hand_ForearmStub',
                # and the line is NOT about 'RootPos'
                elif finger_type.find('Hand_Start') != 0 and finger_type.find('Hand_ForearmStub') != 0:
                    set_finger_data(finger_type.split('_')[1], finger_data, frame)
    return gesture


def read_data_files():
    """
    This function should read all the hand gesture data files and map the data to your chosen model.
    """

    # Instead of listing all data file names, find out all data file names programmatically
    # find out current directory where this python source code sit
    dir_path = os.path.dirname(__file__)

    # pointing data set directory
    os.chdir(dir_path + '/data')

    gesture_list = Gestures()
    # selecting all files with '.txt' extension in the pointed data set directory, and iterate the list of files
    for file in glob.glob("*.txt"):
        try:
            gesture_list.add_gesture(read_gesture(file))
        except IOError as ioe:
            print(f'{ioe}: File not found or unreadable', file=sys.stderr)
            # sys.exit(1)
        except Exception as ie:
            print(f'{ie}: Data file is ill-formatted', file=sys.stderr)

    return gesture_list


if __name__ == "__main__":
    all_gestures_data = read_data_files()
    right_index_finger_frame_list = extract_finger_frame('Gesture 4', Gesture.right_hand(),
                                                         [Frame.get_index_finger()], all_gestures_data)
    left_ring_middle_finger_frame_list = extract_finger_frame('Gesture 5', Gesture.left_hand(),
                                                              [Frame.get_ring_finger(), Frame.get_middle_finger()],
                                                              all_gestures_data)
    both_thumb_index_finger_frame_list = extract_finger_frame('Gesture 3', Gesture.both_hand(),
                                                              [Frame.get_thumb_finger(), Frame.get_index_finger()],
                                                              all_gestures_data)
    Visualization.animate_hand_gesture('Gesture 1', all_gestures_data)
    Visualization.animate_hand_gesture('Gesture 2', all_gestures_data)
    Visualization.animate_hand_gesture('Gesture 5', all_gestures_data)
    Visualization.animate_hand_gesture('Gesture 3', all_gestures_data)
