from tkinter import simpledialog, messagebox

from GameTime import GameTime
from Model import Model
from View import View
from os import path


class Controller:

    def __init__(self, db_name=None):
        self.model = Model()
        if db_name is not None:
            self.model.database_name = db_name  # database file changed
        self.view = View(self, self.model)
        self.gametime = GameTime(self.view.lbl_time)   # Create gametime object

    def main(self):
        self.view.main()

    def click_btn_new(self):
        self.view.btn_new["state"] = "disabled"
        self.view.btn_cancel["state"] = "normal"
        self.view.btn_send["state"] = "normal"
        self.view.char_input["state"] = "normal"
        self.view.change_image(0)  # image changes with index
        self.model.start_new_game()  # Starting new game
        self.view.lbl_result.configure(text=self.model.user_word)
        self.view.lbl_error.configure(text="Wrong 0 letter(s)", fg="black")
        self.view.char_input.focus()   # Active input files
        self.gametime.reset()
        self.gametime.start()

    def click_btn_cancel(self):
        self.gametime.stop()
        self.view.btn_new["state"] = "normal"
        self.view.btn_cancel["state"] = "normal"
        self.view.btn_send["state"] = "disabled"
        self.view.char_input["state"] = "disabled"
        self.view.char_input.delete(0, "end")
        self.view.change_image(len(self.model.image_files) - 1)

    def click_btn_send(self):
        self.model.get_user_input(self.view.userinput.get().strip())
        self.view.lbl_result.configure(text=self.model.user_word)
        self.view.lbl_error.configure(text=f"Wrong{self.model.counter} letter(s). {self.model.get_all_user_chars()}")
        self.view.char_input.delete(0, "end")
        if self.model.counter > 0:
            self.view.lbl_error.configure(fg="red")   # Font color
            self.view.change_image(self.model.counter)   # error image change
        self.is_game_over()

    def is_game_over(self):
        if self.model.counter >= 11 or "_" not in self.model.user_word \
                or self.model.counter >= (len(self.model.image_files) - 1):
            self.gametime.stop()
            self.gametime.stop()
            self.view.btn_new["state"] = "normal"
            self.view.btn_cancel["state"] = "disabled"
            self.view.btn_send["state"] = "disabled"
            self.view.char_input["state"] = "disabled"
            player_name = simpledialog.askstring("Game over", "What is the player\'s name?", parent=self.view)
            self.model.set_player_name(player_name, self.gametime.counter)
            self.view.change_image(len(self.model.image_files) - 1)

    def click_btn_leaderboard(self):
        if path.exists(self.model.leaderboard_file) and path.isfile(self.model.leaderboard_file):
            popup_window = self.view.create_popup_window()
            data = self.model.read_leaderboard_file_contents()
            self.view.generate_leaderboard(popup_window, data)
            self.view.create_all_buttons()
        else:
            messagebox.showwarning("Message", " Leaderboard file is missing.\nPlay first!")
