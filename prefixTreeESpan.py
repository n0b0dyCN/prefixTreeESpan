
class Node:
    def __init__(self, label=""):
        self.label = label
        self.e = -1


class Project:
    def __init__(self, tid):
        self.tid = tid
        self.s = []
        self.e = []
    
    def add(self, s, e):
        self.s.append(s)
        self.e.append(e)


class PrefixTreeESpan:
    def __init__(self, min_sup):
        self.min_sup = min_sup
        self.tdb = []
        self.cnt_patterns = {}
        self.results = []
    
    def readin(fn):
        with open(fn, "r"), as f:
            for line in f:
                l = line.strip().split(' ')
                root = Node(l[0])
                stk = [(root, 0)]
                ptr = 1
                tree = [root]
                while stk:
                    _node = Node(l)
                    if l[ptr] == '-1':
                        stk[-1][0].e = ptr
                        stk.pop()
                    else:
                        stk.append(_node)
                    tree.append(_node)
                self.tdb.append(tree)

                labels = set([
                    (_node.label, 0) for _node in tree if _node.label != '-1'
                ])
                for patt in labels:
                    if patt not in self.cnt_patterns:
                        self.cnt_patterns[patt] = 0
                    self.cnt_patterns += 1

    def add_result(self, tree):
        self.results.append(tree)

    def get_frequent_labels(self):
        patterns = [
            p for p in self.cnt_patterns if cnt_patterns[p] > sels.min_sup
        ]

    def fre(self, pre_tree, n, proj_db):
        for proj in proj_db:
            tree = self.tdb[proj.tid]
            for i in range(len(proj.s)):
                for j in range
        pass

    def run(self):
        fre_labels = self.get_frequent_labels()
        for fre_lb in fre_labels:
            prefix_subtree = [fre_lb, '-1']
            self.add_result(prefix_subtree)
            project_db = []
            for i in range(len(self.tdb)):
                tree = self.tdb[i]
                for j in range(len(tree)):
                    if tree[j].label == prefix_subtree[0] and tree[j+1].label != '-1':
                        proj = Project(i)
                        proj.add(j+1, tree[j+1].e)
                        project_db.append(proj)
            
            fre(prefix_subtree, 1, project_db)
        pass



