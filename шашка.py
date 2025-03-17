from abc import ABC, abstractmethod

class CheckersPiece(ABC):
    def __init__(self, color):
        self.color = color
        self.symbol = '●' if color == 'white' else '○'
        self.is_king = False

    @abstractmethod
    def get_valid_moves(self, board, position):
        pass

class RegularChecker(CheckersPiece):
    def get_valid_moves(self, board, position):
        x, y = position
        moves = []
        capture_moves = []
        directions = [(-1, -1), (-1, 1)] if self.color == 'white' else [(1, -1), (1, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if board.is_within_board(nx, ny):
                if not board.grid[nx][ny]:
                    moves.append((nx, ny))
                elif board.grid[nx][ny].color != self.color:
                    nx2, ny2 = nx + dx, ny + dy
                    if board.is_within_board(nx2, ny2) and not board.grid[nx2][ny2]:
                        capture_moves.append((nx2, ny2))
        
        return {'moves': moves, 'captures': capture_moves}

class KingChecker(RegularChecker):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '◎' if color == 'white' else '◉'
        self.is_king = True

    def get_valid_moves(self, board, position):
        moves = super().get_valid_moves(board, position)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dx, dy in directions:
            nx, ny = position[0] + dx, position[1] + dy
            if board.is_within_board(nx, ny) and not board.grid[nx][ny]:
                moves['moves'].append((nx, ny))
        
        return moves

class CheckersBoard:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.init_board()

    def init_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.grid[row][col] = RegularChecker('black')
                    elif row > 4:
                        self.grid[row][col] = RegularChecker('white')

    def is_within_board(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def move_piece(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        piece = self.grid[start_x][start_y]
        
        if not piece:
            return False
        
        valid_moves = piece.get_valid_moves(self, start)
        
        if end in valid_moves['moves']:
            self.grid[end_x][end_y] = piece
            self.grid[start_x][start_y] = None
            self.check_promotion(end)
            return True
        
        if end in valid_moves['captures']:
            captured_x = (start_x + end_x) // 2
            captured_y = (start_y + end_y) // 2
            self.grid[end_x][end_y] = piece
            self.grid[start_x][start_y] = None
            self.grid[captured_x][captured_y] = None
            self.check_promotion(end)
            return True
        
        return False

    def check_promotion(self, position):
        x, y = position
        piece = self.grid[x][y]
        if not piece.is_king:
            if (piece.color == 'white' and x == 0) or (piece.color == 'black' and x == 7):
                self.grid[x][y] = KingChecker(piece.color)

class CheckersGame:
    def __init__(self):
        self.board = CheckersBoard()
        self.current_turn = 'white'
        self.selected_piece = None

    def display_board(self):
        print("  0 1 2 3 4 5 6 7")
        for row in range(8):
            line = [str(row)]
            for col in range(8):
                piece = self.board.grid[row][col]
                if (row + col) % 2 == 0:
                    line.append(' ')
                else:
                    line.append(piece.symbol if piece else '·')
            print(' '.join(line))
        print()

    def parse_input(self, input_str):
        try:
            x, y = map(int, input_str.split())
            return (x, y)
        except:
            return None

    def play(self):
        while True:
            self.display_board()
            print(f"Ход {'белых' if self.current_turn == 'white' else 'черных'}:")
            
            start = None
            while not start:
                start_str = input("Выберите фигуру (ряд столбец): ")
                start = self.parse_input(start_str)
                if start and self.board.grid[start[0]][start[1]] and \
                   self.board.grid[start[0]][start[1]].color == self.current_turn:
                    break
                print("Некорректный выбор")
                start = None
            
            end = None
            while not end:
                end_str = input("Куда ходим: ")
                end = self.parse_input(end_str)
                if end:
                    break
                print("Некорректный ввод")
            
            if self.board.move_piece(start, end):
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            else:
                print("Недопустимый ход!")

if __name__ == "__main__":
    game = CheckersGame()
    game.play()