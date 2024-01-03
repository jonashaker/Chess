from board import chessboard
import board
import pieces


import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox



class Chess(QGraphicsView):
    def __init__(self, chessboard):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.turn_label = QLabel("Turn: White", self)
        self.turn_label.setGeometry(10, 10, 100, 30)

        self.square_size = 60
        self.rows = 8
        self.columns = 8

        self.chessboard = chessboard

        self.draw_chessboard()

        self.start = None
        self.to = None
        self.turn = "white"

    def draw_chessboard(self):
        self.scene.clear()

        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.square_size
                y = row * self.square_size
                piece = self.chessboard[row][col]
                square = ChessSquare(x, y, self.square_size, row, col, piece)
                self.scene.addItem(square)

    def switch_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

        self.update_turn_label()

    def update_turn_label(self):
        self.turn_label.setText(f"Turn: {self.turn.capitalize()}")

    def check_turn(self, piece):
        return piece.color == self.turn

    def mousePressEvent(self, event):
        item = self.scene.itemAt(event.pos(), self.transform())
        if isinstance(item, ChessSquare):
            if self.start is None:
                if self.chessboard[item.row][item.col].color is None:
                    pass
                else:
                    self.start = (item.row, item.col)
            elif self.to is None:
                self.to = (item.row, item.col)
                
                if self.chessboard[self.start[0]][self.start[1]].is_valid_move(self.chessboard, self.start, self.to) and self.check_turn(self.chessboard[self.start[0]][self.start[1]]):
                    self.chessboard = board.update_board(self.chessboard, self.start, self.to)
                    self.draw_chessboard()
                    self.switch_turn()
                else:
                    self.show_message("Illegal Move")
                

                self.start = None
                self.to = None

    def show_message(self, message):
        if message == "Illegal Move":
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Illegal Move")
            msg_box.setText("Illegal Move")
            msg_box.exec_()
        

class ChessSquare(QGraphicsPixmapItem):
    def __init__(self, x, y, size, row, col, piece):
        super().__init__()

        self.setPos(x, y)
        self.setAcceptHoverEvents(True)

        self.row = row
        self.col = col

        self.piece = piece
    
        self.setPixmap(QPixmap(self.get_piece_image_path()))

    def get_piece_image_path(self):
        return f"Chess_pieces/{self.piece.color}_{self.piece.getName()}.png" if self.piece.color is not None else "Chess_pieces/empty_square.png"



if __name__ == "__main__":
    app = QApplication(sys.argv)
    chess = Chess(chessboard)

    main_widget = QWidget()
    layout = QVBoxLayout(main_widget)
    layout.addWidget(chess)
    layout.addWidget(chess.turn_label)

    main_widget.show()

    sys.exit(app.exec_())



