# Dylan Greene
# 8-Queens Game Local Search Solution

import random

class Board:
    def __init__(self, n=8):
        self._create_board(n)
        self.n = n

    def _create_board(self, n):
        # init a random board
        b = [['0' for _ in range(n)] for _ in range(n)]
        for i in range(n): # one queen per column randomly placed
            b[random.randint(0, n-1)][i] = 'Q'
        self.board = b

    def __str__(self):
        return '\n'.join(map(' '.join, self.board))

    def _get_conflicted(self):
        # return a random conflicted queen position
        indices = [(r, c) for c in range(self.n) for r in range(self.n)]
        random.shuffle(indices)
        for r, c in indices:
            if self.board[r][c] == 'Q' and self._num_conflicts(r, c) > 0:
                return (r, c)
        return None

    def _num_conflicts(self, r, c):
        # implements the requested heuristic
        # all adjacent queens in a row, col, or diag contribute to the conflict val
        n = 0
        for i, j in [(i, j) for j in range(self.n) for i in range(self.n)]:
            if (i, j) == (r, c) and self.board[i][j] == 'Q':
                continue
            # row conflicts:
            if i == r and self.board[i][j] == 'Q':
                n+=1
            # column conflicts
            if j == c and self.board[i][j] == 'Q':
                n+=1
            # diag conflicts
            if abs(i-r) == abs(j-c) and self.board[i][j] == 'Q':
                n+=1
        return n

    def solve(self, max_steps=1000):
        return self._min_conflicts(max_steps)

    def _min_conflicts(self, max_steps): # this performs the local search
        steps_taken = 0
        for i in range(max_steps):
            current = self._get_conflicted()
            if current == None: # goal check
                return (True, steps_taken)
            # find the accessible location which minimizes the conflicts
            value = self._get_value(current[0], current[1])
            # update the board by moving to the new local min
            self.board[value[0]][value[1]] = 'Q'
            self.board[current[0]][current[1]] = '0'
            steps_taken += 1
        return (False, steps_taken) # failure, unable to find solution

    def _get_value(self, r, c):
        conflicts = {}
        for i in range(self.n):
            if i != r: # cannot stay in the same spot even if it has min conflicts
                conflicts[(i, c)] = self._num_conflicts(i, c)
        return min(conflicts, key=conflicts.get)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Solve the N-Queens Puzzle')
    parser.add_argument('--bench', action='store_true', help='benchmark the solution (avg of 1000)')
    parser.add_argument('-n', type=int, default=8, help='number of queens/board size')
    parser.add_argument('--steps', type=int, default=1000, help='max steps to solve')
    args = parser.parse_args()

    if args.bench:
        count = 0
        trials = 5000
        num_solved = 0
        for i in range(trials):
            board = Board(args.n)
            is_solved, steps = board.solve(args.steps)
            if is_solved:
                count += steps
                num_solved += 1
        print('Average moves:', round(count/trials, 2))
        print('Number solved:', num_solved, 'out of', trials)
    else:
        board = Board(args.n)
        print('Initial game state:')
        print(board)
        is_solved, steps = board.solve(args.steps)
        if is_solved:
            print('Solution:')
            print(board)
        else:
            print('Failed to solve in {} steps'.format(args.steps))
            print(board)
