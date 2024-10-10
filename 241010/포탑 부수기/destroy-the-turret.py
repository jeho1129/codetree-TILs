def select():
    # 공격자의 공격력, 열, 행 저장
    a1, y1, x1 = 5001, 0, 0
    # 공격당하는 자의 공격력, 열, 행 저장
    a2, y2, x2 = 0, 0, 0
    for i in range(N):
        for j in range(M):
            if graph[i][j] != 0:
                if graph[i][j] < a1:
                    a1, y1, x1 = graph[i][j], i, j
                elif graph[i][j] == a1:
                    if attack[i][j] > attack[y1][x1]:
                        a1, y1, x1 = graph[i][j], i, j
                    elif attack[i][j] == attack[y1][x1]:
                        if i + j > y1 + x1 or (i + j == y1 + x1 and j > x1):
                            a1, y1, x1 = graph[i][j], i, j
            if graph[i][j] > a2:
                a2, y2, x2 = graph[i][j], i, j
            elif graph[i][j] == a2:
                if attack[i][j] < attack[y2][x2]:
                    a2, y2, x2 = graph[i][j], i, j
                elif attack[i][j] == attack[y2][x2]:
                    if i + j < y2 + x2 or (i + j == y2 + x2 and j < x2):
                        a2, y2, x2 = graph[i][j], i, j

    return y1, x1, y2, x2


def attack1(a, b, c, d):
    queue = deque([[a, b]])
    visited = [[False] * M for _ in range(N)]
    visited[a][b] = True
    path = [[None] * M for _ in range(N)]
    while queue:
        y1, x1 = queue.popleft()
        if y1 == c and x1 == d:
            real_path = []
            while True:
                if path[y1][x1] == (a, b):
                    break
                real_path.append(path[y1][x1])
                y1, x1 = path[y1][x1]
            return real_path
        for i in range(4):
            new_y, new_x = y1 + dy[i], x1 + dx[i]
            if new_y < 0:
                new_y = N - 1
            elif new_y >= N:
                new_y = new_y - N
            if new_x < 0:
                new_x = M - 1
            elif new_x >= M:
                new_x = new_x - M
            if not visited[new_y][new_x] and graph[new_y][new_x] != 0:
                visited[new_y][new_x] = True
                path[new_y][new_x] = (y1, x1)
                queue.append([new_y, new_x])
    return None


def attack2(a, b, c, d):
    path = []
    for i in range(8):
        new_y, new_x = c + dy[i], d + dx[i]
        if new_y < 0:
            new_y = N - 1
        elif new_y >= N:
            new_y = new_y - N
        if new_x < 0:
            new_x = M - 1
        elif new_x >= M:
            new_x = new_x - M
        if new_y == a and new_x == b:
            continue
        elif graph[new_y][new_x] != 0:
            graph[new_y][new_x] -= graph[a][b] // 2
            path.append((new_y, new_x))
            if graph[new_y][new_x] < 0:
                graph[new_y][new_x] = 0
    graph[c][d] -= graph[a][b]
    if graph[c][d] < 0:
        graph[c][d] = 0
    return path


N, M, K = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
attack = [[0] * M for _ in range(N)]
for t in range(K):
    count = 0
    # 부서지지 않은 포탑이 1개일 경우 즉시 중지
    for i in range(N):
        count += graph[i].count(0)
    if count == N * M - 1:
        break
    # 공격자, 공격당할 자 선정
    attack_y, attack_x, attacked_y, attacked_x = select()
    # 해당 공격자의 공격력 증가
    graph[attack_y][attack_x] += (N + M)
    attack[attack_y][attack_x] = t + 1
    # 레이저 공격 시도
    if attack1(attack_y, attack_x, attacked_y, attacked_x) is not None:
        result = attack1(attack_y, attack_x, attacked_y, attacked_x)
        for i in range(len(result)):
            y, x = result[i]
            graph[y][x] -= graph[attack_y][attack_x] // 2
            if graph[y][x] < 0:
                graph[y][x] = 0
        graph[attacked_y][attacked_x] -= graph[attack_y][attack_x]
        if graph[attacked_y][attacked_x] < 0:
            graph[attacked_y][attacked_x] = 0
    # 포탑 공격 시도
    else:
        result = attack2(attack_y, attack_x, attacked_y, attacked_x)
    result = result + [(attack_y, attack_x), (attacked_y, attacked_x)]
    # 공격 후 포탑 정비
    for i in range(N):
        for j in range(M):
            if graph[i][j] != 0 and (i, j) not in result:
                graph[i][j] += 1

score = 0
for i in range(N):
    for j in range(M):
        if graph[i][j] > score:
            score = graph[i][j]
print(score)