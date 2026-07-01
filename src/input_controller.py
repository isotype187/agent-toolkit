from pynput import mouse, keyboard
import threading
import time

kb = keyboard.Controller()

enabled = False

right_held = False
left_dragging = False

copy_ready = False   # ?? NEW STATE FLAG


def toggle():
    global enabled
    enabled = not enabled
    print(f"[Automation Mode] {enabled}")


def on_click(x, y, button, pressed):

    global right_held, left_dragging, copy_ready

    if not enabled:
        return

    # -----------------------
    # RIGHT BUTTON TRACKING
    # -----------------------
    if button == mouse.Button.right:

        if pressed:
            right_held = True
        else:
            right_held = False

        return

    # -----------------------
    # LEFT BUTTON LOGIC
    # -----------------------
    if button == mouse.Button.left:

        # LEFT DOWN
        if pressed:
            left_dragging = True

        # LEFT UP
        else:

            # CASE 1: COPY ON RELEASE
            if left_dragging and not right_held:
                time.sleep(0.05)

                with kb.pressed(keyboard.Key.ctrl):
                    kb.press('c')
                    kb.release('c')

                copy_ready = True   # ?? SET STATE ONLY HERE

            # CASE 2: RIGHT HELD + LEFT CLICK = ENTER ONLY
            if right_held:
                kb.press(keyboard.Key.enter)
                kb.release(keyboard.Key.enter)

            left_dragging = False


def on_move(x, y):
    pass


def on_scroll(x, y, dx, dy):
    pass


def start_listener():
    listener = mouse.Listener(
        on_click=on_click,
        on_move=on_move,
        on_scroll=on_scroll
    )
    listener.start()
    listener.join()


def start():
    thread = threading.Thread(target=start_listener, daemon=True)
    thread.start()
