"""
Шахматный движок с графическим интерфейсом в консоли.

Модуль реализует:
- Все стандартные шахматные фигуры с правилами ходов
- Особые правила: рокировка, взятие на проходе, превращение пешки
- Проверку на шах и мат
- Интерактивный консольный интерфейс

Классы:
    ChessPiece: Базовый класс для всех шахматных фигур
    Pawn: Класс пешки с реализацией взятия на проходе
    Rook: Класс ладьи
    Knight: Класс коня
    Bishop: Класс слона
    Queen: Класс ферзя
    King: Класс короля с реализацией рокировки
    Board: Класс шахматной доски с логикой игры
    Game: Класс управления игровым процессом

Основной функционал:
- Отображение доски с подсветкой возможных ходов
- Проверка правильности ходов согласно шахматным правилам
- Определение шаха и запрет ходов, ведущих к шаху
- Обработка специальных ходов (рокировка, превращение пешки)
- Пошаговая игра двух игроков через консоль

Пример использования:
    game = Game()
    game.play()
"""

import copy

class ChessPiece:
    """Базовый класс для шахматных фигур.
    
    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black')
        symbol (str): Символ фигуры для отображения
        has_moved (bool): Флаг, указывающий, двигалась ли фигура
    """
    def __init__(self, color):
        """Инициализация фигуры.
        
        Args:
            color (str): Цвет фигуры ('white' или 'black')
        """
        self.color = color
        self.symbol = ''
        self.has_moved = False

    def get_symbol(self):
        """Возвращает символьное представление фигуры."""
        return self.symbol

    def get_color(self):
        """Возвращает цвет фигуры."""
        return self.color

class Pawn(ChessPiece):
    """Класс пешки с реализацией взятия на проходе."""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'P' if color == 'white' else 'p'

    def get_valid_moves(self, board, position, last_move=None):
        """Возвращает допустимые ходы для пешки.
        
        Args:
            board (Board): Текущее состояние доски
            position (tuple): Текущая позиция пешки (x, y)
            last_move (tuple): Последний сделанный ход (from_pos, to_pos)
            
        Returns:
            list: Список допустимых позиций для хода
        """
        x, y = position
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # Обычный ход и двойной ход с начальной позиции
        new_x = x + direction
        if 0 <= new_x < 8 and board.get_piece((new_x, y)) is None:
            moves.append((new_x, y))
            if x == start_row and board.get_piece((new_x + direction, y)) is None:
                moves.append((new_x + direction, y))

        # Взятие фигур
        for dy in [-1, 1]:
            if 0 <= y + dy < 8:
                target = (new_x, y + dy)
                piece = board.get_piece(target)
                if piece and piece.color != self.color:
                    moves.append(target)

        # Взятие на проходе
        if last_move:
            l_from, l_to = last_move
            l_piece = board.get_piece(l_to)
            if isinstance(l_piece, Pawn) and abs(l_from[0] - l_to[0]) == 2:
                if l_to[0] == x and l_to[1] in [y + 1, y - 1]:
                    moves.append((new_x, l_to[1]))

        return moves

class Rook(ChessPiece):
    """Класс ладьи."""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'R' if color == 'white' else 'r'

    def get_valid_moves(self, board, position, last_move=None):
        """Возвращает допустимые ходы ладьи по горизонтали и вертикали."""
        x, y = position
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x, new_y = x + dx * step, y + dy * step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = board.get_piece((new_x, new_y))
                    if not piece:
                        moves.append((new_x, new_y))
                    else:
                        if piece.color != self.color:
                            moves.append((new_x, new_y))
                        break
        return moves

class Knight(ChessPiece):
    """Класс коня с реализацией хода буквой 'Г'."""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'N' if color == 'white' else 'n'

    def get_valid_moves(self, board, position, last_move=None):
        """Возвращает допустимые ходы коня."""
        x, y = position
        moves = []
        jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                 (1, -2), (1, 2), (2, -1), (2, 1)]
        for dx, dy in jumps:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = board.get_piece((new_x, new_y))
                if not piece or piece.color != self.color:
                    moves.append((new_x, new_y))
        return moves

class Bishop(ChessPiece):
    """Класс слона с реализацией ходов по диагонали."""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'B' if color == 'white' else 'b'

    def get_valid_moves(self, board, position, last_move=None):
        """Возвращает допустимые ходы слона."""
        x, y = position
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x, new_y = x + dx * step, y + dy * step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = board.get_piece((new_x, new_y))
                    if not piece:
                        moves.append((new_x, new_y))
                    else:
                        if piece.color != self.color:
                            moves.append((new_x, new_y))
                        break
        return moves

class Queen(ChessPiece):
    """Класс ферзя, объединяющий возможности ладьи и слона."""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'Q' if color == 'white' else 'q'

    def get_valid_moves(self, board, position, last_move=None):
        """Возвращает допустимые ходы ферзя."""
        rook = Rook(self.color)
        bishop = Bishop(self.color)
        return rook.get_valid_moves(board, position) + bishop.get_valid_moves(board, position)

