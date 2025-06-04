import numpy as np
import json

BOARD_SIZE = 9
MAX_TURNS = 50

class Game:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)  # 0:空, 1:玩家1, 2:玩家2
        self.territory = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)  # 0:无, 1:玩家1, 2:玩家2
        self.turns_left = MAX_TURNS
        self.current_player = 1

    def is_valid_move(self, x, y):
        if self.board[x, y] != 0:
            return False
        if self.territory[x, y] != 0 and self.territory[x, y] != self.current_player:
            return False
        return True

    def place_piece(self, x, y):
        if not self.is_valid_move(x, y) or self.turns_left <= 0:
            return False
        self.board[x, y] = self.current_player
        self.turns_left -= 1
        lines = self.check_lines(x, y)
        if lines:
            self.remove_and_expand(lines)
        self.current_player = 3 - self.current_player
        return True

    def check_lines(self, x, y):
        player = self.board[x, y]
        directions = [ (1,0), (0,1), (1,1), (1,-1) ]
        lines = []
        for dx, dy in directions:
            coords = [(x, y)]
            nx, ny = x+dx, y+dy
            while 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and self.board[nx, ny]==player:
                coords.append((nx, ny))
                nx += dx
                ny += dy
            nx, ny = x-dx, y-dy
            while 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and self.board[nx, ny]==player:
                coords.insert(0, (nx, ny))
                nx -= dx
                ny -= dy
            if len(coords) >= 3:
                lines.append(coords)
        return lines

    def remove_and_expand(self, lines):
        player = self.current_player
        for line in lines:
            for x, y in line:
                self.board[x, y] = 0
                self.territory[x, y] = player
            if len(line) >= 2:
                dx = line[1][0] - line[0][0]
                dy = line[1][1] - line[0][1]
                nx, ny = line[-1][0] + dx, line[-1][1] + dy
                while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if self.board[nx, ny] != 0:
                        break
                    self.territory[nx, ny] = player
                    nx += dx
                    ny += dy
                nx, ny = line[0][0] - dx, line[0][1] - dy
                while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if self.board[nx, ny] != 0:
                        break
                    self.territory[nx, ny] = player
                    nx -= dx
                    ny -= dy

    def count_territory(self):
        p1 = np.sum(self.territory == 1)
        p2 = np.sum(self.territory == 2)
        return p1, p2

    def is_game_over(self):
        return self.turns_left == 0

    def get_winner(self):
        p1, p2 = self.count_territory()
        if p1 > p2:
            return 1
        elif p2 > p1:
            return 2
        else:
            return 0  # 平局

# 示例用法
def print_board(game):
    print("  " + "".join(f"{j:2d}" for j in range(BOARD_SIZE)))
    for i in range(BOARD_SIZE):
        row = f"{i:2d} "
        for j in range(BOARD_SIZE):
            if game.board[i, j] == 1:
                row += "X "
            elif game.board[i, j] == 2:
                row += "O "
            elif game.territory[i, j] == 1:
                row += "# "
            elif game.territory[i, j] == 2:
                row += "@ "
            else:
                row += ". "
        print(row)
    p1, p2 = game.count_territory()
    print(f"\n分数：玩家1(X#): {p1}  玩家2(O@): {p2}  剩余回合: {game.turns_left}\n")

move_history = []  # 新增：用于记录每步操作

if __name__ == "__main__":
    game = Game()
    ai_player = 2  # 设定AI为玩家2
    while not game.is_game_over():
        print_board(game)
        x, y = map(int, input(f"玩家{game.current_player}，请输入落子位置 (x y): ").split())
        if not game.place_piece(x, y):
            print("无效落子，请重试。")
            continue
        # 记录操作
        move_history.append({
            "player": 3 - game.current_player,  # 因为place_piece后已切换
            "move": [x, y],
            "board": game.board.tolist(),
            "territory": game.territory.tolist(),
            "turns_left": game.turns_left
        })
    print_board(game)
    winner = game.get_winner()
    if winner:
        print(f"玩家{winner}获胜！")
    else:
        print("游戏结束，平局！")
    # 保存操作历史
    with open("move_history.json", "w", encoding="utf-8") as f:
        json.dump(move_history, f, ensure_ascii=False, indent=2)
