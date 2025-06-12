import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPaintEvent
from PyQt5.QtCore import Qt

BOARD_SIZE = 9
CELL_SIZE = 50
MARGIN = 40


class ChessBoard(QWidget):
    def __init__(self, boba, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = boba
        self.setFixedSize(MARGIN * 2 + CELL_SIZE * BOARD_SIZE, MARGIN * 2 + CELL_SIZE * BOARD_SIZE)
        self.selected = None

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter(self)
        # 显示剩余步数
        qp.setPen(QPen(Qt.black, 1))
        qp.setFont(qp.font())
        text = f"剩余步数: {self.game.turns_left}"
        qp.drawText(MARGIN, MARGIN // 2, text)
        # 绘制格子
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x = MARGIN + j * CELL_SIZE
                y = MARGIN + i * CELL_SIZE
                # 领地染色
                if self.game.territory[i, j] == 1:
                    qp.setBrush(QBrush(QColor(255, 230, 180)))
                elif self.game.territory[i, j] == 2:
                    qp.setBrush(QBrush(QColor(180, 220, 255)))
                else:
                    qp.setBrush(Qt.white)
                qp.setPen(QPen(Qt.black, 1))
                qp.drawRect(x, y, CELL_SIZE, CELL_SIZE)
                # 棋子
                if self.game.board[i, j] == 1:
                    qp.setBrush(QBrush(QColor(200, 80, 80)))
                    qp.setPen(Qt.NoPen)
                    qp.drawEllipse(x + 8, y + 8, CELL_SIZE - 16, CELL_SIZE - 16)
                elif self.game.board[i, j] == 2:
                    qp.setBrush(QBrush(QColor(80, 80, 200)))
                    qp.setPen(Qt.NoPen)
                    qp.drawEllipse(x + 8, y + 8, CELL_SIZE - 16, CELL_SIZE - 16)
        # 绘制网格线
        qp.setPen(QPen(Qt.black, 2))
        for i in range(BOARD_SIZE + 1):
            qp.drawLine(MARGIN, MARGIN + i * CELL_SIZE, MARGIN + BOARD_SIZE * CELL_SIZE, MARGIN + i * CELL_SIZE)
            qp.drawLine(MARGIN + i * CELL_SIZE, MARGIN, MARGIN + i * CELL_SIZE, MARGIN + BOARD_SIZE * CELL_SIZE)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = (event.y() - MARGIN) // CELL_SIZE
            y = (event.x() - MARGIN) // CELL_SIZE
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                if self.game.place_piece(x, y):
                    self.update()
                    if self.game.is_game_over():
                        winner = self.game.get_winner()
                        if winner == 1:
                            msg = "红方胜利！"
                        elif winner == 2:
                            msg = "蓝方胜利！"
                        else:
                            msg = "平局！"
                        from PyQt5.QtWidgets import QMessageBox
                        reply = QMessageBox.information(self, "游戏结束", msg + "\n点击确定开始新一局。", QMessageBox.Ok)
                        if reply == QMessageBox.Ok:
                            from game import Game
                            self.game = Game()
                            self.update()


class MainWindow(QMainWindow):
    def __init__(self, boba):
        super().__init__()
        self.setWindowTitle("Boba Chess 9x9")
        self.board = ChessBoard(boba)
        self.setCentralWidget(self.board)
        self.setFixedSize(self.board.width(), self.board.height())


if __name__ == "__main__":
    from game import Game  # 确保game.py在同目录

    app = QApplication(sys.argv)
    game = Game()
    window = MainWindow(game)
    window.show()
    sys.exit(app.exec_())
