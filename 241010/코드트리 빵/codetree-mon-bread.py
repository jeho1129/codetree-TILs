from collections import deque
dy, dx = [-1, 0, 0, 1], [0, -1, 1, 0]


def basecamp(time):
    wanted_store = store[time - 1]
    a, b, c = N ** 3, 0, 0
    for i in range(N):
        for j in range(N):
            if base_info[i][j] == 1:
                queue = deque([[i, j]])
                visited = [[0] * N for _ in range(N)]
                visited[i][j] = 1
                while queue:
                    y, x = queue.popleft()
                    if y == wanted_store[0] - 1 and x == wanted_store[1] - 1:
                        break
                    for k in range(4):
                        new_y, new_x = y + dy[k], x + dx[k]
                        if 0 <= new_y < N and 0 <= new_x < N:
                            if visited[new_y][new_x] == 0 and graph[new_y][new_x] == 0:
                                visited[new_y][new_x] = visited[y][x] + 1
                                queue.append([new_y, new_x])
                if 0 < visited[wanted_store[0] - 1][wanted_store[1] - 1] < a:
                    a, b, c = visited[wanted_store[0] - 1][wanted_store[1] - 1], i, j
    base_info[b][c] = 0
    graph[b][c] = time
    graph[wanted_store[0] - 1][wanted_store[1] - 1] = -time
    person[time - 1] = [b, c, 0]


def move(n, y, x):
    count, dir_y, dir_x = N ** 3, 0, 0
    for i in range(4):
        new_y, new_x = y + dy[i], x + dx[i]
        if 0 <= new_y < N and 0 <= new_x < N:
            if graph[new_y][new_x] == -(n + 1):
                person[n] = [new_y, new_x, 1]
                graph[new_y][new_x] = n + 1
                break
            if graph[new_y][new_x] <= 0 or graph[new_y][new_x] == n + 1:
                queue = deque([[new_y, new_x]])
                visited = [[0] * N for _ in range(N)]
                visited[new_y][new_x] = 1
                while queue:
                    y1, x1 = queue.popleft()
                    if graph[y1][x1] == -(n + 1):
                        break
                    for k in range(4):
                        y2, x2 = y1 + dy[k], x1 + dx[k]
                        if 0 <= y2 < N and 0 <= x2 < N:
                            if visited[y2][x2] == 0 and (graph[y2][x2] <= 0 or graph[y2][x2] == n + 1):
                                visited[y2][x2] = visited[y1][x1] + 1
                                queue.append([y2, x2])
                if visited[store[n][0] - 1][store[n][1] - 1] < count:
                    count = visited[store[n][0] - 1][store[n][1] - 1]
                    dir_y, dir_x = new_y, new_x
    else:
        person[n] = [dir_y, dir_x, 0]


N, M = map(int, input().split())  # 격자의 크기 N / 사람의 수 M
base_info = [list(map(int, input().split())) for _ in range(N)]
# 움직일 수 없는 곳을 표시
graph = [[0] * N for _ in range(N)]
# 사람이 있는 곳을 표시
person = [[-1, -1, 0] for _ in range(M)]
store = [list(map(int, input().split())) for _ in range(M)]
result = [False] * M
t = 1
while True:
    # 격자에 있는 사람이 편의점 방향을 향해서 1칸 움직이기
    for i in range(M):
        if person[i][0] != -1 and person[i][2] != 1:
            move(i, person[i][0], person[i][1])

    # M분보다 시간이 적을 때는 사람을 베이스캠프에 배정해야 함.
    if t <= M:
        basecamp(t)

    # 모든 사람이 도착하면 탈출
    count = 0
    for i in range(M):
        if person[i][2] == 1:
            count += 1
    if count == M:
        break
    else:
        t += 1
print(t)