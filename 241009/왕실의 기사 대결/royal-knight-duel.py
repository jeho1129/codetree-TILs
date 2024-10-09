from collections import deque


def change(x, n, d, z):
    for i in range(x[2]):
        for j in range(x[3]):
            knight[i + x[0] - 1][j + x[1] - 1] = 0
    x[0], x[1] = x[0] + dy[d], x[1] + dx[d]
    for i in range(x[2]):
        for j in range(x[3]):
            knight[i + x[0] - 1][j + x[1] - 1] = n
            if z == 1 and chess[i + x[0] - 1][j + x[1] - 1] == 1:
                knight_info[n - 1][4] -= 1
                if knight_info[n - 1][4] == 0:
                    break
    if knight_info[n - 1][4] == 0:
        for i in range(x[2]):
            for j in range(x[3]):
                knight[i + x[0] - 1][j + x[1] - 1] = 0


def moving(n, d):
    # 해당 기사의 범위만큼 이동하려는 위치에 뭐가 있는 지 조사
    x = knight_info[n - 1]  # r, c, h, w, k
    others = deque([])
    # 위로 이동할 경우
    if d == 0:
        for i in range(x[3]):
            new_y, new_x = x[0] + dy[0] - 1, x[1] + i + dx[0] - 1
            if 0 <= new_y < L and 0 <= new_x < L:
                # 이동하려는 위치에 아무도 없을 경우
                if knight[new_y][new_x] == 0 and chess[new_y][new_x] != 2:
                    continue
                # 이동하려는 위치에 벽이 있는 경우
                elif chess[new_y][new_x] == 2:
                    break
                # 이동하려는 위치에 다른 기사가 있을 경우
                elif knight[new_y][new_x] != 0:
                    for j in range(new_y, -1, -1):
                        if knight[j][new_x] != 0 and knight[j][new_x] not in others:
                            others.append(knight[j][new_x])
                        elif knight[j][new_x] == 0:
                            break
            else:
                break
        # 이동할 수 있어서 이동
        else:
            if others:
                test = check(others, d)
                if test:
                    change(knight_info[n - 1], n, d, 0)
            else:
                change(knight_info[n - 1], n, d, 0)
    elif d == 1:
        for i in range(x[2]):
            new_y, new_x = x[0] + i + dy[1] - 1, x[1] + x[3] - 1 + dx[1] - 1
            if 0 <= new_y < L and 0 <= new_x < L:
                if knight[new_y][new_x] == 0 and chess[new_y][new_x] != 2:
                    continue
                elif chess[new_y][new_x] == 2:
                    break
                elif knight[new_y][new_x] != 0:
                    for j in range(new_x, L):
                        if knight[new_y][j] != 0 and knight[new_y][j] not in others:
                            others.append(knight[new_y][j])
                        elif knight[new_y][j] == 0:
                            break
            else:
                break
        else:
            if others:
                test = check(others, d)
                if test:
                    change(knight_info[n - 1], n, d, 0)
            else:
                change(knight_info[n - 1], n, d, 0)
    elif d == 2:
        for i in range(x[3]):
            new_y, new_x = x[0] + x[2] - 1 + dy[2] - 1, x[1] + i + dx[2] - 1
            if 0 <= new_y < L and 0 <= new_x < L:
                if knight[new_y][new_x] == 0 and chess[new_y][new_x] != 2:
                    continue
                elif chess[new_y][new_x] == 2:
                    break
                elif knight[new_y][new_x] != 0:
                    for j in range(new_y, L):
                        if knight[j][new_x] != 0 and knight[j][new_x] not in others:
                            others.append(knight[j][new_x])
                        elif knight[j][new_x] == 0:
                            break
            else:
                break
        else:
            if others:
                test = check(others, d)
                if test:
                    change(knight_info[n - 1], n, d, 0)
            else:
                change(knight_info[n - 1], n, d, 0)
    else:
        for i in range(x[2]):
            new_y, new_x = x[0] + i + dy[3] - 1, x[1] + dx[3] - 1
            if 0 <= new_y < L and 0 <= new_x < L:
                if knight[new_y][new_x] == 0 and chess[new_y][new_x] != 2:
                    continue
                elif chess[new_y][new_x] == 2:
                    break
                elif knight[new_y][new_x] != 0:
                    for j in range(new_x, -1, -1):
                        if knight[new_y][j] != 0 and knight[new_y][j] not in others:
                            others.append(knight[new_y][j])
                        elif knight[new_y][j] == 0:
                            break
            else:
                break
        else:
            if others:
                test = check(others, d)
                if test:
                    change(knight_info[n - 1], n, d, 0)
            else:
                change(knight_info[n - 1], n, d, 0)


