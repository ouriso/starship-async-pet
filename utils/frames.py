from typing import List

from entities.common import ObjectSize


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


def get_frame_size(text):
    """
    Calculate size of multiline text fragment, return pair
     — number of rows and columns.
     """
    lines = text.splitlines()
    rows = len(lines)
    columns = max((len(line) for line in lines))
    return ObjectSize(height=rows, width=columns)


def get_frames_list(frame_files: List[str]) -> List[str]:
    """
    Reads files with any frames and returns them as list of strings.
    :param frame_files: list of files to read
    :return: list of frames as string objects
    """
    frames = []
    for frame_file in frame_files:
        with open(frame_file, 'r', encoding='utf-8') as fp:
            frames.append(fp.read())

    return frames
