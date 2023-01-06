import glob


class Model:

    def __init__(self):
        self.database_name = "databases/hangman_words_ee.db"
        self.image_files = glob.glob("images/*png")  # All hangman images
        # New game
        self.new_word = None   # Random word from database
        self.user_word = []  # User find letter
        self.all_user_chars = []  # any letters entered incorrectly
        self.counter = 0  # Error counter (wrong letters)
        # Leaderboard
        self.player_name = "UNKNOWN"
        self.leaderboard_file = "leaderboard.txt"
        self.score_data = []  # Leaderboard file contents


