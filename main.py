import pygame 
import random
import os
import neat
import numpy as np
import pickle

from Board import Board
from Piece import Piece


os.environ['SDL_VIDEO_CENTERED'] = "True"

pygame.font.init()
pygame.init()

GEN = 0 										# Generations

# Dimensions of game window
win_width = 900 								# width of window
win_height = 700								# height of window

play_width = 300								# width of Tetris window
play_height = 600								# height of Tetris window

board_x = 80									# starting x of Tetris window
board_y = -60									# starting y of Tetris window
block_size = play_width /10						# block size of Tetris board


# Resets score.txt when file is ran
with open('scores.txt', 'w') as f:
	f.write(str(0)+'\n'+str(0))


def draw_window(win, board, next_piece, alive, game_score, game_gen_score):

	# Draws windows containing the board and annotations.
	#
	# param win 		Window
	# param board 		Board
	# param next_piece 	Next tetromino
	# gen 				Current generation

	win.fill((0,0,0))
	board.draw_board(win, board_x, board_y, block_size)

	draw_next_piece(win, next_piece)

	
	# Title
	font = pygame.font.SysFont('tahoma', 120)			# fonts: sthupo, consolas, tahoma
	label = font.render('tetrAIs', 1, (255, 255, 255))
	win.blit(label, (430,50))


	# Statistics Annotations
	y_start = 330
	y_add = 45
	font = pygame.font.SysFont('tahoma', 30)	

	label = font.render('LEVEL: '+str(board.level), 1, (255, 255, 255))
	win.blit(label, (450,y_start))

	label = font.render('LINES: '+str(board.lines), 1, (255, 255, 255))
	win.blit(label, (450,y_start + y_add))

	label = font.render('SCORE: '+str(int(board.score)), 1, (255, 255, 255))
	win.blit(label, (450,y_start + 2*y_add))

	label = font.render('GENERATION: '+str(GEN), 1, (255, 255, 255))
	win.blit(label, (450,y_start + 3*y_add))

	label = font.render('ALIVE: '+str(alive), 1, (255, 255, 255))
	win.blit(label, (450,y_start + 4*y_add))

	label = font.render('BEST SCORE: '+str(game_score)+' ('+str(game_gen_score)+')', 1, (255, 255, 255))
	win.blit(label, (450,y_start + 5*y_add))

	pygame.display.update()



def draw_next_piece(win, next_piece):

	# Draws next piece on window
	#
	# param win 		Window
	# param next_piece 	Next tetromino in play
	
	# Next Piece
	next_x = 450
	next_y = 190
	background_dim = 4
	border_size = 4

	# Draws background
	pygame.draw.rect(win, (255, 255, 255), 
					(next_x,next_y, background_dim*block_size, background_dim*block_size), 0)

	for i, row in enumerate(next_piece.shape[0]):
		for j, col in enumerate(row):
			if col == '0':

				# Draw next piece
				pygame.draw.rect(win, next_piece.colour, 
					(next_x+i*block_size,next_y+j*block_size, block_size, block_size), 0)

			# Draw grid line
			pygame.draw.line(win, (128,128,128), 
				(next_x + i*block_size, next_y ), 
				(next_x + i*block_size, next_y + background_dim*block_size))	
			pygame.draw.line(win, (128,128,128), 
				(next_x, next_y + j*block_size), 
				(next_x + background_dim*block_size, next_y + j*block_size))


	# Draw border line
	pygame.draw.line(win, (255,0,0),
		(next_x, next_y), 
		(next_x + background_dim*block_size, next_y),
		border_size)
	pygame.draw.line(win, (255,0,0),
		(next_x, next_y + background_dim*block_size), 
		(next_x + background_dim*block_size, next_y + background_dim*block_size),
		border_size)
	pygame.draw.line(win, (255,0,0),
		(next_x, next_y), 
		(next_x, next_y + (background_dim*block_size)),
		border_size)
	pygame.draw.line(win, (255,0,0),
		(next_x + background_dim*block_size, next_y), 
		(next_x + background_dim*block_size, next_y + (background_dim*block_size)),
		border_size)


def update_score(new_score):

	# Checks whether new_score is greater than the current score.
	# Updates if true.
	#
	# param new_score 		New score achieved
    #score, gen_score = get_max_score()

    with open('scores.txt', 'w') as f:
    	f.write(str(new_score)+'\n'+str(GEN))


def get_max_score():

	# Gets current max score from score.txt file

	with open('scores.txt', 'r') as f:
		lines = f.readlines()
		score = lines[0].strip()
		gen_score = lines[1].strip()

	return score, gen_score


