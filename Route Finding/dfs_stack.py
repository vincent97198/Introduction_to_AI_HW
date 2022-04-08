import csv
import math
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    MAP = {}
    dist = {}
    num_visited = {}
    vis_count = 0
    rev = {} 

    with open(edgeFile,'r') as f:
        MAP_tmp = list(csv.reader(f,delimiter=','))
        for i in range(1,len(MAP_tmp)):
            edge = MAP_tmp[i]
            edge[0] = int(edge[0])
            edge[1] = int(edge[1])
            edge[2] = float(edge[2])
            if edge[0] in MAP:
                MAP[edge[0]].append((edge[1],edge[2]))
            else:
                MAP[edge[0]] = [(edge[1],edge[2])]

            dist[edge[0]] = math.inf
            dist[edge[1]] = math.inf
            num_visited[edge[0]] = 0
            num_visited[edge[1]] = 0

    q = []
    q.append(start)
    dist[start] = 0
    path = []
    flag = False
    while len(q) != 0:
        now = q.pop()
        if num_visited[now] == 2:
            continue
        num_visited[now] = 2
        if now not in MAP: 
            continue
        for (next1,DIS) in MAP[now]:
            if num_visited[next1] == 0:
                dist[next1] = dist[now] + DIS
                q.append(next1)
                rev[next1] = now
                num_visited[next1] = 1
                vis_count = vis_count + 1
            if next1 == end:
                flag = True
                break    
        if(flag==True):
            break
    rev_now = end
    path.append(end)
    while rev_now != start:
        rev_now = rev[rev_now]
        path.append(rev_now)
    path.reverse()
    return path,dist[end],vis_count
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