class King(ChessPiece):
    """Класс короля с реализацией рокировки."""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'K' if color == 'white' else 'k'

    def get_valid_moves(self, board, position, last_move=None):
        """Возвращает допустимые ходы короля, включая рокировку."""
        x, y = position
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = board.get_piece((new_x, new_y))
                if not piece or piece.color != self.color:
                    moves.append((new_x, new_y))

        # Рокировка
        if not self.has_moved:
            # Короткая рокировка (kingside)
            if board.get_piece((x, 7)) and isinstance(board.get_piece((x, 7)), Rook) and not board.get_piece((x, 7)).has_moved:
                if all(board.get_piece((x, j)) is None for j in range(y+1, 7)):
                    if not board.is_square_under_attack((x, y+1), self.color) and not board.is_square_under_attack((x, y+2), self.color):
                        moves.append((x, y+2))
            # Длинная рокировка (queenside)
            if board.get_piece((x, 0)) and isinstance(board.get_piece((x, 0)), Rook) and not board.get_piece((x, 0)).has_moved:
                if all(board.get_piece((x, j)) is None for j in range(1, y)):
                    if not board.is_square_under_attack((x, y-1), self.color) and not board.is_square_under_attack((x, y-2), self.color):
                        moves.append((x, y-2))
        return moves

class Board:
    """Класс шахматной доски, управляющий состоянием игры.
    
    Атрибуты:
        grid (list): 8x8 матрица, представляющая шахматную доску
    """
    def __init__(self, initialize=True):
        """Инициализация доски.
        
        Args:
            initialize (bool): Если True, доска инициализируется начальной расстановкой фигур
        """
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        if initialize:
            self.setup_board()

    def setup_board(self):
        """Устанавливает начальную расстановку фигур на доске."""
        # Пешки
        for i in range(8):
            self.grid[1][i] = Pawn('black')
            self.grid[6][i] = Pawn('white')
        # Остальные фигуры
        self.grid[0] = [
            Rook('black'), Knight('black'), Bishop('black'), Queen('black'),
            King('black'), Bishop('black'), Knight('black'), Rook('black')
        ]
        self.grid[7] = [
            Rook('white'), Knight('white'), Bishop('white'), Queen('white'),
            King('white'), Bishop('white'), Knight('white'), Rook('white')
        ]

    def get_piece(self, position):
        """Возвращает фигуру на указанной позиции.
        
        Args:
            position (tuple): Координаты (x, y)
            
        Returns:
            ChessPiece: Фигура на позиции или None, если клетка пуста
        """
        x, y = position
        return self.grid[x][y]

    def move_piece(self, from_pos, to_pos):
        """Перемещает фигуру на доске.
        
        Args:
            from_pos (tuple): Исходная позиция (x, y)
            to_pos (tuple): Целевая позиция (x, y)
            
        Returns:
            bool: True, если ход выполнен успешно
        """
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        piece = self.grid[from_x][from_y]
        if not piece:
            return False
        # Обработка рокировки
        if isinstance(piece, King) and abs(from_y - to_y) == 2:
            direction = 1 if to_y > from_y else -1
            rook_from = (from_x, 7 if direction == 1 else 0)
            rook_to = (from_x, to_y - direction)
            rook = self.grid[rook_from[0]][rook_from[1]]
            self.grid[rook_to[0]][rook_to[1]] = rook
            self.grid[rook_from[0]][rook_from[1]] = None
        # Перемещение фигуры
        self.grid[to_x][to_y] = piece
        self.grid[from_x][from_y] = None
        piece.has_moved = True
        return True

    def copy(self):
        """Создает глубокую копию доски.
        
        Returns:
            Board: Новая копия доски
        """
        new_board = Board(initialize=False)
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece:
                    new_piece = copy.deepcopy(piece)
                    new_board.grid[i][j] = new_piece
        return new_board

    def find_king_position(self, color):
        """Находит позицию короля заданного цвета.
        
        Args:
            color (str): Цвет короля ('white' или 'black')
            
        Returns:
            tuple: Позиция короля (x, y) или None, если король не найден
        """
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if isinstance(piece, King) and piece.color == color:
                    return (i, j)
        return None

    def is_in_check(self, color):
        """Проверяет, находится ли король под шахом.
        
        Args:
            color (str): Цвет короля ('white' или 'black')
            
        Returns:
            bool: True, если король под шахом
        """
        king_pos = self.find_king_position(color)
        if not king_pos:
            return False
        attacker_color = 'black' if color == 'white' else 'white'
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece and piece.color == attacker_color:
                    if king_pos in piece.get_valid_moves(self, (i, j)):
                        return True
        return False

    def is_square_under_attack(self, pos, color):
        """Проверяет, атакована ли клетка фигурами противника.
        
        Args:
            pos (tuple): Позиция для проверки (x, y)
            color (str): Цвет защищающегося игрока
            
        Returns:
            bool: True, если клетка под атакой
        """
        attacker_color = 'black' if color == 'white' else 'white'
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece and piece.color == attacker_color:
                    if pos in piece.get_valid_moves(self, (i, j)):
                        return True
        return False

    def display(self, highlighted=None):
        """Выводит текущее состояние доски в консоль.
        
        Args:
            highlighted (list): Список подсвечиваемых позиций (x, y)
        """
        print("  ----------------------------------")
        for i in range(8):
            print(f"{8 - i} |", end='')
            for j in range(8):
                piece = self.grid[i][j]
                if highlighted and (i, j) in highlighted:
                    print(" * |", end='')
                else:
                    symbol = piece.get_symbol() if piece else ' '
                    print(f" {symbol} |", end='')
            print("\n  ----------------------------------")
        print("    a   b   c   d   e   f   g   h")

