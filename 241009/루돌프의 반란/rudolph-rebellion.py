from collections import deque


def moving_r():
    min_num, min_dist = -1, -1
    # 가장 가까운 산타가 누구인 지 판별
    for i in range(P):
        # 생존한 산타만 판별
        if s[i][3] != -1:
            dist = (r[0] - s[i][0]) ** 2 + (r[1] - s[i][1]) ** 2
            if min_dist == -1 or dist < min_dist:
                min_dist = dist
                min_num = i
            elif dist == min_dist:
                if s[min_num][0] < s[i][0] or (s[min_num][0] == s[i][0] and s[min_num][1] < s[i][1]):
                    min_num = i
    # 가장 가까운 산타를 향해 1칸 돌진
    direction = -1
    if s[min_num][0] > r[0]:
        r[0] += 1
        if s[min_num][1] > r[1]:
            r[1] += 1
            direction = 7
        elif s[min_num][1] < r[1]:
            r[1] -= 1
            direction = 6
        else:
            direction = 2
    elif s[min_num][0] == r[0]:
        if s[min_num][1] > r[1]:
            r[1] += 1
            direction = 1
        elif s[min_num][1] < r[1]:
            r[1] -= 1
            direction = 3
    else:
        r[0] -= 1
        if s[min_num][1] > r[1]:
            r[1] += 1
            direction = 5
        elif s[min_num][1] < r[1]:
            r[1] -= 1
            direction = 4
        else:
            direction = 0
    # 산타와 충돌할 경우
    if (direction < 4 and min_dist == 1) or (4 <= direction < 8 and min_dist == 2):
        # C칸 만큼의 거리가 밀리고 점수를 획득, 해당 산타는 2턴만큼 기절
        s[min_num][0] += dy[direction] * C
        s[min_num][1] += dx[direction] * C
        result[s[min_num][2] - 1] += C
        s[min_num][3] = 2
        # 게임판 밖으로 밀리면 탈락
        if s[min_num][0] < 1 or s[min_num][0] > N or s[min_num][1] < 1 or s[min_num][1] > N:
            s[min_num][3] = -1
        # 밀린 곳에 다른 산타가 있는 지 판별
        else:
            check_santa(s[min_num], direction)


def check_santa(santa, direction):
    for i in range(P):
        # 밀린 곳에 다른 산타가 있을 경우, 해당 산타는 1칸만큼 밀림
        if s[i][0] == santa[0] and s[i][1] == santa[1] and s[i][2] != santa[2] and s[i][3] != -1:
            s[i][0] += dy[direction]
            s[i][1] += dx[direction]
            # 밖으로 밀리면 탈락
            if s[i][0] < 1 or s[i][0] > N or s[i][1] < 1 or s[i][1] > N:
                s[i][3] = -1
            # 안 밀리면 다시 확인
            else:
                check_santa(s[i], direction)
    else:
        return


def moving_s():
    for i in range(P):
        # 각 산타의 상태 판별
        if s[i][3] == 0:
            min_direction, min_dist = -1, (s[i][0] - r[0]) ** 2 + (s[i][1] - r[1]) ** 2
            for j in range(4):
                new_y, new_x = s[i][0] + dy[j], s[i][1] + dx[j]
                if 1 <= new_y <= N and 1 <= new_x <= N:
                    # 해당 자리에 산타가 없을 경우만 이동 가능
                    for k in range(P):
                        if s[k][2] != s[i][2] and s[k][0] == new_y and s[k][1] == new_x:
                            break
                    else:
                        dist = (new_y - r[0]) ** 2 + (new_x - r[1]) ** 2
                        if min_dist > dist:
                            min_dist = dist
                            min_direction = j
            # 움직일 수 있는 경우
            if min_direction != -1:
                s[i][0] += dy[min_direction]
                s[i][1] += dx[min_direction]
                # 루돌프와 부딪힐 경우
                if s[i][0] == r[0] and s[i][1] == r[1]:
                    # D칸 만큼의 반대 방향으로 거리가 밀리고 점수를 획득, 해당 산타는 2턴만큼 기절
                    s[i][0] += dy[(min_direction + 2) % 4] * D
                    s[i][1] += dx[(min_direction + 2) % 4] * D
                    result[s[i][2] - 1] += D
                    s[i][3] = 2
                    # 게임판 밖으로 밀리면 탈락
                    if s[i][0] < 1 or s[i][0] > N or s[i][1] < 1 or s[i][1] > N:
                        s[i][3] = -1
                    # 밀린 곳에 다른 산타가 있는 지 판별
                    else:
                        check_santa(s[i], (min_direction + 2) % 4)


dy, dx = [-1, 0, 1, 0, -1, -1, 1, 1], [0, 1, 0, -1, -1, 1, -1, 1]
N, M, P, C, D = map(int, input().split())
r = list(map(int, input().split()))
s = deque()
result = [0] * P
for _ in range(P):
    sn, sr, sc = map(int, input().split())
    s.append([sr, sc, sn, 0])
for _ in range(M):
    # 모든 산타 기절 스택 1 감소, 모두 탈락 시 즉시 게임 종료
    out_santa = 0
    for i in range(P):
        if s[i][3] > 0:
            s[i][3] -= 1
        elif s[i][3] == -1:
            out_santa += 1
    if out_santa == P:
        break
    s = deque(sorted(s, key=lambda x: x[2]))
    moving_r()
    s = deque(sorted(s, key=lambda x: x[2]))
    moving_s()
    # 턴이 끝날 때, 생존한 산타는 1점씩 추가
    for i in range(P):
        if s[i][3] >= 0:
            result[s[i][2] - 1] += 1
print(*result)