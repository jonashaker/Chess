import logic

from gui_elements import ChessSquare, StartButton

import sys
from PyQt5.QtWidgets import QApplication, QGraphicsSceneMouseEvent, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel, QVBoxLayout, QWidget, QGraphicsRectItem, QPushButton
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QMessageBox
import ai



class GUI(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.screen_width = 500
        self.screen_height = 600
        self.setSceneRect(0, 0, self.screen_width, self.screen_height)

        self.square_size = 60
        self.rows = 8
        self.columns = 8     

        self.playing_game = False

        self.init_labels()
        self.hide_labels()
        self.init_ui()   

    def init_labels(self):
        self.turn_label = QLabel("Turn: White", self)
        self.check_label = QLabel(self)
        self.checkmate_label = QLabel(self)
        
    def show_labels(self):
        self.turn_label.show()
        self.check_label.show()
        self.checkmate_label.show()

    def hide_labels(self):
        self.turn_label.hide()
        self.check_label.hide()
        self.checkmate_label.hide()

    def init_ui(self):
        start_button = StartButton(self.screen_width, self.screen_height)
        self.scene.addItem(start_button)
        start_button.signals.clicked.connect(self.start_game)

    def start_game(self):
        self.chessgame = logic.GameLogic()
        self.ai = ai.AI("black", self.chessgame)
        self.show_labels()
        self.draw_chessboard()
        self.game_started = True
        self.selected_square = None
        self.first_click = None
        self.second_click = None
    
    def end_game(self):
        self.playing_game = False
        self.scene.clear()
        self.init_labels()
        self.hide_labels()
        self.init_ui()

    def draw_chessboard(self):
        self.scene.clear()
        colors = ["#f0d9b5", "#b58863"]  # Light and dark square colors

        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.square_size
                y = row * self.square_size
                piece = self.chessgame.chessboard[row][col]
                square_color = colors[(row+col) % 2]
                square = ChessSquare(x, y, self.square_size, row, col, piece, square_color)
                self.scene.addItem(square)

    def update_turn_label(self):
        self.turn_label.setText(f"Turn: {self.chessgame.turn.capitalize()}")
    
    def update_check_label(self, update):
        if update:
            self.check_label.setText(f"Check: {self.chessgame.turn.capitalize()} King")
        else:
            self.check_label.setText("")

    def update_check_mate_label(self):
        self.check_label.setText(f"Check mate: {self.chessgame.turn.capitalize()} Lost")

    def game_condition_checker(self):
        """Checks the condition of the game and updates the gui labels."""
        if self.chessgame.is_in_check():
                if self.chessgame.is_checkmate():
                    self.end_game()
                else:
                    self.update_check_label(True)
        else:
            self.update_check_label(False)

    def mousePressEvent(self, event):
        """Trigger when the player presses a square on the gameboard. Handles moving pieces."""
        super().mousePressEvent(event)
        if not self.game_started:
            return
        clicked_square = self.scene.itemAt(event.pos(), self.transform())

        if isinstance(clicked_square, ChessSquare):
            if self.selected_square and self.selected_square != clicked_square:
                try:
                    self.selected_square.unselect()
                except RuntimeError:
                    # The object has been deleted; reset the reference
                    self.selected_square = None

            self.selected_square = clicked_square

            if self.first_click is None:
                if self.chessgame.chessboard[clicked_square.row][clicked_square.col].color is None:
                    pass
                else:
                    self.first_click = (clicked_square.row, clicked_square.col)

            elif self.second_click is None:
                self.second_click = (clicked_square.row, clicked_square.col)
                self.selected_square.unselect()
        
                if self.chessgame.is_valid_move(self.first_click, self.second_click):
                    self.chessgame.make_move(self.first_click, self.second_click)
                    self.draw_chessboard()
                    self.update_turn_label()
                    self.game_condition_checker()
                    self.ai_move()
                else:
                    self.show_message("Illegal Move")
                
                self.first_click = None
                self.second_click = None

                #self.ai_move()
    
    def ai_move(self):
        self.ai.update_chessgame(self.chessgame)
        start, to = self.ai.random_strategy()
        self.chessgame.make_move(start, to)
        self.draw_chessboard()
        self.update_turn_label()
        self.game_condition_checker()


    def show_message(self, message):
        if message == "Illegal Move":
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Illegal Move")
            msg_box.setText("Illegal Move")
            msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()

    main_widget = QWidget()
    layout = QVBoxLayout(main_widget)
    layout.addWidget(gui)
    layout.addWidget(gui.turn_label)
    layout.addWidget(gui.check_label)
    layout.addWidget(gui.checkmate_label)
    #main_widget.resize(800, 600)
    main_widget.show()

    sys.exit(app.exec_())




