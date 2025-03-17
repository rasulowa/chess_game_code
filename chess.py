import copy
from abc import ABC, abstractmethod

class ChessPiece(ABC):
    def __init__(self, color):
        self.color = color
        self.symbol = ''

    @abstractmethod
    def get_valid_moves(self, board, position):
        pass

    def __repr__(self):
        return self.symbol

class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♙' if color == 'white' else '♟'
        self.has_moved = False

    def get_valid_moves(self, board, position):
        x, y = position
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        if board.is_within_board(x + direction, y) and not board.grid[x + direction][y]:
            moves.append((x + direction, y))
            if x == start_row and not board.grid[x + 2*direction][y]:
                moves.append((x + 2*direction, y))

        for dy in (-1, 1):
            if board.is_within_board(x + direction, y + dy):
                target = board.grid[x + direction][y + dy]
                if target and target.color != self.color:
                    moves.append((x + direction, y + dy))
        return moves

class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♖' if color == 'white' else '♜'

    def get_valid_moves(self, board, position):
        x, y = position
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while board.is_within_board(nx, ny):
                piece = board.grid[nx][ny]
                if not piece:
                    moves.append((nx, ny))
                else:
                    if piece.color != self.color:
                        moves.append((nx, ny))
                    break
                nx += dx
                ny += dy
        return moves