def check(others, d):
    # 어느 기사부터 움직여야 하는지 우선순위 판별
    size = []
    for i in range(len(others)):
        t = knight_info[others[i] - 1]
        if d == 0:
            size.append([t[0], others[i]])
        elif d == 1:
            size.append([t[1] + t[3] - 1, others[i]])
        elif d == 2:
            size.append([t[0] + t[2] - 1, others[i]])
        else:
            size.append([t[1], others[i]])
    if d == 0 or d == 3:
        size.sort(key=lambda x: x[0])
    else:
        size.sort(key=lambda x: x[0], reverse=True)
    for u in range(len(others)):
        x = knight_info[size[u][1] - 1]
        if d == 0:
            for i in range(x[3]):
                new_y, new_x = x[0] + dy[0] - 1, x[1] + i + dx[0] - 1
                if 0 <= new_y < L and 0 <= new_x < L:
                    # 이동하려는 위치에 아무도 없을 경우
                    if knight[new_y][new_x] == 0 and chess[new_y][new_x] != 2:
                        continue
                    # 이동하려는 위치에 벽이 있는 경우
                    elif chess[new_y][new_x] == 2:
                        return False
                else:
                    return False
            # 이동할 수 있어서 이동
            else:
                change(knight_info[size[u][1] - 1], size[u][1], d, 1)
        elif d == 1:
            for i in range(x[2]):
                new_y, new_x = x[0] + i + dy[1] - 1, x[1] + x[3] - 1 + dx[1] - 1
                if 0 <= new_y < L and 0 <= new_x < L:
                    if knight[new_y][new_x] == 0 and chess[new_y][new_x] != 2:
                        continue
                    elif chess[new_y][new_x] == 2:
                        return False
                else:
                    return False
            else:
                change(knight_info[size[u][1] - 1], size[u][1], d, 1)
        elif d == 2:
            for i in range(x[3]):
                new_y, new_x = x[0] + x[2] - 1 - 1 + dy[2], x[1] + i + dx[2] - 1
                if 0 <= new_y < L and 0 <= new_x < L:
                    if knight[new_y][new_x] == 0 and chess[new_y][new_x] != 2:
                        continue
                    elif chess[new_y][new_x] == 2:
                        return False
                else:
                    return False
            else:
                change(knight_info[size[u][1] - 1], size[u][1], d, 1)
        else:
            for i in range(x[2]):
                new_y, new_x = x[0] + i + dy[3] - 1, x[1] + dx[3] - 1
                if 0 <= new_y < L and 0 <= new_x < L:
                    if knight[new_y][new_x] == 0 and chess[new_y][new_x] != 2:
                        continue
                    elif chess[new_y][new_x] == 2:
                        return False
                else:
                    return False
            else:
                change(knight_info[size[u][1] - 1], size[u][1], d, 1)
    return True


dy, dx = [-1, 0, 1, 0], [0, 1, 0, -1]
L, N, Q = map(int, input().split())  # 체스판의 크기, 기사의 수, 명령의 수
chess = [list(map(int, input().split())) for _ in range(L)]  # 0 = 빈칸, 1 = 함정, 2 = 벽
knight = [[0] * L for _ in range(L)]
knight_info = []
life = []
for i in range(N):
    r, c, h, w, k = map(int, input().split())
    knight_info.append([r, c, h, w, k])
    life.append(k)
    for j in range(h):
        for k in range(w):
            knight[j + r - 1][k + c - 1] = i + 1
for _ in range(Q):
    n, d = map(int, input().split())  # n번 기사에게 방향 d(상, 우, 하, 좌)로 한 칸 이동
    # 해당 기사가 살아있을 경우에만 명령 수행
    if knight_info[n - 1][4] == 0:
        continue
    moving(n, d)

result = 0
for i in range(N):
    if knight_info[i][4] != 0:
        result += life[i] - knight_info[i][4]
print(result)