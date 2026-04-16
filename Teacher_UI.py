import json
import requests
import arcade
import arcade.gui

with open("Constants.txt", "r") as file:
    data = json.load(file)

WINDOW_WIDTH = data["WINDOW_WIDTH"]
WINDOW_HEIGHT = data["WINDOW_HEIGHT"]
WINDOW_TITLE = data["WINDOW_TITLE"]

SERVER_URL = "http://localhost:5000"
STUDENT_NAME = "alice"


def send_message_to_server(role, student, message):
    try:
        r = requests.post(f"{SERVER_URL}/send_message", json={
            "role": role,
            "student": student,
            "message": message
        }, timeout=5)
        return r.json()
    except Exception as e:
        print(f"Server error: {e}")
        return None


def get_messages_from_server():
    try:
        r = requests.get(f"{SERVER_URL}/get_messages", timeout=5)
        return r.json()
    except Exception as e:
        print(f"Server error: {e}")
        return []


def get_stats_from_server():
    try:
        r = requests.get(f"{SERVER_URL}/get_stats", timeout=5)
        return r.json()
    except Exception as e:
        print(f"Server error: {e}")
        return []


def clear_chat_on_server():
    try:
        requests.post(f"{SERVER_URL}/clear_messages", timeout=5)
    except Exception as e:
        print(f"Server error: {e}")


