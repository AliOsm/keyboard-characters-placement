import os
import copy
import cv2 as cv
import numpy as np

from helpers import *
from classes.button import Button
from classes.hand import Hand

class KeyboardStructure:
    def __init__(self, name, width, height, buttons, hands):
        self.name = name
        self.width = width
        self.height = height

        self.buttons = list()
        for button in buttons:
            self.buttons.append(Button(
                id=button['id'],
                location=button['location'],
                size=button['size']
            ))

        self.buttons = list(sorted(self.buttons, key=lambda button: button.id))

        self._check_buttons_overlapping()

        self.hands = list()
        for hand in hands:
            self.hands.append(Hand(fingers=hand['fingers']))

    def smallest_distance_from_button_to_finger(self, button_id):
        minimum_distance_value = 1e9
        minimum_distance_index = (-1, -1)

        for i, hand in enumerate(self.hands):
            for j, finger in enumerate(hand.fingers):
                temp_minimum_distance = finger.actual_location.euclidean_distance(self.buttons[button_id].location)
                if minimum_distance_value > temp_minimum_distance:
                    minimum_distance_value = temp_minimum_distance
                    minimum_distance_index = (i, j)

        if not self.hands[minimum_distance_index[0]].fingers[minimum_distance_index[1]].is_return:
            self.hands[minimum_distance_index[0]].fingers[minimum_distance_index[1]].actual_location = copy.deepcopy(self.buttons[button_id].location)

        return minimum_distance_value

    def reset_fingers_locations(self):
        for hand in self.hands:
            for finger in hand.fingers:
                finger.reset_location()

    def visualize(
        self,
        dirpath,
        characters_placement=None,
        show_hands=True,
        save=False
    ):
        if characters_placement is None:
            characters_placement = [''] * len(self.buttons)

        img = np.zeros((cm2px(self.height), cm2px(self.width), 3), np.uint8)

        for button, character in zip(self.buttons, characters_placement):
            cv.rectangle(
                img=img,
                pt1=cm2px((button.top_left.x, button.top_left.y)),
                pt2=cm2px((button.bottom_right.x, button.bottom_right.y)),
                color=(255, 255, 255),
                thickness=2
            )

            cv.putText(
                img=img,
                text=character,
                org=cm2px((button.text_origin.x, button.text_origin.y)),
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(255, 255, 255),
                thickness=2
            )

        if show_hands:
            for hand in self.hands:
                hand_color = random_color()
                for finger in hand.fingers:
                    cv.circle(
                        img=img,
                        center=cm2px((finger.location.x, finger.location.y)),
                        radius=cm2px(0.5),
                        color=hand_color,
                        thickness=3
                    )

        cv.imshow(self.name, img)
        cv.waitKey(0)

        if save:
            print(self.name)
            cv.imwrite(os.path.join(dirpath, self.name + '.png'), img)

    def _check_buttons_overlapping(self):
        for i in range(len(self.buttons)):
            for j in range(i, len(self.buttons)):
                if i == j: continue
                if self.buttons[i].is_overlapping(self.buttons[j]):
                    warning_log('buttons %s and %s are overlapped' % (i + 1, j + 1))

    def __str__(self):
        text = '%s Configurations\n' % self.name
        text += '- Width: %scm\n' % self.width
        text += '- Height: %scm\n' % self.height
        text += '- Number of Buttons: %s\n' % len(self.buttons)
        text += '- Number of Hands: %s' % len(self.hands)
        return text
