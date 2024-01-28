from PyQt5.QtWidgets import QApplication, QGraphicsSceneMouseEvent, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel, QVBoxLayout, QWidget, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal

class ChessSquare(QGraphicsRectItem):
    def __init__(self, x, y, size, row, col, piece, square_color):
        super().__init__()

        self.setAcceptHoverEvents(True)
        
        self.row = row
        self.col = col
        self.piece = piece
        self.square_color = QColor(square_color)

        self.setRect(x, y, size, size)
        self.setBrush(self.square_color)

        self.piece_pixmap = QPixmap(self.get_piece_image_path()) if self.piece.color is not None else QPixmap()

        self.hovered = False
        self.clicked = False

    def get_piece_image_path(self):
        return f"Chess_pieces/{self.piece.color}_{self.piece.getName()}.png" if self.piece.color is not None else "Chess_pieces/empty_square.png"

    def paint(self, painter, option, widget=None):
        # Draw the square
        super().paint(painter, option, widget)

        # Draw the piece
        if not self.piece_pixmap.isNull():
            # Convert QRectF to QRect
            rect = self.rect().toRect()
            # Alternatively, use the position and size directly
            # x, y, w, h = self.rect().getRect()
            # rect = QRect(x, y, w, h)

            painter.drawPixmap(rect, self.piece_pixmap)
        
        if self.hovered:
            painter.fillRect(self.rect(), QColor(255, 255, 255, 128))  # semi-transparent white overlay

        if self.clicked and self.piece.color != None:
            painter.fillRect(self.rect(), QColor(255, 0, 0, 128))
        
    def hoverEnterEvent(self, event):
        # Change the state when the mouse hovers over the square
        self.hovered = True
        self.update()  # This will trigger the paint event

    def hoverLeaveEvent(self, event):
        # Reset the state when the mouse leaves the square
        self.hovered = False
        self.update()  # This will trigger the paint event

    def mousePressEvent(self, event):
        self.clicked = True
        self.update()

    def unselect(self):
        self.clicked = False
        self.update()

class StartButtonSignals(QObject):
    # Define a new signal called 'clicked'
    clicked = pyqtSignal()

class StartButton(QGraphicsRectItem):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.signals = StartButtonSignals()
        self.rect_width = 100
        self.rect_height = 50
        self.color = "#f0d9b5"
        self.setRect((screen_width-self.rect_width)/2, (screen_height-self.rect_height)/2, self.rect_width, self.rect_height)
        self.setBrush(QColor("#f0d9b5"))
        
        # Text on the button
        self.textItem = QGraphicsTextItem("Play", self)
        #self.textItem.setFont(QFont("Arial", 14))
        self.textItem.setDefaultTextColor(Qt.black)
        self.centerText(screen_width, screen_height)

    def centerText(self, screen_width, screen_height):
        """ Center the text inside the button """
        rect = self.textItem.boundingRect()
        x = (self.rect().width() - rect.width()) / 2 + (screen_width-self.rect_width)/2
        y = (self.rect().height() - rect.height()) / 2 + (screen_height-self.rect_height)/2
        self.textItem.setPos(x, y)

    def mousePressEvent(self, event):
        self.signals.clicked.emit()

    


