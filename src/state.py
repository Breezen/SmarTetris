CELL_SIZE =	18
COLS =		10
ROWS =		22

BLOCKS = [
	[[1, 1, 1],
	 [0, 1, 0]],

	[[0, 2, 2],
	 [2, 2, 0]],

	[[3, 3, 0],
	 [0, 3, 3]],

	[[4, 0, 0],
	 [4, 4, 4]],

	[[0, 0, 5],
	 [5, 5, 5]],

	[[6, 6, 6, 6]],

	[[7, 7],
	 [7, 7]]
]

ACTIONS = [(n, x) for n in xrange(4) for x in xrange(COLS)]

import copy

# init a board, row length=23, col length= 10
# the board[22] is ground, with a list of 1
def newBoard():
	board = [ [ 0 for x in xrange(COLS) ]
			for y in xrange(ROWS) ]
	board += [[ 1 for x in xrange(COLS)]]
	return board

class State(object):
    def __init__(self, board, score, block, nextBlock):
        self.board = board
        self.score = score
        self.block = block
        self.nextBlock = nextBlock
        self.newScore = score

    def nextStates(self, action):
        rotateN, x = action
        newStates = []
        block = self.rotate(self.block, rotateN)
        if not self.checkCollision(block, (x, 0)):
            newBoard = self.drop(block, x)
            newScore = self.newScore
            newBlock = self.nextBlock
            for newNextBlock in BLOCKS:
                newState = State(newBoard, newScore, newBlock, newNextBlock)
                newStates.append(newState)
        return newStates

    def checkCollision(self, block, offset):
        board = self.board
        x, y = offset
        for blockY, row in enumerate(block):
            for blockX, pixel in enumerate(row):
                #the pos in board has alread existed pixel
                try:
                    if pixel and board[blockY + y][blockX + x]:
                        return True
                #the given position is beyond board
                except IndexError:
          	         return True
        return False

    def rotate(self, block, N):
        for _ in xrange(N):
            block = [[block[y][x]
                      for y in xrange(len(block))]
                      for x in xrange(len(block[0]) - 1, -1, -1)]
        return block

    def drop(self, block, x):
        y = 0
        while not self.checkCollision(block, (x,y)):
            y += 1
        return self.removeRow(self.addBlock(block, (x,y-1)))

    def addBlock(self, block, offset):
        board = copy.deepcopy(self.board)
        x, y = offset
        for blockY, row in enumerate(block):
            for blockX, pixel in enumerate(row):
                #there are an extra line in the board : board[22]
                board[blockY + y][blockX + x] += pixel
        return board

    def removeRow(self, board):
        clearedRows = 0
        for i, row in enumerate(board[:-1]):
            if 0 not in row:
                del board[i]
                board = [[0 for i in xrange(COLS)]] + board
                clearedRows += 1
        self.addScore(clearedRows)
        return board

    def addScore(self, n):
		linescores = [0, 40, 100, 300, 1200]
		# self.newScore = self.score + linescores[n]
		self.newScore = linescores[n]

if __name__ == '__main__':
    testBoard = \
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    testState = State(testBoard, 0, BLOCKS[0], BLOCKS[1])
    print testState.nextStates((1, 2))[0].board
    print testState.board
    print testState.nextStates((1, 2))[0].score
    print testState.nextStates((1, 2))[0].block
