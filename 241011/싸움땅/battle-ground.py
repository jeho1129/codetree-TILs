dy, dx = [-1, 0, 1, 0], [0, 1, 0, -1]


def game(n):
    # 본인이 향하는 방향으로 한 칸 이동
    new_y, new_x = player[n][0] + dy[player[n][2]], player[n][1] + dx[player[n][2]]
    # 격자를 벗어나면 정반대 방향으로 방향을 바꾸어서 한 칸 이동
    if new_y < 0 or new_x < 0 or new_y >= N or new_x >= N:
        player[n][2] = (player[n][2] + 2) % 4
        new_y, new_x = player[n][0] + dy[player[n][2]], player[n][1] + dx[player[n][2]]

    player[n][0], player[n][1] = new_y, new_x
    # 이동한 방향에 플레이어가 없으면 총이 있는 지 확인
    for i in range(M):
        if i == n:
            continue
        # 이동한 방향에 플레이어가 있을 경우
        # 싸움에 돌입
        if player[i][0] == new_y and player[i][1] == new_x:
            fight(n, i, new_y, new_x)
    # 이동한 방향에 플레이어가 없을 경우
    else:
        x = player[n][4]
        y = guns[new_y][new_x]
        # 총이 있는 지 확인
        if y > 0:
            # 플레이어가 총이 없거나, 기존 공격력이 낮을 경우
            if 0 <= x < y:
                player[n][4] = y
                guns[new_y][new_x] = x


def fight(a, b, new_y, new_x):
    # 두 플레이어의 초기 능력치 + 가지고 있는 공격력의 합을 비교
    a1, a2, b1, b2 = player[a][3], player[a][4], player[b][3], player[b][4]
    # 더 큰 플레이어가 승리
    if a1 + a2 > b1 + b2:
        winner = a
        loser = b
    elif b1 + b2 > a1 + a2:
        winner = b
        loser = a
    # 만약 수치가 같을 경우에는 초기 능력치가 더 높은 플레이어가 승리
    else:
        if a1 > b1:
            winner = a
            loser = b
        else:
            winner = b
            loser = a
    # 이긴 플레이어는 각 플레이어의 초기 능력치와 가지고 있는 총의 공격력의 합의 차이만큼 포인트로 획득
    points[winner] += abs((a1 + a2) - (b1 + b2))
    # 진 플레이어는 본인이 가지고 있는 총을 해당 격자에 내려 놓고
    x = player[loser][4]
    y = guns[new_y][new_x]
    if x > y:
        guns[new_y][new_x] = x
    player[loser][4] = 0
    # 이긴 플레이어는 승리한 칸에서 떨어져 있는 총과 원래 들고 있는 총 중 가장 공격력이 높은 총을 획득하고, 나머지 총은 내려 놓는다
    x = player[winner][4]
    if x < y:
        guns[new_y][new_x] = x
        player[winner][4] = y
    # 진 플레이어는 해당 플레이어가 원래 가고 있던 방향으로 한 칸 더 이동
    y1, x1 = player[loser][0] + dy[player[loser][2]], player[loser][1] + dx[player[loser][2]]
    # 범위 밖인 경우, 다른 플레이어가 이미 위치해 있는 경우
    while True:
        if y1 < 0 or y1 >= N or x1 < 0 or x1 >= N:
            player[loser][2] = (player[loser][2] + 1) % 4
            y1, x1 = player[loser][0] + dy[player[loser][2]], player[loser][1] + dx[player[loser][2]]
        else:
            for i in range(M):
                if player[i][0] == y1 and player[i][1] == x1:
                    player[loser][2] = (player[loser][2] + 1) % 4
                    y1, x1 = player[loser][0] + dy[player[loser][2]], player[loser][1] + dx[player[loser][2]]
                    break
            else:
                break
    player[loser][0], player[loser][1] = y1, x1
    # 해당 칸에 총이 있다면 다시 비교
    x2 = player[loser][4]
    y2 = guns[y1][x1]
    # 총이 있는 지 확인
    if y2 > 0:
        # 플레이어가 총이 없거나, 기존 공격력이 낮을 경우
        if 0 <= x2 < y2:
            player[loser][4] = y2
            guns[y1][x1] = x2


N, M, K = map(int, input().split())  # N = 격자의 크기, M = 플레이어 수, K = 라운드
guns = [list(map(int, input().split())) for _ in range(N)]
# [0] = x 좌표, [1] = y 좌표, [2] = 방향(상우하좌), [3] = 초기 능력치, [4] = 보유 공격력
player = [list(map(int, input().split())) + [0] for _ in range(M)]
for i in range(M):
    player[i][0], player[i][1] = player[i][0] - 1, player[i][1] - 1
points = [0] * M
for _ in range(K):
    for j in range(M):
        game(j)
print(points)