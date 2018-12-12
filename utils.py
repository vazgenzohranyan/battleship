import numpy as np


def find_neighbour(pos, board):
        i,j = pos
        for n in range(i - 1, i + 2):
                for m in range(j - 1, j + 2):
                        if m in range(10) and n in range(10) and [i, j] != [n, m]:
                                if board[n][m] == 1:
                                        return False
        return True

def find_available_positions(length, vertical, board):
        positions = []
        if vertical:
                for i,raw in enumerate(board):
                        for j,p in enumerate(raw):
                                if p == 0:
                                        pos = []
                                        for k in range(length):
                                                if (i+k) in range(10):
                                                        if board[i+k][j]==0 and find_neighbour([i+k,j], board):
                                                             pos.append([i+k,j])
                                                        elif board[i+k][j] == 1 or find_neighbour([i+k,j], board) is False:
                                                             pos = None
                                                             break
                                        if pos is not None:
                                                positions.append(pos)
        else:
                for i,raw in enumerate(board):
                        for j,p in enumerate(raw):
                                if p == 0:
                                        pos = []
                                        for k in range(length):
                                                if (j+k) in range(10):
                                                        if board[i][j+k]==0 and find_neighbour([i,j+k],board):
                                                             pos.append([i,j+k])
                                                        elif board[i][j+k] == 1 or find_neighbour([i,j+k],board) is False:
                                                             pos = None
                                                             break
                                        if pos is not None:
                                                positions.append(pos)
        return positions

def set(length, board):
        vertical = np.random.randint(0, 2)
        positions = find_available_positions(length, vertical, board)
        if len(positions) == 0:
                generate_board()
        coord = positions[np.random.randint(0, len(positions))]
        place_ship(coord,board)

def place_ship(coord,board):
        for p in coord:
                board[p[0]][p[1]] = 1

def generate_board():
        board = np.zeros((10, 10))

        ships = {
                '4': 1,
                '3': 2,
                '2': 3,
                '1': 4
        }
        for ship in ships:
                length = int(ship)
                for _ in range(ships[ship]):
                        set(length, board)

        return board

