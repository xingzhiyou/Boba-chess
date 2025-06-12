# 泡姆泡姆啵叭棋复刻

本项目为泡姆泡姆啵叭棋的非官方复刻，仅供学习与交流使用。

## 玩法简介

- 9x9 棋盘，支持两名玩家对战。
- 规则与原作类似，支持领地扩张与消除。
- 详细规则见代码注释。

## 运行方法

1. 安装依赖（需要 Python 3 和 numpy）：
   ```sh
   pip install numpy
   ```
2. 运行游戏：
   ```sh
   python game.py
   ```

## game.py 文件说明

### 主要变量
- `BOARD_SIZE`：棋盘大小，默认为 9。
- `MAX_TURNS`：最大回合数，默认为 50。
- `self.board`：棋盘状态，0 表示空，1 表示玩家1，2 表示玩家2。
- `self.territory`：领地状态，0 表示无，1 表示玩家1，2 表示玩家2。
- `self.turns_left`：剩余回合数。
- `self.current_player`：当前玩家（1 或 2）。

### 主要函数
- `is_valid_move(x, y)`：判断 (x, y) 位置是否为当前玩家的有效落子点。
- `place_piece(x, y)`：在 (x, y) 位置落子，若成功返回 True，否则返回 False，并自动切换玩家。
- `check_lines(x, y)`：检查 (x, y) 处落子后是否形成连续的同色棋子线，返回所有满足条件的线坐标。
- `remove_and_expand(lines)`：消除形成的线，并将该线两端的空格扩展为当前玩家的领地。
- `count_territory()`：统计双方领地数，返回 (玩家1, 玩家2) 的领地格数。
- `is_game_over()`：判断游戏是否结束（回合数为 0）。
- `get_winner()`：返回获胜玩家（1/2），平局返回 0。

### 其他
- `print_board(game)`：打印当前棋盘和分数。
- `move_history`：记录每步操作，游戏结束后保存为 move_history.json。

## 版权声明

泡姆泡姆啵叭棋及其相关内容版权归 **鹰角网络** 所有。  
本项目仅为个人学习用途，与官方无关。

## 开源协议

本代码以 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

---

> 本项目与鹰角网络无直接关联，若有侵权请联系删除。