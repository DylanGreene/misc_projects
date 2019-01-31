# Markov Chain Babbler - Dylan Greene

import random

class Markov_Babbler():
    def __init__(self, source):
        self.lines = self._read_source(source)
        self.model = {}
        self._build()

    def _read_source(self, source):
        '''read the source file into a list of lists of words (inner list per line)'''
        with open(source, 'r') as f:
            content = f.readlines()
        return [[word for word in line.strip().split()] for line in content]

    def _build(self):
        '''effictively build the markov chain model by simply creating a dictionary
        each key will contain all of the words that chain from that word in the text
        a random sample from the value list will be a probabilistic choice'''
        for line in self.lines:
            # include start and end states for the model
            if '*START*' in self.model:
                self.model['*START*'].append(line[0])
            else:
                self.model['*START*'] = [line[0]]
            line.append('*END*')
            for i in range(len(line)-1):
                key = line[i]
                value = line[i+1]
                if key in self.model:
                    self.model[key].append(value)
                else:
                    self.model[key] = [value]
        return

    def generate(self, n=10):
        '''generate text using the markov model that is n lines long
        the random choice is according to the conditional frequencies since
        each value list contains all following words including duplicates'''
        res = ''
        for i in range(n):
            line = []
            word = random.choice(self.model['*START*'])
            while word != '*END*':
                line.append(word)
                word = random.choice(self.model[word])
            res += ' '.join(line) + '\n'
        return res


if __name__ == '__main__':
    Shakespear_Babbler = Markov_Babbler('sonnets.txt')
    print(Shakespear_Babbler.generate(), end='')
