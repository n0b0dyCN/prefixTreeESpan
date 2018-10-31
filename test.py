
from prefixTreeESpan import build_tree, TreeDB


def readin(fn):
    tdb = TreeDB()
    idx = 0
    with open(fn, "r") as f:
        for line in f:
            tdb.push(build_tree(line.strip().split(' ')), idx)
            idx += 1


def main():
    pass


if __name__ == '__main__':
    main()