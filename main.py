import tkinter as tk
from PIL import Image, ImageTk
import random
from collections import Counter
from tkinter import font


class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Loading...")
        self.root.geometry("350x550")
        self.root.resizable(width=False, height=False)
        self.root.configure(bg="lightblue") 
        
        font1 = tk.font.Font(family="Times", size=12, weight="normal", slant="italic")
        
        self.loading_label = tk.Label(self.root, text="Loading game, please wait...", font=font1,bg="lightblue")
        self.loading_label.grid(row=0, column=1, pady=20)

        cube_images = [
            ImageTk.PhotoImage(Image.open("images/dice1.png").resize((50, 50))),
            ImageTk.PhotoImage(Image.open("images/dice2.png").resize((50, 50))),
            ImageTk.PhotoImage(Image.open("images/dice3.png").resize((50, 50))),
            ImageTk.PhotoImage(Image.open("images/dice4.png").resize((50, 50))),
            ImageTk.PhotoImage(Image.open("images/dice5.png").resize((50, 50))),
            ImageTk.PhotoImage(Image.open("images/dice6.png").resize((50, 50)))
        ]

        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame3 = tk.Frame(self.root)
        self.frame4 = tk.Frame(self.root)
        self.frame5 = tk.Frame(self.root)
        self.frame6 = tk.Frame(self.root)

        self.frame1.grid(row=1, column=1, pady=10, padx=10)
        self.frame2.grid(row=2, column=1, pady=10, padx=10)
        self.frame3.grid(row=3, column=1, pady=10, padx=10)
        self.frame4.grid(row=4, column=1, pady=10, padx=10)
        self.frame5.grid(row=5, column=1, pady=10, padx=10)
        self.frame6.grid(row=6, column=1, pady=10, padx=10)

        self.animate_images(self.frame1, 6, cube_images)
        self.animate_images(self.frame2, 6, cube_images)
        self.animate_images(self.frame3, 6, cube_images)
        self.animate_images(self.frame4, 6, cube_images)
        self.animate_images(self.frame5, 6, cube_images)
        self.animate_images(self.frame6, 6, cube_images)

        self.root.after(3000, self.start_game)

    def start_game(self):
        self.root.destroy()

        root = tk.Tk()
        game = YadziGame(root)
        game.new_game()
        root.mainloop()

    def animate_images(self, frame, num_images, cube_images):
        def change_image(image_label, frame, num_images):
            if num_images <= 0:
                return

            image_index = random.randint(0, 5)
            image = cube_images[image_index]
            image_label.config(image=image)
            image_label.image = image

            self.root.after(1000, change_image, image_label, frame, num_images - 1)

        for i in range(num_images):
            image_index = random.randint(0, 5)
            image = cube_images[image_index]
            image_label = tk.Label(frame, image=image,bg="lightblue")
            image_label.grid(row=0, column=i)
            change_image(image_label, frame, num_images)



