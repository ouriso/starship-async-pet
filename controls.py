from config import (
    ROWS_SPEED, COLUMNS_SPEED,
    UP_KEY_CODE, DOWN_KEY_CODE, RIGHT_KEY_CODE, LEFT_KEY_CODE, SPACE_KEY_CODE
)


def read_controls(canvas):
    """Read keys pressed and returns tuple with controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        canvas.nodelay(True)
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -ROWS_SPEED

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = ROWS_SPEED

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = COLUMNS_SPEED

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -COLUMNS_SPEED

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed
