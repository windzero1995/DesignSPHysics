#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Base Motion object for movements to inherit """

from mod.enums import MotionType

class BaseMotion():
    """ Base motion class to inherit by others.

        Attributes:
            duration: Movement duration in seconds
        """

    def __init__(self, duration=1, parent_movement=None):
        self.duration = duration
        self.type = MotionType.BASE
        self.parent_movement = parent_movement

    def __str__(self):
        return "BaseMotion [Duration: {}]".format(self.duration)
