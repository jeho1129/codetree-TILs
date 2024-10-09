def moving():
    global result
    for i in range(M):
        if people_locate[i] == exits:
            continue

        people_y, people_x = people_locate[i][0], people_locate[i][1]
        exits_y, exits_x = exits[0], exits[1]

        if people_y != exits_y:
            new_y, new_x = people_y, people_x
            if new_y > exits_y:
                new_y -= 1
            else:
                new_y += 1

            if not miro[new_y][new_x]:
                people_locate[i] = [new_y, new_x]
                result += 1
                continue

        if people_x != exits_x:
            new_y, new_x = people_y, people_x
            if new_x > exits_x:
                new_x -= 1
            else:
                new_x += 1

            if not miro[new_y][new_x]:
                people_locate[i] = [new_y, new_x]
                result += 1
                continue


def find_square():
    for i in range(2, N + 1):
        for j in range(N - i + 1):
            for k in range(N - i + 1):
                j2, k2 = j + i - 1, k + i - 1
                # 출입구가 해당 사각형에 없을 경우
                if j > exits[0] or exits[0] > j2 or k > exits[1] or exits[1] > k2:
                    continue
                count = 0
                for l in range(M):
                    if not (people_locate[l][0] == exits[0] and people_locate[l][1] == exits[1]):
                        if j <= people_locate[l][0] <= j2 and k <= people_locate[l][1] <= k2:
                            count += 1
                if count > 0:
                    return j, k, i


def rotate(sy, sx, length):
    new_arr = [[0] * N for _ in range(N)]
    for y in range(sy, sy + length):
        for x in range(sx, sx + length):
            # (0, 0)으로 옮기는 변환
            oy, ox = y - sy, x - sx
            # 회전했을 때 좌표
            ry, rx = ox, length - oy - 1
            new_arr[sy + ry][sx + rx] = miro[y][x]

    for y in range(sy, sy + length):
        for x in range(sx, sx + length):
            miro[y][x] = new_arr[y][x]
            if miro[y][x] > 0:
                miro[y][x] -= 1


def rotate2(sy, sx, length):
    global exits
    for i in range(M):
        if sy <= people_locate[i][0] < sy + length and sx <= people_locate[i][1] < sx + length:
            oy, ox = people_locate[i][0] - sy, people_locate[i][1] - sx
            ry, rx = ox, length - oy - 1
            people_locate[i] = [sy + ry, sx + rx]

    oy, ox = exits[0] - sy, exits[1] - sx
    ry, rx = ox, length - oy - 1
    exits = [sy + ry, sx + rx]


N, M, K = map(int, input().split())
miro = [list(map(int, input().split())) for _ in range(N)]
people_locate = [list(map(lambda x: x - 1, map(int, input().split()))) for _ in range(M)]
exits = list(map(int, input().split()))
exits = [x - 1 for x in exits]
result = 0
for _ in range(K):
    moving()
    # 모든 사람이 탈출했을 때, 즉시 종료
    for i in range(M):
        if people_locate[i] != exits:
            break
    else:
        break
    j, k, l = find_square()
    rotate(j, k, l)
    rotate2(j, k, l)
print(result)