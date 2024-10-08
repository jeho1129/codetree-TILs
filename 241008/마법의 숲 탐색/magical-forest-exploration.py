from collections import deque

dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]


def BFS(y, x):
    count = y
    queue = deque([(y, x)])
    visited = [[False] * C for _ in range(R + 3)]
    visited[y][x] = True
    while queue:
        y1, x1 = queue.popleft()
        for i in range(4):
            new_y, new_x = y1 + dy[i], x1 + dx[i]
            if 0 <= new_x < C and 3 <= new_y < R + 3:
                if (graph[new_y][new_x] == graph[y1][x1] or (graph[new_y][new_x] != 0 and out[y1][x1] != 0)):
                    if not visited[new_y][new_x]:
                        visited[new_y][new_x] = True
                        count = max(count, new_y)
                        queue.append((new_y, new_x))
    return count


def down(y, x, d, n):
    global graph
    global out
    if check1(y + 1, x):
        down(y + 1, x, d, n)
    elif check2(y, x - 1):
        down(y + 1, x - 1, (d + 3) % 4, n)
    elif check2(y, x + 1):
        down(y + 1, x + 1, (d + 1) % 4, n)
    else:
        if y - 1 < 3 or y + 1 >= R + 3 or x - 1 < 0 or x + 1 >= C:
            graph = [[0] * C for i in range(R + 3)]
            out = [[0] * C for i in range(R + 3)]
        else:
            graph[y][x] = n
            for i in range(4):
                if d == i:
                    out[y + dy[i]][x + dx[i]] = 1
                graph[y + dy[i]][x + dx[i]] = n
            global result
            result += BFS(y, x) - 3 + 1


def check1(y, x):
    if x - 1 < 0 or x + 1 >= C or y + 1 >= R + 3:
        return False
    for i in range(4):
        if graph[y + dy[i]][x + dx[i]] != 0:
            return False
    else:
        if graph[y][x] != 0:
            return False
        else:
            return True


def check2(y, x):
    if x - 1 < 0 or x + 1 >= C or y + 2 >= R + 3:
        return False
    for i in range(4):
        if graph[y + dy[i]][x + dx[i]] != 0:
            return False
    for i in range(4):
        if graph[y + 1 + dy[i]][x + dx[i]] != 0:
            return False
    else:
        return True


R, C, K = map(int, input().split())
graph = [[0] * C for i in range(R + 3)]
out = [[0] * C for i in range(R + 3)]
result = 0
for i in range(K):
    c, d = map(int, input().split())
    down(1, c - 1, d, i + 1)
print(result)