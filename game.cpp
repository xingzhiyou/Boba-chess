// game.cpp
#include <iostream>
#include <vector>
#include <fstream>
#include <windows.h>
#include <string>
#include <sstream>

constexpr int BOARD_SIZE = 9;
constexpr int MAX_TURNS = 50;

class Game {
public:
    std::vector<std::vector<int>> board;
    std::vector<std::vector<int>> territory;
    int turns_left;
    int current_player;

    Game() : board(BOARD_SIZE, std::vector<int>(BOARD_SIZE, 0)),
             territory(BOARD_SIZE, std::vector<int>(BOARD_SIZE, 0)),
             turns_left(MAX_TURNS), current_player(1) {}

    bool is_valid_move(int x, int y) {
        if (board[x][y] != 0) return false;
        if (territory[x][y] != 0 && territory[x][y] != current_player) return false;
        return true;
    }

    bool place_piece(int x, int y) {
        if (!is_valid_move(x, y) || turns_left <= 0) return false;
        board[x][y] = current_player;
        turns_left--;
        auto lines = check_lines(x, y);
        if (!lines.empty()) {
            remove_and_expand(lines);
        }
        current_player = 3 - current_player;
        return true;
    }

    std::vector<std::vector<std::pair<int, int>>> check_lines(int x, int y) {
        int player = board[x][y];
        std::vector<std::pair<int, int>> directions = { {1,0}, {0,1}, {1,1}, {1,-1} };
        std::vector<std::vector<std::pair<int, int>>> lines;
        for (auto& dir : directions) {
            std::vector<std::pair<int, int>> coords = { {x, y} };
            int nx = x + dir.first, ny = y + dir.second;
            while (nx >= 0 && nx < BOARD_SIZE && ny >= 0 && ny < BOARD_SIZE && board[nx][ny] == player) {
                coords.emplace_back(nx, ny);
                nx += dir.first; ny += dir.second;
            }
            nx = x - dir.first; ny = y - dir.second;
            while (nx >= 0 && nx < BOARD_SIZE && ny >= 0 && ny < BOARD_SIZE && board[nx][ny] == player) {
                coords.insert(coords.begin(), {nx, ny});
                nx -= dir.first; ny -= dir.second;
            }
            if (coords.size() >= 3) lines.push_back(coords);
        }
        return lines;
    }

    void remove_and_expand(const std::vector<std::vector<std::pair<int, int>>>& lines) {
        int player = current_player;
        for (const auto& line : lines) {
            for (const auto& p : line) {
                board[p.first][p.second] = 0;
                territory[p.first][p.second] = player;
            }
            if (line.size() >= 2) {
                int dx = line[1].first - line[0].first;
                int dy = line[1].second - line[0].second;
                int nx = line.back().first + dx, ny = line.back().second + dy;
                while (nx >= 0 && nx < BOARD_SIZE && ny >= 0 && ny < BOARD_SIZE) {
                    if (board[nx][ny] != 0) break;
                    territory[nx][ny] = player;
                    nx += dx; ny += dy;
                }
                nx = line[0].first - dx; ny = line[0].second - dy;
                while (nx >= 0 && nx < BOARD_SIZE && ny >= 0 && ny < BOARD_SIZE) {
                    if (board[nx][ny] != 0) break;
                    territory[nx][ny] = player;
                    nx -= dx; ny -= dy;
                }
            }
        }
    }

    [[nodiscard]] std::pair<int, int> count_territory() const {
        int p1 = 0, p2 = 0;
        for (int i = 0; i < BOARD_SIZE; ++i) {
            for (int j = 0; j < BOARD_SIZE; ++j) {
                if (territory[i][j] == 1) ++p1;
                else if (territory[i][j] == 2) ++p2;
            }
        }
        return {p1, p2};
    }

    [[nodiscard]] bool is_game_over() const {
        return turns_left == 0;
    }

    [[nodiscard]] int get_winner() const {
        if (auto [p1, p2] = count_territory(); p1 > p2) return 1;
        else if (p2 > p1) return 2;
        else return 0;
    }
};

void print_board(const Game& game) {
    std::cout << "   ";
    for (int j = 0; j < BOARD_SIZE; ++j) std::cout << j << " ";
    std::cout << std::endl;
    for (int i = 0; i < BOARD_SIZE; ++i) {
        std::cout << i << " ";
        if (i < 10) std::cout << " ";
        for (int j = 0; j < BOARD_SIZE; ++j) {
            if (game.board[i][j] == 1) std::cout << "X ";
            else if (game.board[i][j] == 2) std::cout << "O ";
            else if (game.territory[i][j] == 1) std::cout << "# ";
            else if (game.territory[i][j] == 2) std::cout << "@ ";
            else std::cout << ". ";
        }
        std::cout << std::endl;
    }
    auto [p1, p2] = game.count_territory();
    std::cout << "\n分数：玩家1(X#): " << p1 << "  玩家2(O@): " << p2 << "  剩余回合: " << game.turns_left << "\n" << std::endl;
}

int main() {
    SetConsoleOutputCP(CP_UTF8);
    Game game;
    while (!game.is_game_over()) {
        print_board(game);
        int x, y;
        std::cout << "玩家" << game.current_player << "，请输入落子位置 (x y): ";
        std::cin >> x >> y;
        if (!game.place_piece(x, y)) {
            std::cout << "无效落子，请重试。" << std::endl;
            continue;
        }
        // 可扩展：记录历史、保存到文件等
    }
    print_board(game);
    if (const int winner = game.get_winner())
        std::cout << "玩家" << winner << "获胜！" << std::endl;
    else
        std::cout << "游戏结束，平局！" << std::endl;
    return 0;
}