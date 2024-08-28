import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import random

words = [
    'PYTHON', 'TKINTER', 'HANGMAN', 'PROGRAMMING', 'COMPUTER',
    'ASTROLOGY', 'PYRAMID', 'VORTEX', 'ZENITH', 'JAZZ',
    'KALEIDOSCOPE', 'EQUINOX', 'QUIXOTIC', 'FANTASY', 'VANGUARD',
    'SYMPHONY', 'EXPLORATION', 'MIRAGE', 'HORIZON', 'MYSTIQUE',
    'CHIMERA', 'ODYSSEY', 'TRIANGLE', 'FUSION',
    'GIRAFFE', 'LABYRINTH', 'VIRUS', 'ALCHEMY', 'ECLIPSE',
    'OASIS', 'FANTASIA', 'NEBULA', 'GARGANTUAN', 'COSMOS'
]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title('Hangman Game')

        self.root.geometry('800x800')

        self.font = Font(family='Comic Sans MS', size=20, weight='bold')
        self.button_color = '#FF69B4' 

        self.cloud_photo = self.load_image('cloud.gif')

        self.word = random.choice(words)
        self.guessed_letters = set()
        self.max_attempts = 6
        self.attempts = 0

        self.create_widgets()
        
        self.create_footer()

    def load_image(self, image_path):
        """Load an image and return a PhotoImage object."""
        try:
            image = tk.PhotoImage(file=image_path)
            return image
        except tk.TclError as e:
            print(f"Error loading image: {e}")
            return None

    def create_widgets(self):
        self.center_frame = tk.Frame(self.root, bg='purple', padx=20, pady=20)
        self.center_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.8)
        
        self.title_label = tk.Label(self.center_frame, text='Hangman Game', font=self.font, bg='purple', fg='white')
        self.title_label.pack(pady=10)

        self.word_label = tk.Label(self.center_frame, text=self.get_display_word(), font=self.font, bg='purple', fg='white')
        self.word_label.pack(pady=20)

        self.sticker_label = tk.Label(self.center_frame, text='', font=self.font, bg='purple', fg='white')
        self.sticker_label.pack(pady=10)

        self.guessed_label = tk.Label(self.center_frame, text='Guessed Letters: ', font=self.font, bg='purple', fg='white')
        self.guessed_label.pack(pady=10)

        self.guess_entry = tk.Entry(self.center_frame, font=self.font)
        self.guess_entry.pack(pady=10)

        self.guess_button = tk.Button(self.center_frame, text='Guess', command=self.guess, font=self.font, bg=self.button_color, fg='white')
        self.guess_button.pack(pady=10)

        self.show_missing_button = tk.Button(self.center_frame, text='Show Missing Letters', command=self.show_missing_letters, font=self.font, bg=self.button_color, fg='white')
        self.show_missing_button.pack(pady=10)

        self.reset_button = tk.Button(self.center_frame, text='Reset', command=self.reset_game, font=self.font, bg='#FF1493', fg='white')
        self.reset_button.pack(pady=10)

        self.attempts_label = tk.Label(self.center_frame, text=f'Attempts left: {self.max_attempts}', font=self.font, bg='purple', fg='white')
        self.attempts_label.pack(pady=10)

        self.add_cloud_stickers()

    def create_footer(self):
        """Create a footer with copyright information."""
        self.footer = tk.Label(self.root, text='© Biswajit Das Coding', font=self.font, bg='purple', fg='white')
        self.footer.pack(side=tk.BOTTOM, pady=10)

    def add_cloud_stickers(self):
        if self.cloud_photo:
            for _ in range(5):
                cloud_label = tk.Label(self.center_frame, image=self.cloud_photo, bg='purple')
                cloud_label.place(x=random.randint(0, 650), y=random.randint(0, 550))
        else:
            print("Cloud image not available. Stickers will not be displayed.")

    def get_display_word(self):
        display_word = ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])
        return display_word

    def guess(self):
        guess = self.guess_entry.get().upper()
        self.guess_entry.delete(0, tk.END)

        if not guess.isalpha() or len(guess) != 1:
            messagebox.showwarning('Invalid input', 'Please enter a single letter.')
            return

        if guess in self.guessed_letters:
            messagebox.showinfo('Already Guessed', 'You already guessed that letter.')
            return

        self.guessed_letters.add(guess)

        if guess in self.word:
            if set(self.word) == self.guessed_letters:
                self.end_game(True)
            else:
                self.word_label.config(text=self.get_display_word())
                self.sticker_label.config(text=self.get_random_sticker())
        else:
            self.attempts += 1
            self.attempts_label.config(text=f'Attempts left: {self.max_attempts - self.attempts}')
            if self.attempts >= self.max_attempts:
                self.end_game(False)

    def show_missing_letters(self):
        missing_letters = set(self.word) - self.guessed_letters
        missing_count = len(missing_letters)
        if missing_letters:
            messagebox.showinfo('Missing Letters', f'Missing Letters: {", ".join(missing_letters)}\nCount: {missing_count}')
        else:
            messagebox.showinfo('All Letters Guessed', 'You have guessed all the letters!')

    def get_random_sticker(self):
        return f"🎉 {' '.join(random.choices(['#FFDDC1', '#FFABAB', '#FFC3A0'], k=1))} 🎉"

    def end_game(self, won):
        if won:
            messagebox.showinfo('Congratulations!', 'You guessed the word!')
        else:
            messagebox.showerror('Game Over', f'You lost! The word was: {self.word}')
        self.reset_game()

    def reset_game(self):
        self.word = random.choice(words)
        self.guessed_letters = set()
        self.attempts = 0
        self.word_label.config(text=self.get_display_word())
        self.sticker_label.config(text='')
        self.guessed_label.config(text='Guessed Letters: ')
        self.attempts_label.config(text=f'Attempts left: {self.max_attempts}')

if __name__ == '__main__':
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
