from collections import deque

def moving_r():
    num_c, distance_c = N, N ** 3
    # 루돌프와 각 산타 간 거리 재기
    for j in range(len(c)):
        if c[j][3] > 0:
            c[j][3] -= 1
        distance = (r[0] - c[j][0]) ** 2 + (r[1] - c[j][1]) ** 2
        if distance < distance_c:
            num_c = j
            distance_c = distance
        elif distance == distance_c:
            if c[j][0] > c[num_c][0] or (c[j][0] == c[num_c][0] and c[j][1] > c[num_c][1]):
                num_c = j
                distance_c = distance
    # 가까운 산타에게 돌진하기
    if c[num_c][0] > r[0]:
        r[0] += 1
        if c[num_c][1] > r[1]:
            r[1] += 1
            direction = 7
        elif c[num_c][1] < r[1]:
            r[1] -= 1
            direction = 6
        else:
            direction = 2
    elif c[num_c][0] == r[0]:
        if c[num_c][1] > r[1]:
            r[1] += 1
            direction = 1
        else:
            r[1] -= 1
            direction = 3
    else:
        r[0] -= 1
        if c[num_c][1] > r[1]:
            r[1] += 1
            direction = 5
        elif c[num_c][1] < r[1]:
            r[1] -= 1
            direction = 4
        else:
            direction = 0
    # 산타와 루돌프가 충돌할 경우
    for j in range(len(c)):
        x = c.popleft()
        if x[0] == r[0] and x[1] == r[1]:
            result[x[2] - 1] += C
            x[3] = 2
            x[0] += dy[direction] * C
            x[1] += dx[direction] * C
            if 0 < x[0] <= N and 0 < x[1] <= N:
                check_c(x[0], x[1], direction, len(c))
                c.append(x)
            else:
                break
        else:
            c.append(x)


def check_c(y, x, direction, n):
    if n == 1:
        return
    for _ in range(n):
        t = c.popleft()
        if t[0] == y and t[1] == x:
            t[0] += dy[direction]
            t[1] += dx[direction]
            if 0 < t[0] <= N and 0 < t[1] <= N:
                c.append(t)
                check_c(t[0], t[1], direction, n - 1)
            else:
                return
        else:
            c.append(t)


def moving_c():
    global graph
    for i in range(len(c)):
        x = c.popleft()
        if x[3] > 0:
            c.append(x)
            continue
        # 가장 가까운 거리를 계산
        min_dis = (r[0] - x[0]) ** 2 + (r[1] - x[1]) ** 2
        min_dir = 4
        for j in range(4):
            if 0 <= x[0] + dy[j] - 1 < N and 0 <= x[1] + dx[j] - 1 < N:
                if graph[x[0] + dy[j] - 1][x[1] + dx[j] - 1] == 0:
                    dis = (r[0] - (x[0] + dy[j])) ** 2 + (r[1] - (x[1] + dx[j])) ** 2
                    if dis < min_dis:
                        min_dis = dis
                        min_dir = j
        if min_dir < 4:
            graph[x[0] - 1][x[1] - 1] = 0
            x[0] += dy[min_dir]
            x[1] += dx[min_dir]
            if x[0] == r[0] and x[1] == r[1]:
                result[x[2] - 1] += D
                x[3] = 2
                x[0] += -dy[min_dir] * D
                x[1] += -dx[min_dir] * D
                if 0 < x[0] <= N and 0 < x[1] <= N:
                    check_c(x[0], x[1], (min_dir + 2) % 4, len(c))
                    c.append(x)
                    graph = [[0] * N for _ in range(N)]
                    for k in range(len(c)):
                        p = c[k]
                        graph[p[0] - 1][p[1] - 1] = 1
            else:
                c.append(x)
                graph[x[0] - 1][x[1] - 1] = 1
        else:
            c.append(x)

dy, dx = [-1, 0, 1, 0, -1, -1, 1, 1], [0, 1, 0, -1, -1, 1, -1, 1]

N, M, P, C, D = map(int, input().split())
r = list(map(int, input().split()))
c = deque()
for i in range(P):
    cn, cy, cx = map(int, input().split())
    c.append([cy, cx, cn, 0])
result = [0] * P  # 최종 점수
for i in range(M):
    if len(c) == 0:
        break
    moving_r()
    c = deque(sorted(c, key=lambda x: x[2]))
    graph = [[0] * N for _ in range(N)]
    for j in range(len(c)):
        x = c[j]
        graph[x[0] - 1][x[1] - 1] = 1
    moving_c()
    c = deque(sorted(c, key=lambda x: x[2]))
    for j in range(len(c)):
        x = c[j]
        result[x[2] - 1] += 1
print(*result)