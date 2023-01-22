import copy
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    # Search function

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    #  Applying Kruskal algorithm
    def kruskal_algo(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        # for u, v, weight in result:
            # print("%d - %d: %d" % (u, v, weight))

        return result

def dfs(times, i, visited):
	# if(visited[i] == 0):
	visited[i] = 1
	n = len(times)
	for i in range(1, n+1):
		if(visited[i] == 0):
			dfs(times, i, visited)

	# here means I have reached the end 



def computeTime(temp1, times):
	# mstTree = getMST(times)
	# print(mstTree)
	# n = len(times)
	# visited = [0 for i in range(n)]
	
	# x = 0
	# for i in mstTree:
	# 	x += i[2]

	count = 0
	nodes = {}
	for i in temp1:
		nodes[i] = count 
		count += 1

	print(temp1)
	print(nodes)
	print(len(nodes))

	g = Graph(len(nodes))
	for i in range(len(temp1)):
		for j in range(i+1, len(temp1)):
			g.add_edge(nodes[temp1[i]], nodes[temp1[j]], times[temp1[i]][temp1[j]])
			# print(nodes[temp1[i]], nodes[temp1[j]], times[temp1[i]][temp1[j]])

	res = g.kruskal_algo()
	# print(g.kruskal_algo())

	ans = 0
	for i in res:
		ans += i[2]

	return ans

	
def solve(n, m, times):
	
	timesC = []
	timesC.append([])
	for i in range(1, len(times)):
		# X = times[i]
		# X.sort()
		# timesC.append(X)
		X = []
		for j in range(1, len(times)):
			X.append([times[i][j], j])
		X.sort()
		# print(X)
		timesC.append(X)


	locations = {}
	# print(timesC[3])
	# exit()
	
	# initial point
	# S = timesC[0][0][0]
	# S = 1
	# # print(timesC[0])
	# currDriver = 1
	# print("first point", S)

	# get the first x points
	for i in range(1, n+1):
		locations[1] = i
		currSet = [1]
		options = set()

		count = 0
		while (count < 20):
			x = 0
			for j in currSet:
				for k in range(len(timesC[j])):
					if timesC[j][k][1] not in locations:
						x += 1 
						options.add(timesC[j][k][1])
					if(x > 4):
						break

			# when flag is true everything is in locatiosn, 
			flag= True
			for k in range(1,m+1):
				if k not in locations:
					flag=False
			
			if flag ==True:
				count = 21
				break
				
			menEle = 100000
			thisEle = -1
			for k in options:
				temp1 = copy.deepcopy(currSet)
				temp1.append(k)
				x = computeTime(temp1, times)
				if(x < menEle):
					thisEle = k
					menEle = x
			

			locations[thisEle] = i
			currSet.append(thisEle)
			options.remove(thisEle)
			count += 1

	print(locations)
	return locations

# n = int(input())
# m = int(input())

# # let hub be location 1
# times = [[10000 for i in range(m+1)] for j in range(m+1)]
# # print(len(times))

# # for i in range(m):
# # 	for j in range(i+1, m):
# # 		arr = list(map(int, input().split()))
# # 		# print(arr)
# # 		times[arr[0]][arr[1]] = arr[2]
# def distance(x1, y1, x2, y2):
# 	return 0.5 ** ((x1 - x2) ** 2 + (y1-y2) ** 2)

# points = []

# for i in range(m):
# 	arr = list(map(float,input().split()))
# 	points.append(arr)

# for i in range(m):
# 	for j in range(i+1, m):
# 		times[int(points[i][0])][int(points[j][0])] = distance(points[i][1], points[i][2], points[j][1], points[j][2])

# fig, ax = plt.subplots(figsize = (10,10))
# fig.suptitle("Points")

# # n - number of drivers
# # m - number of locations
# # times - (m + 1)* ( m +1 ) matrix - distance matrix 10000
# # location 1 is the hub

# # return a map -> (location, drivers)
# locations = solve(n, m, times)

# X = []
# Y = []

# for i in range(5):
# 	X.append([])
# 	Y.append([])


# for i in locations.keys():
# 	print(locations[i])
# 	X[locations[i]].append(points[i][1])
# 	Y[locations[i]].append(points[i][2])

# colors = ['blue', 'red', 'black', 'green', 'purple']
# for i in range (5):
# 	ax.scatter(X[i], Y[i], colors[i])

# plt.show()
