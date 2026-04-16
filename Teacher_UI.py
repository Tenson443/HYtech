import json
import arcade
import arcade.gui

with open("Constants.txt", "r") as file:
    data = json.load(file)

WINDOW_WIDTH = data["WINDOW_WIDTH"]
WINDOW_HEIGHT = data["WINDOW_HEIGHT"]
WINDOW_TITLE = data["WINDOW_TITLE"]

class First_screen(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLUE)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

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
        self.window.show_view(Student_screen())

    def go_to_teacher_screen(self, event):
        self.window.show_view(Teacher_screen())

    def on_draw(self):
        self.clear()
        self.manager.draw()


class Student_screen(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.messages = []

        self.title_text = arcade.Text("Student Screen", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50, arcade.color.BLACK, font_size=20, anchor_x="center")

        self.input_box = arcade.gui.UIInputText(
            x=20,
            y=20,
            width=WINDOW_WIDTH - 160,
            height=40,
            text="",
            text_color=arcade.color.BLACK
        )

        self.send_button = arcade.gui.UIFlatButton(
            x=WINDOW_WIDTH - 130,
            y=20,
            width=110,
            height=40,
            text="Send"
        )

        self.send_button.on_click = self.on_send

        self.manager.add(self.input_box.with_background(color=arcade.color.LIGHT_GRAY))
        self.manager.add(self.send_button)

    def on_send(self, event):
        message = self.input_box.text.strip()
        if message:
            self.messages.append(message)
            self.input_box.text = ""

    def on_draw(self):
        self.clear()
        self.title_text.draw()

        y = 80
        for message in reversed(self.messages):
            arcade.draw_text(message, WINDOW_WIDTH - 20, y, arcade.color.BLACK, font_size=14, anchor_x="right")
            y += 25

        self.manager.draw()


class Teacher_screen(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.messages = []

        self.title_text = arcade.Text("Teacher Screen", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50, arcade.color.BLACK, font_size=20, anchor_x="center")

        self.input_box = arcade.gui.UIInputText(
            x=20,
            y=20,
            width=WINDOW_WIDTH - 160,
            height=40,
            text="",
            text_color=arcade.color.BLACK
        )

        self.send_button = arcade.gui.UIFlatButton(
            x=WINDOW_WIDTH - 130,
            y=20,
            width=110,
            height=40,
            text="Send"
        )

        self.send_button.on_click = self.on_send

        self.manager.add(self.input_box.with_background(color=arcade.color.LIGHT_GRAY))
        self.manager.add(self.send_button)

    def on_send(self, event):
        message = self.input_box.text.strip()
        if message:
            self.messages.append(message)
            self.input_box.text = ""

    def on_draw(self):
        self.clear()
        self.title_text.draw()

        y = 80
        for message in reversed(self.messages):
            arcade.draw_text(message, WINDOW_WIDTH - 20, y, arcade.color.BLACK, font_size=14, anchor_x="right")
            y += 25

        self.manager.draw()


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.show_view(First_screen())
    arcade.run()

main()