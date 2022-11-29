import os
from typing import List, Union, TypeVar

from entities.common import ObjectSize
from utils.sleep import sleep

PathLike = TypeVar('PathLike', str, bytes, os.PathLike)


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """
    Draw multiline text fragment on canvas, erase text instead of drawing
     if negative=True is specified.
     """

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


async def update_frame(canvas, pos_y: int, pos_x: int, frame: str,
                       base_sleep_ticks: int = 2) -> None:
    """
    Draws and removes passed frame.
    :param canvas: current WindowObject
    :param pos_y: frame start position by y-axis
    :param pos_x: frame start position by x-axis
    :param frame: frame to draw
    :param base_sleep_ticks: awaiting delay
    """
    draw_frame(
        canvas, pos_y, pos_x, frame
    )
    await sleep(base_sleep_ticks)
    draw_frame(
        canvas, pos_y, pos_x, frame, negative=True
    )


def get_frame_size(text):
    """
    Calculate size of multiline text fragment, return pair
     — number of rows and columns.
     """
    lines = text.splitlines()
    rows = len(lines)
    columns = max((len(line) for line in lines))
    return ObjectSize(height=rows, width=columns)


def get_frames_from_files(
        frame_files: Union[List[PathLike], PathLike]) -> Union[List[str], str]:
    """
    Reads files with any frames and returns them as list of strings.
    :param frame_files: list of files to read
    :return: list of frames as string objects
    """
    if not isinstance(frame_files, list):
        frame_files = [frame_files]
    frames = []
    for frame_file in frame_files:
        with open(frame_file, 'r', encoding='utf-8') as fp:
            frames.append(fp.read())

    if len(frame_files) == 1:
        return frames[0]
    return frames
