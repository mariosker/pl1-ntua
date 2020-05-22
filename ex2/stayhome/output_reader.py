with open("flood10", 'r') as f:
    for line in f:
        line = line.strip("\n")
        coords = line.split("  ")
        for c in coords:
            y = c[1:-1]
            cc = y.split(",")
            a = cc[0]
            b = cc[1]
            if '~' in a:
                a = a.replace('~', '-')
            if '~' in b:
                b = b.replace('~', '-')
            print('({:>3}, {:>3})'.format(a, b), end=" ")
        print()