class Game:
    """Класс управления игровым процессом.
    
    Атрибуты:
        board (Board): Шахматная доска
        current_player (str): Текущий игрок ('white' или 'black')
        move_count (int): Счетчик ходов
        last_move (tuple): Последний сделанный ход (from_pos, to_pos)
    """
    def __init__(self):
        """Инициализация новой игры."""
        self.board = Board()
        self.current_player = 'white'
        self.move_count = 0
        self.last_move = None

    def switch_player(self):
        """Переключает текущего игрока."""
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def play(self):
        """Основной игровой цикл."""
        while True:
            self.board.display()
            print(f"Ход {'белых' if self.current_player == 'white' else 'черных'}")
            from_pos = self.get_position("Выберите фигуру (например, a2): ")
            if not from_pos:
                continue
            piece = self.board.get_piece(from_pos)
            if not piece or piece.color != self.current_player:
                print("Выберите свою фигуру!")
                continue

            valid_moves = piece.get_valid_moves(self.board, from_pos, self.last_move)
            valid_moves = self.filter_self_checks(from_pos, valid_moves)
            if not valid_moves:
                print("Нет допустимых ходов для этой фигуры!")
                continue

            self.board.display(highlighted=valid_moves)
            to_pos = self.get_position("Куда походим? (например, a4): ")
            if to_pos not in valid_moves:
                print("Недопустимый ход!")
                continue

            self.execute_move(from_pos, to_pos, piece)
            self.switch_player()
            self.move_count += 1

    def filter_self_checks(self, from_pos, valid_moves):
        """Фильтрует ходы, которые оставляют короля под шахом.
        
        Args:
            from_pos (tuple): Исходная позиция фигуры
            valid_moves (list): Список возможных ходов
            
        Returns:
            list: Отфильтрованный список допустимых ходов
        """
        filtered = []
        for move in valid_moves:
            temp_board = self.board.copy()
            temp_board.move_piece(from_pos, move)
            if not temp_board.is_in_check(self.current_player):
                filtered.append(move)
        return filtered

    def execute_move(self, from_pos, to_pos, piece):
        """Выполняет ход, включая специальные правила.
        
        Args:
            from_pos (tuple): Исходная позиция
            to_pos (tuple): Целевая позиция
            piece (ChessPiece): Перемещаемая фигура
        """
        # Взятие на проходе
        if isinstance(piece, Pawn) and to_pos[1] != from_pos[1] and self.board.get_piece(to_pos) is None:
            captured_pawn_pos = (from_pos[0], to_pos[1])
            self.board.grid[captured_pawn_pos[0]][captured_pawn_pos[1]] = None

        self.board.move_piece(from_pos, to_pos)
        self.last_move = (from_pos, to_pos)

        # Превращение пешки
        if isinstance(piece, Pawn) and (to_pos[0] == 0 or to_pos[0] == 7):
            self.promote_pawn(to_pos)

    def promote_pawn(self, pos):
        """Превращает пешку в выбранную фигуру.
        
        Args:
            pos (tuple): Позиция пешки для превращения
        """
        while True:
            choice = input("Выберите фигуру (Q, R, B, N): ").upper()
            if choice == 'Q':
                new_piece = Queen(self.current_player)
            elif choice == 'R':
                new_piece = Rook(self.current_player)
            elif choice == 'B':
                new_piece = Bishop(self.current_player)
            elif choice == 'N':
                new_piece = Knight(self.current_player)
            else:
                print("Неверный выбор!")
                continue
            self.board.grid[pos[0]][pos[1]] = new_piece
            break

    def get_position(self, prompt):
        """Запрашивает и преобразует ввод позиции от пользователя.
        
        Args:
            prompt (str): Приглашение для ввода
            
        Returns:
            tuple: Координаты позиции (x, y) или None при неверном вводе
        """
        while True:
            pos_str = input(prompt).strip().lower()
            if len(pos_str) != 2:
                print("Неверный формат!")
                continue
            col, row = pos_str[0], pos_str[1]
            if not col.isalpha() or not row.isdigit():
                print("Неверный формат!")
                continue
            x = 8 - int(row)
            y = ord(col) - ord('a')
            if 0 <= x < 8 and 0 <= y < 8:
                return (x, y)
            else:
                print("Позиция вне доски!")

if __name__ == "__main__":
    game = Game()
    game.play()
