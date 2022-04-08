import csv
import math
import heapq
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
        # Begin your code (Part 4)
    MAP = {}
    dist = {}
    h_dist={}
    num_visited = {}
    rev = {}
    vis_count = 1
    with open(edgeFile,'r') as f:
        MAP_tmp = list(csv.reader(f,delimiter=','))
        for i in range(1,len(MAP_tmp)):
            edge = MAP_tmp[i]
            edge[0] = int(edge[0])
            edge[1] = int(edge[1])
            edge[2] = float(edge[2])
            edge[3] = float(edge[3])*1000/3600
            if edge[0] in MAP:
                MAP[edge[0]].append((edge[1],edge[2],edge[3]))
            else:
                MAP[edge[0]] = [(edge[1],edge[2],edge[3])]
            dist[edge[0]] = math.inf
            dist[edge[1]] = math.inf
            num_visited[edge[0]] = 0
            num_visited[edge[1]] = 0

    index = 0
    with open('heuristic.csv','r') as f:
        MAP_tmp = list(csv.reader(f,delimiter=','))
        for i in range(1,len(MAP_tmp[0])):
            if end == int(MAP_tmp[0][i]):
                index = i
        for i in range(1,len(MAP_tmp)):
            h_dist[int(MAP_tmp[i][0])] = float(MAP_tmp[i][index])
    q = []
    heapq.heappush(q,(h_dist[start],start))
    dist[start] = 0
    path = []
    while len(q) != 0:
        (DDIS,now) = heapq.heappop(q)
        if num_visited[now] == 2:
            continue
        num_visited[now] = 2
        if now == end:
            break
        if now not in MAP: 
            continue
        for (next1,DIS,SP) in MAP[now]:
           if (num_visited[next1]!=2):
                if(dist[next1] > dist[now] + DIS/SP):
                    dist[next1] = dist[now] + DIS/SP
                    heapq.heappush(q,(dist[next1]+(h_dist[next1])/SP,next1))
                    rev[next1] = now
                    vis_count = vis_count + 1
                
    rev_now = end
    path.append(end)
    while rev_now != start:
        rev_now = rev[rev_now]
        path.append(rev_now)
    path.reverse()
    return path,dist[end],vis_count
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
