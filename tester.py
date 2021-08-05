from optimal import main
import string
import random as rd

def iterrows(n):
    letters = iter(string.ascii_lowercase)
    next_len = rd.randint(0, n)
    while n > 0:
        char = next(letters, None)
        if char is None:
            break
        n -= next_len
        yield from (char for _ in range(next_len))

        next_len = rd.randint(0, n)

    while True:
        char = next(letters, 'z')
        yield from (char for _ in range(n))

def generate_input(n, m):
    seen = set()
    lst = list()
    iterators = [iterrows(m) for _ in range(n)]
    while len(seen) < n:
        print(len(seen))
        temp = ''.join(next(i) for i in iterators)
        print(temp)
        added = len(seen) != (seen.add(temp) or len(seen))
        if added:
            lst.append(temp)
            

    return lst


def main():
    print(generate_input(100, 100))
    print('a')

if __name__ == '__main__':
    main()