class First_screen(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLUE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.student_screen = Student_screen(self)
        self.teacher_screen = Teacher_screen(self)

        my_button_2 = arcade.gui.UIFlatButton(text="Teacher", width=200)
        my_button_2.center_x = 300
        my_button_2.center_y = WINDOW_HEIGHT // 2

        my_button_1 = arcade.gui.UIFlatButton(text="Student", width=200)
        my_button_1.center_x = 500
        my_button_1.center_y = WINDOW_HEIGHT // 2

        my_button_1.on_click = self.go_to_student_screen
        my_button_2.on_click = self.go_to_teacher_screen

        self.manager.add(my_button_1)
        self.manager.add(my_button_2)

    def go_to_student_screen(self, event):
        self.manager.disable()
        self.window.show_view(self.student_screen)

    def go_to_teacher_screen(self, event):
        self.manager.disable()
        self.window.show_view(self.teacher_screen)

    def on_show_view(self):
        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.manager.draw()


class Student_screen(arcade.View):
    def __init__(self, first_screen):
        super().__init__()
        self.first_screen = first_screen
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = arcade.gui.UIManager()
        self.messages = []
        self.poll_timer = 0
        self.POLL_INTERVAL = 2

        self.title_text = arcade.Text("Student Screen", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50,
                                      arcade.color.BLACK, font_size=20, anchor_x="center")

        self.back_button = arcade.gui.UIFlatButton(x=10, y=WINDOW_HEIGHT - 50, width=100, height=35, text="Back")
        self.back_button.on_click = self.go_back
        self.manager.add(self.back_button)

        self.input_box = arcade.gui.UIInputText(x=20, y=20, width=WINDOW_WIDTH - 160, height=40,
                                                text="", text_color=arcade.color.BLACK)
        self.send_button = arcade.gui.UIFlatButton(x=WINDOW_WIDTH - 130, y=20, width=110, height=40, text="Send")
        self.send_button.on_click = self.on_send
        self.manager.add(self.input_box.with_background(color=arcade.color.LIGHT_GRAY))
        self.manager.add(self.send_button)

    def on_show_view(self):
        self.manager.enable()
        self.messages = get_messages_from_server()

    def on_hide_view(self):
        self.manager.disable()

    def go_back(self, event):
        self.window.show_view(self.first_screen)

    def on_send(self, event):
        message = self.input_box.text.strip()
        if message:
            send_message_to_server("student", STUDENT_NAME, message)
            self.input_box.text = ""
            self.messages = get_messages_from_server()

    def on_update(self, delta_time):
        self.poll_timer += delta_time
        if self.poll_timer >= self.POLL_INTERVAL:
            self.poll_timer = 0
            self.messages = get_messages_from_server()

    def on_draw(self):
        self.clear()
        self.title_text.draw()
        y = 80
        for msg in reversed(self.messages):
            role = msg.get("role", "student")
            sender = msg.get("student", "?")
            message = msg.get("message", "")
            color = arcade.color.BLUE if role == "student" else arcade.color.RED
            arcade.draw_text(f"{sender}: {message}", WINDOW_WIDTH - 20, y,
                             color, font_size=14, anchor_x="right")
            y += 25
        self.manager.draw()


class Teacher_screen(arcade.View):
    def __init__(self, first_screen):
        super().__init__()
        self.first_screen = first_screen
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = arcade.gui.UIManager()
        self.messages = []
        self.poll_timer = 0
        self.POLL_INTERVAL = 2

        self.title_text = arcade.Text("Teacher Screen", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50,
                                      arcade.color.BLACK, font_size=20, anchor_x="center")

        # back button
        self.back_button = arcade.gui.UIFlatButton(x=10, y=WINDOW_HEIGHT - 50, width=100, height=35, text="Back")
        self.back_button.on_click = self.go_back
        self.manager.add(self.back_button)

        # stats button
        self.stats_button = arcade.gui.UIFlatButton(x=120, y=WINDOW_HEIGHT - 50, width=130, height=35, text="View Stats")
        self.stats_button.on_click = self.go_to_stats
        self.manager.add(self.stats_button)

        # clear button
        self.clear_button = arcade.gui.UIFlatButton(x=260, y=WINDOW_HEIGHT - 50, width=130, height=35, text="Clear Chat")
        self.clear_button.on_click = self.on_clear
        self.manager.add(self.clear_button)

        self.input_box = arcade.gui.UIInputText(x=20, y=20, width=WINDOW_WIDTH - 160, height=40,
                                                text="", text_color=arcade.color.BLACK)
        self.send_button = arcade.gui.UIFlatButton(x=WINDOW_WIDTH - 130, y=20, width=110, height=40, text="Send")
        self.send_button.on_click = self.on_send
        self.manager.add(self.input_box.with_background(color=arcade.color.LIGHT_GRAY))
        self.manager.add(self.send_button)

    def on_show_view(self):
        self.manager.enable()
        self.messages = get_messages_from_server()

    def on_hide_view(self):
        self.manager.disable()

    def go_back(self, event):
        self.window.show_view(self.first_screen)

    def go_to_stats(self, event):
        stats_screen = Stats_screen(self)
        self.window.show_view(stats_screen)

    def on_clear(self, event):
        clear_chat_on_server()
        self.messages = []

    def on_send(self, event):
        message = self.input_box.text.strip()
        if message:
            send_message_to_server("teacher", "Teacher", message)
            self.input_box.text = ""
            self.messages = get_messages_from_server()

    def on_update(self, delta_time):
        self.poll_timer += delta_time
        if self.poll_timer >= self.POLL_INTERVAL:
            self.poll_timer = 0
            self.messages = get_messages_from_server()

    def on_draw(self):
        self.clear()
        self.title_text.draw()
        y = 80
        for msg in reversed(self.messages):
            role = msg.get("role", "student")
            sender = msg.get("student", "?")
            message = msg.get("message", "")
            color = arcade.color.BLUE if role == "student" else arcade.color.RED
            arcade.draw_text(f"{sender}: {message}", 20, y, color, font_size=14)
            y += 25
            if y > WINDOW_HEIGHT - 80:
                break
        self.manager.draw()


class Stats_screen(arcade.View):
    def __init__(self, teacher_screen):
        super().__init__()
        self.teacher_screen = teacher_screen
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = arcade.gui.UIManager()
        self.stats = get_stats_from_server()

        self.title_text = arcade.Text("Subject Statistics", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50,
                                      arcade.color.BLACK, font_size=22, anchor_x="center", bold=True)

        self.back_button = arcade.gui.UIFlatButton(x=10, y=WINDOW_HEIGHT - 50, width=100, height=35, text="Back")
        self.back_button.on_click = self.go_back
        self.manager.add(self.back_button)

        self.refresh_button = arcade.gui.UIFlatButton(x=120, y=WINDOW_HEIGHT - 50, width=100, height=35, text="Refresh")
        self.refresh_button.on_click = self.on_refresh
        self.manager.add(self.refresh_button)

    def on_show_view(self):
        self.manager.enable()
        self.stats = get_stats_from_server()

    def on_hide_view(self):
        self.manager.disable()

    def go_back(self, event):
        self.window.show_view(self.teacher_screen)

    def on_refresh(self, event):
        self.stats = get_stats_from_server()

    def on_draw(self):
        self.clear()
        self.title_text.draw()

        if not self.stats:
            arcade.draw_text("No data yet.", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                             arcade.color.GRAY, font_size=18, anchor_x="center")
            self.manager.draw()
            return

        max_count = max(s["count"] for s in self.stats)
        max_bar_width = WINDOW_WIDTH - 300
        bar_height = 36
        start_y = WINDOW_HEIGHT - 120
        label_x = 160

        for stat in self.stats:
            subject = stat["subject"]
            count = stat["count"]
            bar_width = int((count / max_count) * max_bar_width)

            # bar
            arcade.draw_lbwh_rectangle_filled(label_x, start_y, bar_width, bar_height, arcade.color.LIGHT_BLUE)
            arcade.draw_lbwh_rectangle_outline(label_x, start_y, max_bar_width, bar_height, arcade.color.GRAY)

            # subject label on the left
            arcade.draw_text(subject, label_x - 10, start_y + bar_height // 2,
                             arcade.color.BLACK, font_size=13, anchor_x="right", anchor_y="center")

            # count on the right of the bar
            arcade.draw_text(str(count), label_x + bar_width + 8, start_y + bar_height // 2,
                             arcade.color.BLACK, font_size=13, anchor_y="center")

            start_y -= bar_height + 14

        self.manager.draw()


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    first_screen = First_screen()
    window.show_view(first_screen)
    arcade.run()


main()