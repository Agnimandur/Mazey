import random
import json
import collections

#generate a maze via randomized prim's algorithm with "N" rows and "M" columns
class Maze:
	def __init__(self,N,M,player,message=None,moves=0,seed=None):
		self.moves = moves
		self.message = message
		self.player = player
		if type(N)==int and type(M)==int:
			self.maze = self.generate_maze(N,M,seed)
			self.center = [1,1]
			self.N=N
			self.M=M
		elif type(N)==list and type(M)==list:
			self.maze = N
			self.center = M
			self.N = len(self.maze)-1
			self.M = len(self.maze[0])-1
		else:
			raise ValueError
	
	def generate_maze(self,N,M,seed):
		assert 6 <= N <= 50 and 6 <= M <= 50, "dimensions must be in the interval [6,50]"
		assert N % 2 == 0 and M % 2 == 0, "dimensions must be even"
		if seed:
			random.seed(seed)
		
		PASSAGE_CHAR = '.'
		WALL_CHAR = 'X'
		WALL = False
		PASSAGE = True
		maze = []
		for i in range(N):
			maze.append([WALL]*M)

		frontiers = []
		x = random.randint(0,N-1)
		y = random.randint(0,M-1)
		frontiers.append([x,y,x,y])
		while len(frontiers) > 0:
			ind = random.randint(0,len(frontiers)-1)
			f = frontiers[ind]
			del frontiers[ind]
			x = f[2]
			y = f[3]
			if maze[x][y] == WALL:
				maze[f[0]][f[1]] = PASSAGE
				maze[x][y] = PASSAGE

				if x >= 2 and maze[x-2][y] == WALL:
					frontiers.append([x-1,y,x-2,y])
				
				if y >= 2 and maze[x][y-2] == WALL:
					frontiers.append([x,y-1,x,y-2])
				if x < N-2 and maze[x+2][y] == WALL:
					frontiers.append([x+1,y,x+2,y])
				if y < M-2 and maze[x][y+2] == WALL:
					frontiers.append([x,y+1,x,y+2])
		
		if PASSAGE in maze[0]:
			maze = [[WALL]*M] + maze
		else:
			maze = maze + [[WALL]*M]
		if PASSAGE in [maze[i][0] for i in range(len(maze))]:
			for i in range(len(maze)):
				maze[i].insert(0,WALL)
		else:
			for i in range(len(maze)):
				maze[i].append(WALL)
		return maze

	def display(self,n=5):
		WALL = False
		assert self.maze[self.center[0]][self.center[1]] != WALL, "cannot be at a wall"
		toprow = self.center[0]-n//2
		leftcol = self.center[1]-n//2
		result = []
		for i in range(n):
			result.append([WALL]*n)
		dirs = [[0,-1],[0,1],[1,0],[-1,0]]
		for dir in dirs:
			cell = [self.center[0],self.center[1]]
			while 0 <= cell[0] < len(self.maze) and 0 <= cell[1] < len(self.maze[0]) and self.maze[cell[0]][cell[1]] != WALL and abs(cell[0]-self.center[0])+abs(cell[1]-self.center[1]) <= n//2:
				result[cell[0]-toprow][cell[1]-leftcol] = (not WALL)
				cell[0] += dir[0]
				cell[1] += dir[1]
		return result

	def render_maze(self,wall=':black_large_square:',passage=':white_large_square:', player=':white_square_button:',goal=':red_square:',text=False):
		maze = self.display()
		n = len(maze)
		h = n//2
		ans = ""
		for i in range(n):
			for j in range(n):
				if i == h and j == h:
					ans += player
				elif maze[i][j]:
					if self.center[0]+(i-h) == self.N-1 and self.center[1]+(j-h) == self.M-1:
						ans += goal
					else:
						ans += passage
				else:
					ans += wall
			ans += '\n'
		if text: ans = f"```\n{ans}```"
		return ans

	def move(self,dir):
		d = {"left":[0,-1],"right":[0,1],"up":[-1,0],"down":[1,0]}
		x = d[dir]
		if self.maze[self.center[0]+x[0]][self.center[1]+x[1]]:
			self.center = [self.center[0]+x[0],self.center[1]+x[1]]
			self.moves += 1
			return True
		else:
			return False

	def fastest(self):
		INF = 1000000
		dist = [[INF for x in range(self.N)] for y in range(self.M)]
		dist[self.N-1][self.M-1] = 0
		bfs = collections.deque()
		bfs.append((self.N-1,self.M-1))
		dirs = [[0,-1],[0,1],[-1,0],[1,0]]
		while len(bfs)>0:
			cell = bfs.popleft()
			for dir in dirs:
				r = cell[0]+dir[0]
				c = cell[1]+dir[1]
				if 0 <= r < self.N and 0 <= c < self.M and self.maze[r][c] and dist[r][c]==INF:
					dist[r][c] = dist[cell[0]][cell[1]]+1
					bfs.append((r,c))
		
		return dist[1][1]
			
	def atgoal(self):
		return self.center==[self.N-1,self.M-1]