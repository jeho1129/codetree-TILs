import copy
from collections import deque


def in_range(y, x):
    return 0 <= y < 5 and 0 <= x < 5


def rotate(board, sy, sx, cnt):
    result = copy.deepcopy(board)
    for _ in range(cnt):
        tmp = result[sy + 0][sx + 2]
        result[sy + 0][sx + 2] = result[sy + 0][sx + 0]
        result[sy + 0][sx + 0] = result[sy + 2][sx + 0]
        result[sy + 2][sx + 0] = result[sy + 2][sx + 2]
        result[sy + 2][sx + 2] = tmp
        tmp = result[sy + 1][sx + 2]
        result[sy + 1][sx + 2] = result[sy + 0][sx + 1]
        result[sy + 0][sx + 1] = result[sy + 1][sx + 0]
        result[sy + 1][sx + 0] = result[sy + 2][sx + 1]
        result[sy + 2][sx + 1] = tmp

    return result


def cal_score(board):
    score = 0
    visit = [[False for _ in range(5)] for _ in range(5)]
    dy, dx = [0, 1, 0, -1], [1, 0, -1, 0]

    for i in range(5):
        for j in range(5):
            if not visit[i][j]:
                q, trace = deque([(i, j)]), deque([(i, j)])
                visit[i][j] = True
                while q:
                    cur = q.popleft()
                    for k in range(4):
                        ny, nx = cur[0] + dy[k], cur[1] + dx[k]
                        if in_range(ny, nx) and board[ny][nx] == board[cur[0]][cur[1]] and not visit[ny][nx]:
                            q.append((ny, nx))
                            trace.append((ny, nx))
                            visit[ny][nx] = True
                if len(trace) >= 3:
                    score += len(trace)
                    while trace:
                        t = trace.popleft()
                        board[t[0]][t[1]] = 0
    return score


def fill(board, que):
    for j in range(5):
        for i in reversed(range(5)):
            if board[i][j] == 0:
                board[i][j] = que.popleft()


def treasure_hunt(K, M, initial_board, wall_pieces):
    board = copy.deepcopy(initial_board)
    q = deque(wall_pieces)
    results = []

    for _ in range(K):
        maxScore = 0
        maxScoreBoard = None

        for cnt in range(1, 4):
            for sx in range(3):
                for sy in range(3):
                    rotated = rotate(board, sy, sx, cnt)
                    score = cal_score(rotated)
                    if maxScore < score:
                        maxScore = score
                        maxScoreBoard = rotated

        if maxScoreBoard is None:
            break

        board = maxScoreBoard

        while True:
            fill(board, q)
            newScore = cal_score(board)
            if newScore == 0:
                break
            maxScore += newScore

        results.append(maxScore)

    return results


K, M = map(int, input().split())
initial_board = [list(map(int, input().split())) for _ in range(5)]
wall_pieces = list(map(int, input().split()))

results = treasure_hunt(K, M, initial_board, wall_pieces)

print(*results)