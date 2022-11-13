from collections import namedtuple

ObjectAxesParams = namedtuple('ObjectPosition', ['axis_y', 'axis_x'])
ObjectSize = namedtuple('ObjectSize', ['height', 'width'])
ObjectBorders = namedtuple('ObjectBorders', ['top', 'bottom', 'left', 'right'])

Frame = namedtuple('Frame', ['lifetime', 'frame'])
FrameStage = namedtuple('FrameStage', ['lifetime', 'style'])
