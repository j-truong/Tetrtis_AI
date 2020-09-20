import pygame
import copy

hidden_rows = 4

class Board:

	def __init__(self):
		self.x = 10
		self.y = 20 + hidden_rows

		self.locked_board = [[(255,255,255) for _ in range(self.x)] for _ in range(self.y)]
		self.temp_board = copy.deepcopy(self.locked_board)
		self.temp_input_board = copy.deepcopy(self.locked_board)

		self.level = 0
		self.lines = 0
		self.score = 0

		self.height = 0


	def update_board(self, piece):

		# Given a piece, this function updates the colour of the board data.
		# update_validation must be called before this to check feasibility.
		#
		# param piece 		Tetromino

		self.temp_board = copy.deepcopy(self.locked_board)
		
		for i, line in enumerate(piece.shape[piece.rotation%len(piece.shape)]):
			for j, char in enumerate(line):

				if char == '0':
					self.temp_board[piece.y+j][piece.x+i] = piece.colour


	def update_validation(self, piece):

		# Checks whether position of piece is feasible on the board.
		#
		# param piece 		Tetromino

		# potential positions
		accepted_positions = [] 	
		for i in range(self.x):
			for j in range(self.y):
				if self.locked_board[j][i] == (255,255,255):
					accepted_positions.append( (j,i) )

		for i, line in enumerate(piece.shape[piece.rotation%len(piece.shape)]):
			for j, char in enumerate(line):
				if char == '0':
					if (piece.y+j,piece.x+i) not in accepted_positions:
						return False

		return True


	def lock_piece(self, piece):

		# Locks piece in locked data.
		#
		# param piece 		Tetromino

		for i, line in enumerate(piece.shape[piece.rotation%len(piece.shape)]):
			for j, char in enumerate(line):

				if char == '0':
					self.locked_board[piece.y+j][piece.x+i] = piece.colour


	def scoring(self):

		# Given a successful tetris, this function will implement the Original Sega scoring 
		#system.

		line = 0
		points = 0

		# Check for completed lines in board
		for old_row in range(self.y-1,0,-1):
			if (255,255,255) not in self.locked_board[old_row]:
				line += 1

				del self.locked_board[old_row]
				self.locked_board.insert(0, [(255,255,255) for _ in range(self.x)])


		# Original Sega Scoring System
		# line_multiplier = {1:1, 2:4, 3:9, 4:20}
		# if line == 0:
		# 	pass
		# elif 0 <= self.level <= 1:
		# 	points += 100*line_multiplier[line]
		# elif 2 <= self.level <= 3:
		# 	points += 200*line_multiplier[line]
		# elif 4 <= self.level <= 5:
		# 	points += 300*line_multiplier[line]
		# elif 6 <= self.level <= 7:
		# 	points += 400*line_multiplier[line]
		# elif self.level <= 8:
		# 	points += 500*line_multiplier[line]
		if line == 0:
			pass
		elif line == 1:
			points += 40
		elif line == 2:
			points += 120
		elif line == 3:
			points += 300
		elif line == 4:
			points += 1200


		# Check for Perfect Clear
		perfect_clear = all([x == (255,255,255) for x in self.locked_board[i]] for i in range(len(self.locked_board)))
		if perfect_clear:
			points *= 10

		self.lines += line
		self.score += points

		# Tetris(NES, Nintendo) level system
		if self.lines < 200:
			self.level = self.lines // 10


	def draw_board(self ,win, board_x, board_y, block_size):

		# Draws the board and grid lines using pygame.
		#	
		# param win			Pygame window
		# param board_x		Starting x point of board
		# param board y 	Starting y point of board
		# param block_size	Block size

		border_size = 3


		for i in range(self.x):
			for j in range(hidden_rows,self.y):

				# Draw board
				pygame.draw.rect(win, self.temp_board[j][i], 
					(board_x + i*block_size, board_y + j*block_size, block_size, block_size), 0)	

				# Draw grid line
				pygame.draw.line(win, (128,128,128), 
					(board_x + i*block_size, board_y + (hidden_rows*block_size)), 
					(board_x + i*block_size, board_y + block_size*self.y))	
				pygame.draw.line(win, (128,128,128), 
					(board_x, board_y + j*block_size), 
					(board_x + self.x*block_size, board_y + j*block_size))


		# Draw border line
		pygame.draw.line(win, (255,0,0),
			(board_x, board_y + (hidden_rows*block_size)), 
			(board_x + self.x*block_size, board_y + (hidden_rows*block_size)),
			border_size)
		pygame.draw.line(win, (255,0,0),
			(board_x, board_y + self.y*block_size), 
			(board_x + self.x*block_size, board_y + self.y*block_size),
			border_size)
		pygame.draw.line(win, (255,0,0),
			(board_x, board_y + (hidden_rows*block_size)), 
			(board_x, board_y + (self.y*block_size)),
			border_size)
		pygame.draw.line(win, (255,0,0),
			(board_x + self.x*block_size, board_y + (hidden_rows*block_size)), 
			(board_x + self.x*block_size, board_y + (self.y*block_size)),
			border_size)


	def input_data(self, piece):

		# Calculates the input data for genetic algorithm given the tetromino piece.
		#
		# param  piece 				Tetromino
		# output sum(heights)		Aggregrated height
		# output completed_lines	Lines completed
		# output holes 				Holes within stack
		# output bumpiness			Bumpiness within height


		# Updates temp_board with hard-dropped piece to conduct analysis
		for i in range(30):
			piece.y += 1

			if not self.update_validation(piece):
				piece.y -= 1
				self.update_board(piece)
				piece.y -= i
				break


		# Calculate input data
		heights = [0 for i in range(self.x)]
		height_counted = [False for i in range(self.x)]

		holes = 0
		completed_lines = 0
		bumpiness = 0


		for j in range(hidden_rows, self.y):

			if not (255,255,255) in self.temp_board[j]:
				completed_lines += 1

			for i in range(self.x):

				# Find height if column not empty
				if not self.temp_board[j][i] == (255,255,255) and not height_counted[i]:
					heights[i] = self.y - j
					height_counted[i] = True

				# Count holes if column height acquired
				if self.temp_board[j][i] == (255,255,255) and height_counted[i]:
					holes += 1

		# Calculate bumpiness
		for i in range(self.x - 2):
			bumpiness += abs(heights[i] - heights[i+1])


		return [sum(heights), completed_lines, holes, bumpiness]
		#return (*heights, completed_lines, holes, bumpiness)
		#return sum(heights), completed_lines, holes, bumpiness




	def board_heuristic_inputs(self, piece):

		# Calculates heursitic inputs for every combination of rotation and position in x axis.
		#
		# param	 piece 		Tetromino
		# output inputs		Inputs (size: [160])

		inputs = [0 for i in range(40*4)]

		for k in range(piece.rotations):
			piece.rotation = k

			# Move furthest to left
			for j in range(5):
				piece.x -= 1
				if not self.update_validation(piece):
					piece.x += 1
					break

			# Obtain heuristic inputs for each combination of rotation and column position
			for j in range(10):				
				if self.update_validation(piece):
					inputs[ 10*k + 4*j : 10*k + 4*(j+1) ] = self.input_data(piece)
				piece.x += 1

		# Reset to original piece parameters
		piece.x = 0
		piece.rotation = 0

		return inputs
