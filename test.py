
from prefixTreeESpan import build_tree


def readin(fn):
    tree_set = []
    with open(fn, "r") as f:
        for l in f.readline():
            tree_set.append(build_tree(l.strip().split(' ')))


def main():
    pass


if __name__ == '__main__':
    main()