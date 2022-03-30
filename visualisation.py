import matplotlib;

import matplotlib;

from models.gestures import Gestures

matplotlib.use("TkAgg")
import numpy as np
from matplotlib import pyplot as plt, animation

from models.frame import Frame


class Visualization:
    """ This is a class to run visualization.
    In the program, all methods used to visualise gestures static method,
    and therefore this class will NOT be instantiated for visualisation.
    """

    # this variable is set as a private constant to encapsulate the access
    # to the variable keeping the control for the object status.
    # Not allowing external objects to change the status of the object.
    __FINGER_LIST = [Frame.get_thumb_finger(), Frame.get_index_finger(), Frame.get_middle_finger(),
                     Frame.get_ring_finger(), Frame.get_pinky_finger()]

    @classmethod
    def __generate_finger_line_data(cls, first_frame: Frame, finger_name: str) -> np.stack:
        """
        Parameters:
            first_frame(Frame) : input gesture name e.g Gesture 4,
            finger_name(str) : hand side e.g 'R', 'L', or 'B',

        Returns:
            np.stack : A matrix(2 Dimensional array) representing (X, Y, Z) coordinates of finger landmarks

        this  is a generic method to extract finger data from the given frame
        and generate coordinates of landmark data for a finger. In addition the access for this method is private because
        this method is only used within the class, in other words this method will not be called outside of this class.
        """
        wrist_position = first_frame.wrist_position

        finger_data_value = list()
        # extract finger data value based on the given finger name
        if finger_name == Frame.get_thumb_finger():
            finger_data_value = first_frame.get_thumb_data().values()
        elif finger_name == Frame.get_index_finger():
            finger_data_value = first_frame.get_index_finger_data().values()
        elif finger_name == Frame.get_middle_finger():
            finger_data_value = first_frame.get_middle_finger_data().values()
        elif finger_name == Frame.get_ring_finger():
            finger_data_value = first_frame.get_ring_finger_data().values()
        elif finger_name == Frame.get_pinky_finger():
            finger_data_value = first_frame.get_pinky_data().values()

        # the reason for adding wrist_position to each coordinate is that the wrist is a root for all fingers
        temp_x = [float(wrist_position[0]) - float(x[0]) for x in finger_data_value]
        temp_x.insert(0, float(wrist_position[0]))
        finger_x = np.array(temp_x)
        temp_y = [float(wrist_position[1]) - float(x[1]) for x in finger_data_value]
        temp_y.insert(0, float(wrist_position[1]))
        finger_y = np.array(temp_y)
        temp_z = [float(wrist_position[2]) - float(x[2]) for x in finger_data_value]
        temp_z.insert(0, float(wrist_position[2]))
        finger_z = np.array(temp_z)
        return np.stack((finger_x, finger_y, finger_z))

    @classmethod
    def update(cls, frame_number, hand_finger, all_frames):
        """ This method updates each Line2Ds to generate animation of fingers
        Parameters:
            frame_number(int) : total number of frames of each fingers,
            hand_finger(dict) : a list of Line2D of each fingers for each hand side,
            all_frames(list) : a list of each hand side's frames in a gesture having all fingers coordinate data

        Returns:
            void

        this method is to update animation of finger(s) and hand movement
        """
        for each_side_frame_data in all_frames:
            # some gesture might or might not have two hands in it so it needs to check if it is for two hands or not
            if len(each_side_frame_data) > 0:
                # extracting a frame
                frame = each_side_frame_data[frame_number-1]
                hand = frame.hand_type
                for finger in cls.__FINGER_LIST:
                    finger_graph_data = cls.__generate_finger_line_data(frame, finger)
                    hand_finger[hand][finger].set_data(finger_graph_data[:2, :])  # (finger_x, finger_y)
                    hand_finger[hand][finger].set_3d_properties(finger_graph_data[2, :])  # (finger_z)

    @classmethod
    def animate_hand_gesture(cls, gesture_name: str, gesture_list: Gestures):
        """ This method is a main method to do gesture animation
        Parameters:
            gesture_name(str) : a gesture name to animate,
            gesture_list(list) : a list of gestures

        Returns:
            void

        this method is to animate a gesture for a given gesture name
        """
        # checking if a gesture name is actually in a given list of gestures
        if gesture_name in gesture_list.get_list_of_gesture().keys():
            a_gesture = gesture_list.get_gesture([gesture_name])[0]
            all_frames = a_gesture.get_frames_data_in_list()
            fig = plt.figure()
            fig.suptitle(gesture_name, fontsize=16)
            ax = plt.axes(projection='3d')
            frame_number = a_gesture.get_frame_number()

            # hand_finger is a dictionary to store a Line2D of each fingers for each hand side,
            hand_finger = dict()

            # all_frames has all frames data of each hand side
            for each_hand_side_frame_data in all_frames:
                # check if a gesture has a frame data for each hand sides
                if len(each_hand_side_frame_data) > 0:
                    first_frame = each_hand_side_frame_data[0]
                    hand_side = first_frame.hand_type
                    # finger_lines is a dictionary to store a Line2D of each fingers
                    finger_lines = dict()
                    # for each finger, draw an initial line, and store a Line2D data of each finger into finger_line dict
                    for finger in cls.__FINGER_LIST:
                        finger_graph_data = cls.__generate_finger_line_data(first_frame, finger)
                        line, = ax.plot(finger_graph_data[0, :], finger_graph_data[1, :], finger_graph_data[2, :],
                                        'o-', label=finger, lw=2)
                        finger_lines.update({finger: line})
                    hand_finger.update({hand_side: finger_lines})

            labels = []
            visibility = []
            # draw a box for interactive labels for each animated fingers
            rax = plt.axes([0.05, 0.4, 0.2, 0.45])
            # store current labels and visibility status of each fingers for each hand side
            for k, v in hand_finger.items():
                for k_1, line in v.items():
                    labels.append(k + "_" + str(line.get_label()))
                    visibility.append(line.get_visible())
            from matplotlib.widgets import CheckButtons

            # draw checkboxes of labels for each fingers
            check = CheckButtons(rax, labels, visibility)

            # this function is to make each finger Line2D visible or invisible
            def func(label_in):
                label_array = str(label_in).split('_')
                temp_line = hand_finger[label_array[0]][label_array[1]]
                temp_line.set_visible(not temp_line.get_visible())
                plt.draw()

            check.on_clicked(func)

            line_ani = animation.FuncAnimation(fig, cls.update, frame_number,
                                               fargs=(hand_finger, all_frames), interval=100, blit=False)

            # Setting the axes properties
            ax.set_xlabel('X')
            ax.set_xlim3d([0, 0.5])
            ax.set_ylabel('Y')
            ax.set_ylim3d([0.8, 1.3])
            ax.set_zlabel('Z')
            ax.set_zlim3d([0.2, 0.4])

            plt.ion
            plt.show()