class YadziGame:
    def __init__(self, window):
        self.window = window
        self.window.geometry("350x550")
        self.window.title("Yatzi")
        self.window.resizable(width=False, height=False)
        self.window.configure(bg="lightblue") 

        new_image = Image.open(f"images/new_game.png")
        new_image = new_image.resize((100, 40))
        self.new_image = ImageTk.PhotoImage(new_image)
        
        exit_image = Image.open(f"images/exit.png")
        exit_image = exit_image.resize((100, 40))
        self.exit_image = ImageTk.PhotoImage(exit_image)
        
        self.cube_png = [ImageTk.PhotoImage(Image.open(f"images/dice{i}.png").resize((64, 64))) for i in range(1, 7)]
        self.cube_undefined = ImageTk.PhotoImage(Image.open("images/dice_nan.png").resize((64, 64)))

        self.cube_player = [None] * 5
        self.pc_cube = [None] * 5
        self.pc_score = 0
        self.player_score = 0
        self.pas = 0
        self.flag = 0
        self.history = []

        self.create_icons()

    def create_icons(self):

        font1 = tk.font.Font(family="Times", size=12, weight="normal", slant="italic")
        self.player_result_label = tk.Label(self.window, text="", font=font1,bg="lightblue")
        self.player_result_label.grid(row=1, column=7, columnspan=5)

        self.pc_result_label = tk.Label(self.window, text="", font=font1,bg="lightblue")
        self.pc_result_label.grid(row=3, column=7, columnspan=5)

        self.submut_score = tk.Label(self.window, text="", font=font1,bg="lightblue")
        self.submut_score.grid(row=2, column=7, columnspan=5)

        self.history_text = tk.Text(self.window, height=10, width=40, bd=0,bg="lightblue")
        self.history_text.grid(row=6, column=9, columnspan=5, padx=10, pady=10)


        self.dice_buttons = [tk.Button(self.window, image="", bd=0,bg="lightblue") for _ in range(5)]
        for i, dice_button in enumerate(self.dice_buttons):
                dice_button.grid(row=1+i, column=1)

        self.pc_cube_buttons = [tk.Button(self.window, image="", bd=0,bg="lightblue") for _ in range(5)]
        for i, pc_cube_button in enumerate(self.pc_cube_buttons):
            pc_cube_button.grid(row=i+1, column=3)

        self.cube_player_label = tk.Label(self.window, text="" , font=font1)

        self.cube_player_value = tk.Label(self.window, text="", font=font1)

        self.pc_cube_label = tk.Label(self.window, text="" , font=font1)

        self.pc_cube_value = tk.Label(self.window, text="", font=font1)
        
        self.new_game_button = tk.Button(self.window, image=self.new_image, command=self.new_game, font=font1, relief="flat",bg="lightblue")
        self.new_game_button.grid(row=4, column=7, columnspan=5)
        
        self.quit_button = tk.Button(self.window, image=self.exit_image, command=self.window.quit, font=font1, relief="flat",bg="lightblue")
        self.quit_button.grid(row=5, column=7, columnspan=5)

    
    def new_game(self):
        self.pc_score = 0
        self.player_score = 0
        self.pas = 0
        self.flag = 0
        self.cube_player.clear()
        self.pc_cube.clear()
        for i in range(5):
            self.cube_player.append(None)
            self.pc_cube.append(None)
            self.dice_buttons[i].config(image=self.cube_undefined , command = self.spin,bg="lightblue")
            self.pc_cube_buttons[i].config(image=self.cube_undefined, command = self.spin,bg="lightblue")

        self.player_result_label.config(text="")
        self.pc_result_label.config(text="")
        self.submut_score.config(text="")
        self.history_text.delete("1.0", "end")
        self.history.clear()
        self.cube_player_value.config(text="")
        self.pc_cube_value.config(text="")

    def animation_swap(self, clock, dice_buttons, dice_v, dice_numer):
        if clock == 0:
            self.show_result()
            return

        dice_i = random.randint(0, 4)
        dice_v[dice_i] = random.randint(1, 6)

        for i in range(5):
            if dice_v[i] is not None:
                dice_buttons[i].config(image=self.cube_png[dice_v[i] - 1] , state="disabled",bg="lightblue")
            else:
                dice_buttons[i].config(image=self.cube_undefined , state="disabled",bg="lightblue")

        self.window.after(5, self.animation_swap, clock - 1, dice_buttons, dice_v, dice_numer)
        
        
    def spin(self):
        self.flag = 0
        for i in range(5):
            self.dice_buttons[i].config(image="" )
        self.animation_swap(40, self.dice_buttons, self.cube_player, self.cube_player_value)
        self.spin_pc()
    
    
    def spin_pc(self):
        for i in range(5):
            self.pc_cube_buttons[i].config(image="")
        self.animation_swap(40, self.pc_cube_buttons, self.pc_cube, self.pc_cube_value)
        
    def show_result(self):
        for i in range(5):
            self.dice_buttons[i].config(state="active",bg="lightblue")
            self.pc_cube_buttons[i].config(state="active",bg="lightblue")
        counts = [self.cube_player.count(i) for i in range(1, 7)]

        if 2 in counts:
            self.player_score = 5

        elif 3 in counts:
            self.player_score = 10
        elif 4 in counts:
            self.player_score = 20
        elif 5 in counts:
            self.player_score = 50

        counts = [self.pc_cube.count(i) for i in range(1, 7)]

        if 2 in counts:
            self.pc_score = 5

        elif 3 in counts:
            self.pc_score = 10
        elif 4 in counts:
            self.pc_score = 20
        elif 5 in counts:
            self.pc_score = 50
        self.pas += 1
        if self.pas % 2:
            if self.player_score > self.pc_score:
                self.history.append(f"U:{self.player_score} \ PC:{self.pc_score} Win")
            elif self.player_score == self.pc_score:
                self.history.append(f"U:{self.player_score} \ PC:{self.pc_score} Draw")
            else:
                self.history.append(f"U:{self.player_score} \ PC:{self.pc_score} Loss")
            
            self.history_text.delete("1.0", "end")
            for line in self.history:
                self.history_text.insert("end", line + "\n")
        else:
            pass
        self.player_result_label.config(text=f"Your result: {self.player_score} points" )
        self.pc_result_label.config(text=f"Result PC: {self.pc_score} points")
        if self.player_score > self.pc_score:
            self.submut_score.config(text=f"U WIN!")
        elif self.player_score < self.pc_score:
            self.submut_score.config(text=f"U Loss")
        elif self.player_score == self.pc_score:
            self.submut_score.config(text=f"Draw")


"""
if __name__ == "__main__":
    root = tk.Tk()
    game = YadziGame(root)
    game.new_game()
    root.mainloop()
"""
if __name__ == "__main__":
    root = tk.Tk()
    loading_screen = LoadingScreen(root)
    root.mainloop()

