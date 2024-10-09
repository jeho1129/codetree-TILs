from collections import deque

def change(knight_info, knight_id, direction):
    # 기사 위치 업데이트
    for i in range(knight_info[knight_id - 1][2]):
        for j in range(knight_info[knight_id - 1][3]):
            knight[knight_info[knight_id - 1][0] + i - 1][knight_info[knight_id - 1][1] + j - 1] = 0
            
    knight_info[knight_id - 1][0] += dy[direction]
    knight_info[knight_id - 1][1] += dx[direction]
    
    for i in range(knight_info[knight_id - 1][2]):
        for j in range(knight_info[knight_id - 1][3]):
            knight[knight_info[knight_id - 1][0] + i - 1][knight_info[knight_id - 1][1] + j - 1] = knight_id
            
def moving(knight_id, direction):
    x = knight_info[knight_id - 1]
    others = deque()
    can_move = True
    
    # 이동할 위치 조사
    for i in range(x[2] if direction in (0, 2) else x[3]):
        new_y = x[0] + dy[direction] - 1 + (i if direction in (0, 2) else 0)
        new_x = x[1] + dx[direction] - 1 + (i if direction in (1, 3) else 0)

        if not (0 <= new_y < L and 0 <= new_x < L):
            can_move = False
            break
        
        if chess[new_y][new_x] == 2:  # 벽
            can_move = False
            break
        
        if knight[new_y][new_x] != 0:  # 다른 기사
            others.append(knight[new_y][new_x])

    if can_move:
        # 기사 이동
        change(knight_info, knight_id, direction)
        if others:
            apply_damage(others, knight_id, direction)

def apply_damage(others, knight_id, direction):
    # 피해 계산
    damage_map = [[0] * L for _ in range(L)]
    x = knight_info[knight_id - 1]
    
    # 이동한 위치의 함정 수 세기
    for i in range(x[2]):
        for j in range(x[3]):
            new_y = x[0] + dy[direction] - 1 + i
            new_x = x[1] + dx[direction] - 1 + j
            if 0 <= new_y < L and 0 <= new_x < L:
                if chess[new_y][new_x] == 1:
                    damage_map[new_y][new_x] += 1

    # 밀려난 기사들에게 피해 적용
    for knight_id in others:
        knight_info[knight_id - 1][4] -= damage_map[x[0] + dy[direction] - 1][x[1] + dx[direction] - 1]
        if knight_info[knight_id - 1][4] <= 0:
            knight_info[knight_id - 1][4] = 0  # 기사 제거

# 초기화 및 입력 처리
dy, dx = [-1, 0, 1, 0], [0, 1, 0, -1]
L, N, Q = map(int, input().split())  
chess = [list(map(int, input().split())) for _ in range(L)]  
knight = [[0] * L for _ in range(L)]
knight_info = []

for i in range(N):
    r, c, h, w, k = map(int, input().split())
    knight_info.append([r, c, h, w, k])
    for j in range(h):
        for k in range(w):
            knight[j + r - 1][k + c - 1] = i + 1

for _ in range(Q):
    n, d = map(int, input().split())
    if knight_info[n - 1][4] > 0:  # 살아있으면
        moving(n, d)

result = sum(life - knight_info[i][4] for i, life in enumerate(knight_info) if life[4] > 0)
print(result)