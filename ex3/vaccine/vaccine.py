import sys
import time

DEBUG = False

BLUE = '\033[94m'
GREEN = '\033[92m'
ENDC = '\033[0m'
RED = '\033[91m'


class rna_data:
    def __init__(self,
                 initial_rna_sequence,
                 final_rna_sequence=None,
                 correction=None,
                 initial_size=None):
        self.initial_size = initial_size if initial_size != None else len(
            initial_rna_sequence)

        if (type(initial_rna_sequence) == str):
            self.initial_rna_sequence = list(initial_rna_sequence)
        else:
            self.initial_rna_sequence = initial_rna_sequence

        if (final_rna_sequence == None):
            self.final_rna_sequence = list()
        elif (type(final_rna_sequence) == str):
            self.final_rna_sequence = list(final_rna_sequence)
        else:
            self.final_rna_sequence = final_rna_sequence

        self.correction = correction
        if (correction == None):
            self.correction = 'n'
        elif (correction == 'p'):
            self.push()
        elif (correction == 'c'):
            self.complement()
        elif (correction == 'r'):
            self.reverse()

    def push(self):
        if (self.initial_size == 0):
            return
        base = self.initial_rna_sequence.pop()
        self.final_rna_sequence.insert(0, base)
        self.initial_size -= 1

    def complement(self):
        for i in range(len(self.initial_rna_sequence)):
            if (self.initial_rna_sequence[i] == "A"):
                self.initial_rna_sequence[i] = "U"
            elif (self.initial_rna_sequence[i] == "C"):
                self.initial_rna_sequence[i] = "G"
            elif (self.initial_rna_sequence[i] == "G"):
                self.initial_rna_sequence[i] = "C"
            elif (self.initial_rna_sequence[i] == "U"):
                self.initial_rna_sequence[i] = "A"

    def reverse(self):
        self.final_rna_sequence.reverse()

    def is_valid(self):
        if (self.initial_size != 0):
            return False
        found = set()
        previous = None

        for b in self.final_rna_sequence:
            if (b not in found):
                found.add(b)
                previous = b
            if (b in found and previous == b):
                continue
            if (b in found and previous != b):
                return False
        return True


def debug(rna: rna_data, msg="", color=RED):
    print(color + msg + "{}({}) -> {} ".format(
        rna.initial_rna_sequence, rna.initial_size, rna.final_rna_sequence))


def bfs(initial_rna):
    parent = {initial_rna: None}
    frontier = [initial_rna]
    while frontier:
        next = []
        for u in frontier:
            if (u.initial_size == 0):
                debug(u, "size satisfied ", BLUE)
                if (u.is_valid()):
                    # final rna sequence found, now recreating steps
                    final = u

                    moves = []
                    moves_append = moves.append

                    while not final.correction == 'n':
                        moves_append(final.correction)
                        final = parent[final]

                    moves.reverse()
                    return "".join(moves)

            temp_initial_rna = u.initial_rna_sequence
            temp_final_rna = u.final_rna_sequence
            temp_size = u.initial_size

            if (u.initial_size != 0):
                p = rna_data(temp_initial_rna.copy(), temp_final_rna.copy(),
                             'p', temp_size)
                c = rna_data(temp_initial_rna.copy(), temp_final_rna, 'c',
                             temp_size)
            else:
                p = None
                c = None

            r = rna_data(temp_initial_rna, temp_final_rna.copy(), 'r',
                         temp_size)

            if (u.initial_size != 0):
                corrections = [c, p, r]
            else:
                corrections = [r]

            for v in corrections:
                if (v not in parent):
                    debug(v, "not in dict ")
                    parent[v] = u
                    next.append(v)

        frontier = next


def main(argv):
    filename = "testcases/vaccine.in1"
    # if (len(argv) != 2):
    #     print("Expected 1 argument, got", len(argv) - 1)
    #     exit(2)
    # filename = argv[1]

    sum_time = 0
    with open(filename, 'rt') as fn:
        count_bases = int(fn.readline())
        for i in range(count_bases):
            if DEBUG:
                s = time.time()
            base = rna_data(fn.readline()[:-1])
            res = bfs(base)

            if DEBUG:
                print(res, end=" - ")
                e = time.time()
                sum_time += e - s
                print(BLUE + "TEST TIME:", e - s, GREEN + "TOTAL TIME:",
                      sum_time, ENDC)
            else:
                print(res)


if __name__ == "__main__":
    main(sys.argv)
