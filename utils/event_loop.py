from types import coroutine

COROUTINES: coroutine = []


def get_coroutines():
    global COROUTINES
    return COROUTINES


def append_coroutine(new_coroutine: coroutine):
    global COROUTINES
    COROUTINES.append(new_coroutine)


def delete_coroutine(exhaustion_coroutine):
    global COROUTINES
    COROUTINES.remove(exhaustion_coroutine)