class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♘' if color == 'white' else '♞'

    def get_valid_moves(self, board, position):
        x, y = position
        moves = []
        jumps = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                 (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for dx, dy in jumps:
            nx, ny = x + dx, y + dy
            if board.is_within_board(nx, ny):
                piece = board.grid[nx][ny]
                if not piece or piece.color != self.color:
                    moves.append((nx, ny))
        return moves

class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♗' if color == 'white' else '♝'

    def get_valid_moves(self, board, position):
        x, y = position
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while board.is_within_board(nx, ny):
                piece = board.grid[nx][ny]
                if not piece:
                    moves.append((nx, ny))
                else:
                    if piece.color != self.color:
                        moves.append((nx, ny))
                    break
                nx += dx
                ny += dy
        return moves

class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♕' if color == 'white' else '♛'

    def get_valid_moves(self, board, position):
        x, y = position
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while board.is_within_board(nx, ny):
                piece = board.grid[nx][ny]
                if not piece:
                    moves.append((nx, ny))
                else:
                    if piece.color != self.color:
                        moves.append((nx, ny))
                    break
                nx += dx
                ny += dy
        return moves

class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♔' if color == 'white' else '♚'

    def get_valid_moves(self, board, position):
        x, y = position
        moves = []
        directions = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not (i == 0 and j == 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if board.is_within_board(nx, ny):
                piece = board.grid[nx][ny]
                if not piece or piece.color != self.color:
                    moves.append((nx, ny))
        return moves

# Дополнительные фигуры
class Archangel(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'A' if color == 'white' else 'a'

    def get_valid_moves(self, board, position):
        x, y = position
        moves = []
        king_moves = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]
        knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for dx, dy in king_moves + knight_moves:
            nx, ny = x + dx, y + dy
            if board.is_within_board(nx, ny):
                piece = board.grid[nx][ny]
                if not piece or piece.color != self.color:
                    moves.append((nx, ny))
        return moves

class Wizard(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'W' if color == 'white' else 'w'

    def get_valid_moves(self, board, position):
        x, y = position
        moves = []
        diagonals = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        straights = [(3, 0), (-3, 0), (0, 3), (0, -3)]
        for dx, dy in diagonals + straights:
            nx, ny = x + dx, y + dy
            if board.is_within_board(nx, ny):
                piece = board.grid[nx][ny]
                if not piece or piece.color != self.color:
                    moves.append((nx, ny))
        return moves

class Griffin(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'G' if color == 'white' else 'g'

    def get_valid_moves(self, board, position):
        x, y = position
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if not board.is_within_board(nx, ny):
                    break
                piece = board.grid[nx][ny]
                if not piece:
                    moves.append((nx, ny))
                elif piece.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
        return moves

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.init_board()

    def init_board(self):
        for i in range(8):
            self.grid[1][i] = Pawn('black')
            self.grid[6][i] = Pawn('white')
        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, piece in enumerate(pieces):
            self.grid[0][i] = piece('black')
            self.grid[7][i] = piece('white')

    def is_within_board(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def is_in_check(self, color):
        king_pos = None
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (i, j)
                    break
            if king_pos:
                break
        if not king_pos:
            return False
        opponent = 'black' if color == 'white' else 'white'
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece and piece.color == opponent:
                    if king_pos in piece.get_valid_moves(self, (i, j)):
                        return True
        return False

    def move_piece(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        piece = self.grid[start_x][start_y]
        if not piece:
            return False
        valid_moves = piece.get_valid_moves(self, (start_x, start_y))
        if (end_x, end_y) not in valid_moves:
            return False
        temp_board = copy.deepcopy(self)
        temp_board.grid[end_x][end_y] = temp_board.grid[start_x][start_y]
        temp_board.grid[start_x][start_y] = None
        if temp_board.is_in_check(piece.color):
            return False
        self.grid[end_x][end_y] = piece
        self.grid[start_x][start_y] = None
        if isinstance(piece, Pawn):
            piece.has_moved = True
        return True

class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'
        self.move_count = 0

    def display_board(self):
        print("  a b c d e f g h")
        for i in range(8):
            row = [str(8 - i)]
            for j in range(8):
                piece = self.board.grid[i][j]
                row.append(piece.symbol if piece else '·')
            print(' '.join(row))
        print()

    def parse_position(self, pos_str):
        if len(pos_str) != 2:
            return None
        col = pos_str[0].lower()
        row = pos_str[1]
        if not ('a' <= col <= 'h') or not row.isdigit():
            return None
        x = 8 - int(row)
        y = ord(col) - ord('a')
        if not self.board.is_within_board(x, y):
            return None
        return (x, y)

    def play(self):
        while True:
            self.display_board()
            print(f"Ход {'белых' if self.current_turn == 'white' else 'черных'}:")
            start = None
            while not start:
                start_str = input("Откуда: ")
                start = self.parse_position(start_str)
                if not start:
                    print("Некорректный ввод. Попробуйте снова.")
                    continue
                piece = self.board.grid[start[0]][start[1]]
                if not piece or piece.color != self.current_turn:
                    print("Выберите свою фигуру.")
                    start = None
            end = None
            while not end:
                end_str = input("Куда: ")
                end = self.parse_position(end_str)
                if not end:
                    print("Некорректный ввод. Попробуйте снова.")
            if self.board.move_piece(start, end):
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                self.move_count += 1
            else:
                print("Недопустимый ход!")

if __name__ == "__main__":
    game = Game()
    game.play()



class ThreatInfo:
    def __init__(self, threatened_pieces, is_check):
        self.threatened_pieces = threatened_pieces  # Список угрожаемых фигур
        self.is_check = is_check                    # Флаг наличия шаха

class Board:
    # Предполагается, что класс Board уже имеет методы для управления фигурами
    def get_pieces(self, color):
        # Возвращает все фигуры указанного цвета
        return [piece for row in self.grid for piece in row if piece and piece.color == color]

    def is_in_check(self, color):
        # Проверяет, находится ли король цвета 'color' под шахом
        king_pos = None
        for piece in self.get_pieces(color):
            if isinstance(piece, King):
                king_pos = piece.position
                break
        if not king_pos:
            return False
        # Проверяем, атакована ли позиция короля
        return self.is_square_under_attack(king_pos, color)

    def is_square_under_attack(self, position, color):
        # Проверяет, атакована ли клетка фигурами противника
        opponent_color = 'white' if color == 'black' else 'black'
        opponent_pieces = self.get_pieces(opponent_color)
        for piece in opponent_pieces:
            if position in piece.get_possible_moves(self):
                return True
        return False

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 'white'

    def get_threat_info(self):
        # Определяем цвет противника
        opponent_color = 'black' if self.current_player == 'white' else 'white'
        # Собираем все возможные ходы противника
        opponent_pieces = self.board.get_pieces(opponent_color)
        all_opponent_moves = []
        for piece in opponent_pieces:
            all_opponent_moves.extend(piece.get_possible_moves(self.board))
        # Находим фигуры текущего игрока под угрозой
        current_pieces = self.board.get_pieces(self.current_player)
        threatened_pieces = [piece for piece in current_pieces if piece.position in all_opponent_moves]
        # Проверяем шах
        is_check = self.board.is_in_check(self.current_player)
        return ThreatInfo(threatened_pieces, is_check)

    def display_board(self):
        # Визуальное отображение доски с подсветкой угроз
        threat_info = self.get_threat_info()
        for row in self.board.grid:
            for piece in row:
                if piece:
                    if piece in threat_info.threatened_pieces:
                        print(f'*{piece.symbol}*', end=' ')
                    else:
                        print(f' {piece.symbol} ', end='')
                else:
                    print(' . ', end='')
            print()
        if threat_info.is_check:
            print("Шах королю!")

class ChessPiece:
    # Базовый класс для фигур с общими методами
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def get_possible_moves(self, board):
        # Должен быть реализован в каждом подклассе
        raise NotImplementedError

class King(ChessPiece):
    # Пример реализации для короля
    def get_possible_moves(self, board):
        # Логика определения ходов короля
        moves = []
        # ... (реализация ходов короля)
        return moves

# Аналогичные классы для других фигур (Queen, Rook, Bishop, Knight, Pawn)