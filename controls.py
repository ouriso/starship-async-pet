from config import (
    ROWS_SPEED, COLUMNS_SPEED,
    UP_KEY_CODE, DOWN_KEY_CODE, RIGHT_KEY_CODE, LEFT_KEY_CODE, SPACE_KEY_CODE
)


def read_controls(canvas):
    """Read keys pressed and returns tuple with controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        # simultaneous reading of multiple key presses
        pressed_key_codes = [canvas.getch() for _ in range(3)]

        if pressed_key_codes[0] == -1:
            break

        if UP_KEY_CODE in pressed_key_codes:
            rows_direction = -ROWS_SPEED

        if DOWN_KEY_CODE in pressed_key_codes:
            rows_direction = ROWS_SPEED

        if RIGHT_KEY_CODE in pressed_key_codes:
            columns_direction = COLUMNS_SPEED

        if LEFT_KEY_CODE in pressed_key_codes:
            columns_direction = -COLUMNS_SPEED

        if SPACE_KEY_CODE in pressed_key_codes:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed
