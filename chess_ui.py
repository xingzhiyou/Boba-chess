import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPaintEvent
from PyQt5.QtCore import Qt

BOARD_SIZE = 9
CELL_SIZE = 50
MARGIN = 60


class ChessBoard(QWidget):
    def __init__(self, boba, move_list_widget=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = boba
        self.setFixedSize(MARGIN * 2 + CELL_SIZE * BOARD_SIZE, MARGIN * 2 + CELL_SIZE * BOARD_SIZE)
        self.selected = None
        self.move_history = []
        self.move_list_widget = move_list_widget  # 新增：用于显示历史的QListWidget
        self.is_game_over = False  # 新增：标记游戏是否结束

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter(self)
        # 显示剩余步数
        qp.setPen(QPen(Qt.black, 1))
        qp.setFont(qp.font())
        text = f"剩余步数: {self.game.turns_left}"
        qp.drawText(MARGIN, MARGIN // 2, text)
        # 显示当前玩家颜色或胜负
        if self.is_game_over:
            winner = self.game.get_winner()
            if winner == 1:
                color_text = "回合结束，红方胜"
                qp.setPen(QPen(Qt.red, 2))
            elif winner == 2:
                color_text = "回合结束，蓝方胜"
                qp.setPen(QPen(Qt.blue, 2))
            else:
                color_text = "回合结束，平局"
                qp.setPen(QPen(Qt.black, 2))
        else:
            if self.game.turns_left == 0:
                color_text = "回合结束"
                qp.setPen(QPen(Qt.black, 2))
            else:
                color_text = "当前回合: 红方" if self.game.current_player == 1 else "当前回合: 蓝方"
                qp.setPen(QPen(Qt.red if self.game.current_player == 1 else Qt.blue, 2))
        qp.setFont(qp.font())
        qp.drawText(MARGIN + 200, MARGIN // 2, color_text)
        # 显示双方分数
        p1, p2 = self.game.count_territory()
        qp.setPen(QPen(Qt.red, 2))
        qp.drawText(MARGIN, self.height() - 10, f"红方分数: {p1}")
        qp.setPen(QPen(Qt.blue, 2))
        qp.drawText(self.width() - MARGIN - 100, self.height() - 10, f"蓝方分数: {p2}")
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
        # 绘制坐标（上方和左侧）
        qp.setPen(QPen(Qt.black, 1))
        qp.setFont(qp.font())
        for i in range(BOARD_SIZE):
            # 上方横坐标
            qp.drawText(MARGIN + i * CELL_SIZE + CELL_SIZE // 2 - 8, MARGIN - 10, str(i))
            # 左侧纵坐标
            qp.drawText(MARGIN - 25, MARGIN + i * CELL_SIZE + CELL_SIZE // 2 + 5, str(i))

    def mousePressEvent(self, event):
        if self.is_game_over:
            return  # 游戏结束禁止点击
        if event.button() == Qt.LeftButton:
            x = (event.y() - MARGIN) // CELL_SIZE
            y = (event.x() - MARGIN) // CELL_SIZE
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                if self.game.place_piece(x, y):
                    self.move_history.append((x, y))
                    if self.move_list_widget is not None:
                        self.move_list_widget.addItem(f"{x},{y}")
                        self.move_list_widget.scrollToBottom()
                    self.update()
                    if self.game.is_game_over():
                        self.is_game_over = True
                        if self.move_list_widget is not None:
                            winner = self.game.get_winner()
                            if winner == 1:
                                result = "红方胜"
                            elif winner == 2:
                                result = "蓝方胜"
                            else:
                                result = "平局"
                            self.move_list_widget.addItem(f"{result}")
                            self.move_list_widget.scrollToBottom()
                        self.update()

    def restart(self):
        from game import Game
        self.game = Game()
        self.move_history.clear()
        self.is_game_over = False
        self.update()


class MainWindow(QMainWindow):
    def __init__(self, boba):
        super().__init__()
        self.setWindowTitle("Boba Chess 9x9")
        self.move_list_widget = QListWidget()
        self.move_list_widget.setMinimumWidth(70)
        self.move_list_widget.setMaximumWidth(90)
        self.board = ChessBoard(boba, move_list_widget=self.move_list_widget)
        self.board.setParent(self)
        self.restart_button = QPushButton("开始/重开")
        self.restart_button.clicked.connect(self.restart_game)
        vbox = QVBoxLayout()
        vbox.addWidget(self.move_list_widget)
        vbox.addWidget(self.restart_button)
        vbox.setStretch(0, 1)
        vbox.setStretch(1, 0)
        vbox.setContentsMargins(0, 0, 0, 10)  # 底部留白，防止按钮或文字被遮挡
        layout = QHBoxLayout()
        layout.addWidget(self.board)
        layout.addLayout(vbox)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setFixedSize(self.board.width() + self.move_list_widget.width(), self.board.height() + 20)  # 高度+20，防止底部遮挡

    def restart_game(self):
        from game import Game
        self.board.restart()  # 调用ChessBoard的restart方法，重置棋盘状态
        self.move_list_widget.addItem("新一局")
        self.move_list_widget.scrollToBottom()
        self.board.update()


if __name__ == "__main__":
    from game import Game  # 确保game.py在同目录

    app = QApplication(sys.argv)
    game = Game()
    window = MainWindow(game)
    window.show()
    sys.exit(app.exec_())
