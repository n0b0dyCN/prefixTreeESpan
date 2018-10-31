
class Node:
    def __init__(self, tag, scope=0):
        self.tag = tag
        self.scope = scope

class TreeDB:
    def __init__(self):
        self.trees = []



def build_tree(l):
    root = Node(l[0])
    stack = [(root, 0)]
    tree = [root]
    index = 1
    while stack:
        elem = Node(l[index])