def main(genomes, config):

	# Runs the entire program
	#
	# param genomes 	Maximum number of generations	
	# param config 		Configurations

	global GEN
	GEN += 1

	nets = []
	ge = []
	boards = []
	current_pieces = []
	next_pieces = []

	used_pieces = []
	seeds = [random.randrange(0,7),	# ensure all random pieces are same for all boards
			 random.randrange(0,7)]	

	game_score, game_gen_score = get_max_score()


	for _, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		
		boards.append(Board())

		g.fitness = 0
		ge.append(g)

		current_pieces.append(Piece(3,0, seeds[0]))
		next_pieces.append(Piece(3,0, seeds[1]))

		used_pieces.append(1)


	run = True
	while run:
		
		win = pygame.display.set_mode((win_width, win_height))

		# Keyboard functions
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False


		for x, (current_piece, board) in enumerate(zip(current_pieces, boards)):

			
			# Heuristics inputs for current piece position
			middle_input = board.input_data(current_piece)

			# Heuristics inputs for +/- 1 in x position of current piece position
			current_piece.x -= 1
			if board.update_validation(current_piece):
				left_input = board.input_data(current_piece)
			else: 
				left_input = middle_input
			current_piece.x += 1

			current_piece.x += 1
			if board.update_validation(current_piece):
				right_input = board.input_data(current_piece)
			else: 
				right_input = middle_input
			current_piece.x -= 1			


			# Inference
			outputs = nets[x].activate((
				current_piece.index,
				current_piece.rotation,
				next_pieces[x].index,
				*left_input,
				*middle_input,
				*right_input))

			output = np.argmax(outputs)


			if output == 0: #LEFT
				current_piece.x -= 1
				if not board.update_validation(current_piece):
					current_piece.x += 1

			if output == 1: #RIGHT
				current_piece.x += 1
				if not board.update_validation(current_piece):
					current_piece.x -= 1

			if output == 2: #ROTATE
				current_piece.rotation += 1
				if not board.update_validation(current_piece):
					current_piece.rotation -= 1

			if output == 3: #SOFT DROP
				current_piece.y += 1
				if not board.update_validation(current_piece):
					current_piece.y -= 1

			
			# Make tetromino fall
			current_piece.y += 1
			if not board.update_validation(current_piece):	# If tetromino can not fall any further
				current_piece.y -= 1
				board.lock_piece(current_piece) 			# Locks piece at end of fall

				used_pieces[x] += 1
				if len(seeds) <= used_pieces[x]:
					seeds.append(random.randrange(0,7))

				current_pieces[x] = next_pieces[x]			# Change current piece and upcoming piece
				next_pieces[x] = Piece(3,0, 
					seeds[used_pieces[x]])

				board.score += 1							# +1 gained for soft dropping


			# Update score and fitness
			board.scoring()
			if board.score > int(game_score):
				game_score = board.score
				game_gen_score = GEN
				update_score(game_score)

				# Saves the NN with the best score
				with open('game_best.pickle','wb') as handle:
					pickle.dump(ge[x], handle, protocol=pickle.HIGHEST_PROTOCOL)

			ge[x].fitness = board.score
			board.update_board(current_piece)


			# Game lost; blocks above maximum height
			if not all([board.locked_board[4][i] == (255,255,255) for i in range(10)]):
				nets.pop(x)
				ge.pop(x)
				current_pieces.pop(x)
				next_pieces.pop(x)
				boards.pop(x)


		if len(boards) > 0:
			draw_window(win, boards[0], next_pieces[0], len(boards), game_score, game_gen_score)
		else:
			run = False
			break

		pygame.display.update()



def replay_genome(config_path, genome_path="game_best.pickle"):
	# Load requried NEAT config
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
						neat.DefaultSpeciesSet, neat.DefaultStagnation, 
						config_path)

	# Unpickle saved winner
	with open(genome_path, "rb") as f:
	    genome = pickle.load(f)

	# Convert loaded genome into required data structure
	genomes = [(1, genome)]

	# Call game with only the loaded genome
	main(genomes, config)

#replay_genome('config-feedforward.txt')



def run(config_file):

	# Load requried NEAT config
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner = p.run(main, 100)							# Amount of genomes
	with open('game_winner.pickle', 'wb') as f:			# Save when NN hits fitness level
		pickle.dump(winner,f)
		f.close()

	print('\nBest genome:\n{!s}'.format(winner))


if __name__ =="__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-feedforward.txt")
	run(config_path)