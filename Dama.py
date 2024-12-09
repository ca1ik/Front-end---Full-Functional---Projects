import copy
import random

# Tahta boyutu ve taşların hedef alanı
BOARD_SIZE = 8
TARGET_AREA_B = {(5, 5), (5, 6), (5, 7), (6, 5), (6, 6), (6, 7), (7, 5), (7, 6), (7, 7)}
TARGET_AREA_S = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}

# Tahta oluşturma
def create_board():
    board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for x in range(3):
        for y in range(3):
            board[x][y] = 'S'  # Siyah taşlar
            board[BOARD_SIZE-1-x][BOARD_SIZE-1-y] = 'B'  # Beyaz taşlar
    return board

# Tahtayı yazdırma
def print_board(board):
    for row in board:
        print(" ".join(row))
    print("\n")

# Geçerli hareketleri bulma
def valid_moves(board, x, y):
    moves = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Dört yönlü hareket
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == '.':
            moves.append((nx, ny))
        # Atlama hareketleri
        if 0 <= nx + dx < BOARD_SIZE and 0 <= ny + dy < BOARD_SIZE:
            if board[nx][ny] != '.' and board[nx + dx][ny + dy] == '.':
                moves.append((nx + dx, ny + dy))
    return moves

# Oyuncunun tahtadaki tüm hareketlerini oluşturma
def generate_all_moves(board, player):
    moves = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == player:
                for move in valid_moves(board, x, y):
                    moves.append(((x, y), move))
    return moves

# Hareketi tahtaya uygula
def apply_move(board, move, player):
    (x, y), (nx, ny) = move
    new_board = copy.deepcopy(board)
    new_board[x][y] = '.'
    new_board[nx][ny] = player
    return new_board

# Oyunun bitip bitmediğini kontrol eden fonksiyon
def game_over(board):
    # Beyaz taşlar hedefe ulaştı mı?
    white_in_target = all(board[x][y] == 'B' for x, y in TARGET_AREA_B)
    # Siyah taşlar hedefe ulaştı mı?
    black_in_target = all(board[x][y] == 'S' for x, y in TARGET_AREA_S)
    return white_in_target or black_in_target

# Sezgi fonksiyonu (taşların hedefe yakınlığına göre skor)
def heuristic(board, player):
    target_area = TARGET_AREA_B if player == 'B' else TARGET_AREA_S
    opponent = 'S' if player == 'B' else 'B'
    score = 0
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == player:
                score -= min(abs(x - tx) + abs(y - ty) for tx, ty in target_area)
            elif board[x][y] == opponent:
                score += min(abs(x - tx) + abs(y - ty) for tx, ty in target_area)
    return score

# Mini-Max algoritması
def minimax(board, depth, maximizing_player, alpha, beta, player):
    if depth == 0 or game_over(board):
        return heuristic(board, player), None

    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in generate_all_moves(board, player):
            new_board = apply_move(board, move, player)
            eval_score, _ = minimax(new_board, depth-1, False, alpha, beta, 'S' if player == 'B' else 'B')
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in generate_all_moves(board, player):
            new_board = apply_move(board, move, player)
            eval_score, _ = minimax(new_board, depth-1, True, alpha, beta, 'S' if player == 'B' else 'B')
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

# Oyun simülasyonu
def simulate_games():
    scores = {"B": 0, "S": 0}
    for game in range(5):
        print(f"Game {game + 1}")
        board = create_board()
        print_board(board)
        current_player = 'B'
        while not game_over(board):
            _, move = minimax(board, 3, True, float('-inf'), float('inf'), current_player)
            if move is None:
                break  # Hareket kalmadıysa çık
            board = apply_move(board, move, current_player)
            print_board(board)
            current_player = 'S' if current_player == 'B' else 'B'
        if all(board[x][y] == 'B' for x, y in TARGET_AREA_B):
            print("Beyaz kazandı!\n")
            scores["B"] += 1
        elif all(board[x][y] == 'S' for x, y in TARGET_AREA_S):
            print("Siyah kazandı!\n")
            scores["S"] += 1
    print("Skorlar:", scores)

# Simülasyonu başlat
simulate_games()
