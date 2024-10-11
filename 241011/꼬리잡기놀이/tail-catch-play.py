from collections import deque

dy, dx = [0, -1, 0, 1], [1, 0, -1, 0]


def BFS(n, i, j):
    queue = deque([(i, j)])
    visited = [[False] * N for _ in range(N)]
    visited[i][j] = True
    while queue:
        y, x = queue.popleft()
        for k in range(4):
            new_y, new_x = y + dy[k], x + dx[k]
            if 0 <= new_y < N and 0 <= new_x < N:
                if not visited[new_y][new_x] and graph_info[new_y][new_x] == 0 and graph[new_y][new_x] != 0:
                    visited[new_y][new_x] = True
                    graph_info[new_y][new_x] = n
                    queue.append((new_y, new_x))


def BFS_2(n, i, j):
    queue = deque([(i, j)])
    visited = [[False] * N for _ in range(N)]
    visited[i][j] = True
    while queue:
        y, x = queue.popleft()
        for k in range(4):
            new_y, new_x = y + dy[k], x + dx[k]
            if 0 <= new_y < N and 0 <= new_x < N:
                if not visited[new_y][new_x] and graph_info[new_y][new_x] == n:
                    if 2 <= graph[new_y][new_x]:
                        visited[new_y][new_x] = True
                        queue.append((new_y, new_x))
                        if 2 <= graph[new_y][new_x] <= 3:
                            team_info[n - 1].append((new_y, new_x))
                            if graph[new_y][new_x] == 3:
                                return


def move(n):
    y, x = team_info[n][0]
    for i in range(4):
        new_y, new_x = y + dy[i], x + dx[i]
        if 0 <= new_y < N and 0 <= new_x < N:
            if graph[new_y][new_x] == 4 and graph_info[new_y][new_x] == n + 1:
                graph[new_y][new_x] = 1
                y1, x1 = team_info[n].pop()
                graph[y1][x1] = 4
                for j in range(len(team_info[n])):
                    y2, x2 = team_info[n][j]
                    if j == len(team_info[n]) - 1:
                        graph[y2][x2] = 3
                    else:
                        graph[y2][x2] = 2
                team_info[n].appendleft((new_y, new_x))


def ball1(n):
    global result
    for i in range(N):
        # 해당 궤적에 최초에 만나는 사람
        if 1 <= graph[n][i] <= 3:
            team_number = graph_info[n][i] - 1
            # 해당 사람이 머리 사람을 시작으로 팀 내에서 몇 번째인 지?
            team_index = team_info[team_number].index((n, i)) + 1
            # K번째 사람이라면 K의 제곱만큼 점수를 추가
            result += team_index ** 2
            return team_number


def ball2(n):
    global result
    for i in range(N - 1, -1, -1):
        if 1 <= graph[i][n] <= 3:
            team_number = graph[i][n] - 1
            team_index = team_info[team_number].index((i, n)) + 1
            result += team_index ** 2
            return team_number


def ball3(n):
    global result
    for i in range(N - 1, -1, -1):
        if 1 <= graph[N - 1 - n][i] <= 3:
            team_number = graph[N - 1 - n][i] - 1
            team_index = team_info[team_number].index((N - 1 - n, i)) + 1
            result += team_index ** 2
            return team_number


def ball4(n):
    global result
    for i in range(N):
        if 1 <= graph[N - 1 - n][i] <= 3:
            team_number = graph[N - 1 - n][i] - 1
            team_index = team_info[team_number].index((N - 1 - n, i)) + 1
            result += team_index ** 2
            return team_number


N, M, K = map(int, input().split())  # 격자의 크기 N, 팀의 개수 M, 라운드 수 K
graph = [list(map(int, input().split())) for _ in range(N)]
graph_info = [[0] * N for _ in range(N)]
team_info = deque([deque([]) for _ in range(M)])
result = 0
n = 1
for i in range(N):
    for j in range(N):
        if graph[i][j] != 0 and graph_info[i][j] == 0:
            graph_info[i][j] = n
            BFS(n, i, j)
            n += 1
for i in range(N):
    for j in range(N):
        if graph[i][j] == 1:
            team_info[graph_info[i][j] - 1].append((i, j))
            BFS_2(graph_info[i][j], i, j)
for i in range(1, K + 1):
    # 각 팀은 머리 사람을 따라서 한 칸 이동
    for j in range(M):
        move(j)

    # 각 라운드마다 공이 정해진 선을 따라 던져짐
    i = i % (4 * N)
    if 0 < i <= N:
        number = ball1(i - 1)
    elif i <= 2 * N:
        number = ball2(i - (N + 1))
    elif i <= 3 * N:
        number = ball3(i - (2 * N + 1))
    else:
        if i == 0:
            i = 4 * N
        number = ball4(i - (3 * N + 1))

    team_info[number].reverse()
    for i in range(len(team_info[number])):
        y, x = team_info[number][i]
        if i == 0:
            graph[y][x] = 1
        elif i < len(team_info[number]) - 1:
            graph[y][x] = 2
        else:
            graph[y][x] = 3
print(result)