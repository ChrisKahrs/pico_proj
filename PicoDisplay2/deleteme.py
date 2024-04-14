'''
Create a function that does MCTS on a given board game state for tic-tac-toe
'''

def mcts(board, player, n):
    # Create a root node for the search tree
    root = Node(board, player)
    # Run n simulations
    for i in range(n):
        # Create a copy of the root node
        node = root.copy()
        # Run a simulation from the node
        node.simulate()
        # Backpropagate the result
        node.backpropagate()
    # Return the best move
    return root.best_move()

def Node(board, player):
    # Create a node object
    node = {
        'board': board,
        'player': player,
        'children': [],
        'visits': 0,
        'score': 0
    }
    return node

def copy(node):
    # Copy a node object
    return {
        'board': node['board'][:],
        'player': node['player'],
        'children': node['children'][:],
        'visits': node['visits'],
        'score': node['score']
    }
    
def simulate(node):
    # Run a simulation from a given node
    # Check if the node is a terminal node
    if terminal(node['board']):
        # Return the result of the game
        return result(node['board'])
    # Check if the node has any children
    if len(node['children']) == 0:
        # Expand the node
        expand(node)
        # Select a random child
        child = random.choice(node['children'])
        # Simulate from the child node
        result = simulate(child)
    else:
        # Select the child with the best UCB score
        child = best_child(node)
        # Simulate from the child node
        result = simulate(child)
    # Update the node's visits and score
    node['visits'] += 1
    node['score'] += result
    # Return the result
    return result

def expand(node):
    # Expand a node by adding all possible child nodes
    # Get the board from the node
    board = node['board']
    # Get the player from the node
    player = node['player']
    # Get the opponent from the player
    opponent = opponent(player)
    # Get the possible moves from the board
    moves = possible_moves(board)
    # Loop through the possible moves
    for move in moves:
        # Create a child node
        child = Node(board[:], opponent)
        # Make the move on the child node's board
        child['board'][move] = player
        # Add the child node to the node's children
        node['children'].append(child)
        
def best_child(node):
    # Select the child with the best UCB score
    # Get the player from the node
    player = node['player']
    # Get the children from the node
    children = node['children']
    # Initialize the best child and best score
    best_child = None
    best_score = -1
    # Loop through the children
    for child in children:
        # Calculate the child's UCB score
        score = ucb_score(child, player)
        # Check if the score is better than the best score
        if score > best_score:
            # Update the best child and best score
            best_child = child
            best_score = score
    # Return the best child
    return best_child

def ucb_score(node, player):
    # Calculate the UCB score of a node
    # Get the node's score and visits
    score = node['score']
    visits = node['visits']
    # Get the parent's visits
    parent_visits = node['parent']['visits']
    # Calculate the UCB score
    return score / visits + 2 * math.sqrt(math.log(parent_visits) / visits)

def backpropagate(node):
    # Backpropagate the result of a simulation
    # Check if the node has a parent
    if node['parent'] != None:
        # Backpropagate the result from the parent
        backpropagate(node['parent'])
    # Update the node's visits and score
    node['visits'] += 1
    node['score'] += result
    
def best_move(node):
    # Select the best move from a given node
    # Initialize the best move and best score
    best_move = None
    best_score = -1
    # Get the children from the node
    children = node['children']
    # Loop through the children
    for child in children:
        # Calculate the child's score
        score = child['score']
        # Check if the score is better than the best score
        if score > best_score:
            # Update the best move and best score
            best_move = child['move']
            best_score = score
    # Return the best move
    return best_move

def terminal(board):
    # Check if a board is a terminal board
    # Check if the board is full
    if board_full(board):
        # Return True
        return True
    # Check if the board is won
    if board_won(board):
        # Return True
        return True
    # Return False
    return False

def board_full(board):
    # Check if a board is full
    # Loop through the board
    for cell in board:
        # Check if the cell is empty
        if cell == 0:
            # Return False
            return False
    # Return True
    return True

def board_won(board):
    # Check if a board is won
    # Check if the board is won by a row
    if row_won(board):
        # Return True
        return True
    # Check if the board is won by a column
    if column_won(board):
        # Return True
        return True
    # Check if the board is won by a diagonal
    if diagonal_won(board):
        # Return True
        return True
    # Return False
    return False

def row_won(board):
    # Check if a board is won by a row
    # Loop through the rows
    for row in range(3):
        # Check if the row is won
        if board[row * 3] != 0 and board[row * 3] == board[row * 3 + 1] and board[row * 3] == board[row * 3 + 2]:
            # Return True
            return True
    # Return False
    return False    

def column_won(board):
    # Check if a board is won by a column
    # Loop through the columns
    for column in range(3):
        # Check if the column is won
        if board[column] != 0 and board[column] == board[column + 3] and board[column] == board[column + 6]:
            # Return True
            return True
    # Return False
    return False

def diagonal_won(board):
    # Check if a board is won by a diagonal
    # Check if the board is won by the main diagonal
    if board[0] != 0 and board[0] == board[4] and board[0] == board[8]:
        # Return True
        return True
    # Check if the board is won by the other diagonal
    if board[2] != 0 and board[2] == board[4] and board[2] == board[6]:
        # Return True
        return True
    # Return False
    return False

def result(board):
    # Return the result of a board
    # Check if the board is won by a row
    if row_won(board):
        # Return the winner
        return board[0]
    # Check if the board is won by a column
    if column_won(board):
        # Return the winner
        return board[0]
    # Check if the board is won by a diagonal
    if diagonal_won(board):
        # Return the winner
        return board[0]
    # Return 0
    return 0

def opponent(player):
    # Return the opponent of a player
    return 1 - player

def possible_moves(board):
    # Return the possible moves from a board
    # Initialize the moves list
    moves = []
    # Loop through the board
    for cell in range(9):
        # Check if the cell is empty
        if board[cell] == 0:
            # Add the cell to the moves list
            moves.append(cell)
    # Return the moves list
    return moves

def random_move(board):
    # Return a random move from a board
    # Get the possible moves from the board
    moves = possible_moves(board)
    # Return a random move
    return random.choice(moves)

def print_board(board):
    # Print a board
    # Loop through the rows
    for row in range(3):
        # Print the row
        print(board[row * 3], board[row * 3 + 1], board[row * 3 + 2])
    # Print a newline
    print()

def play_game():
    # Play a game of tic-tac-toe
    # Initialize the board
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # Initialize the player
    player = 0
    # Initialize the opponent
    opponent = 1
    # Initialize the result
    result = 0
    # Start an infinite loop
    while True:
        # Check if the board is full
        if board_full(board):
            # Set the result to a draw
            result = 0
            # Break out of the loop
            break
        # Check if the board is won
        if board_won(board):
            # Set the result to the winner
            result = board[0]
            # Break out of the loop
            break
        # Check if it's the player's turn
        if player == 0:
            # Get the player's move
            move = int(input("Your move: "))
            # Make the move on the board
            board[move] = player
        else:
            # Get the opponent's move
            move = mcts(board, player, 1000)
            # Make the move on the board
            board[move] = player
        # Print the board
        print_board(board)
        # Switch the player and opponent
        player, opponent = opponent, player
    # Print the result
    print("Result:", result)
    
# Play a game of tic-tac-toe
play_game()

# Create a function that does MCTS on a given board game state for tic-tac-toe