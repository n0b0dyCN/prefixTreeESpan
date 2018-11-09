from optparse import OptionParser
from time import time


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
    def __init__(self, min_propotion, inf, outf):
        self.min_propotion = min_propotion
        self.tdb = []
        self.results = []
        self.inf = inf
        self.outf = outf
        self.min_sup = -1
        self.t_start = None
        self.t_stop = None

        self.cnt_one_level_patterns = {}
    
    def readin(self):
        cnt = 0
        with open(self.inf, "r") as f:
            for line in f.readlines():
                cnt += 1
                l = line.strip().split(' ')
                root = Node(l[0])
                stk = [(root, 0)]
                ptr = 1
                tree = [root]
                while stk:
                    _node = Node(l[ptr])
                    if _node.label == '-1':
                        stk[-1][0].e = ptr
                        stk.pop()
                    else:
                        stk.append((_node, ptr))
                    tree.append(_node)
                    ptr += 1
                self.tdb.append(tree)

                labels = set([
                    (_node.label, 0) for _node in tree if _node.label != '-1'
                ])
                for patt in labels:
                    if patt not in self.cnt_one_level_patterns:
                        self.cnt_one_level_patterns[patt] = 0
                    self.cnt_one_level_patterns[patt] += 1
        self.min_sup = int(self.min_propotion * float(len(self.tdb)))
        print ("%d trees read in." % (len(self.tdb)))
        print ("min_sup: ", self.min_sup)
        #exit(0)

    def add_result(self, tree):
        self.results.append(tree)

    def output_result(self):
        with open(self.outf, "w") as f:
            timer = "Time: %.04f secends.\n" % (self.t_stop - self.t_start)
            f.write(timer)
            for each in self.results:
                print each
                f.write(" ".join(each) + "\n")

    def get_frequent_labels(self):
        patterns = [
            p[0] for p in self.cnt_one_level_patterns if self.cnt_one_level_patterns[p] > self.min_sup
        ]
        return patterns

    def fre(self, pre_tree, n, proj_db):
        pattern_cnt = {}
        for proj in proj_db:
            tree = self.tdb[proj.tid]
            for i in range(len(proj.s)):
                for j in range(proj.s[i], proj.e[i]):
                    if tree[j].label != '-1':
                        patt = (tree[j].label, i+1)
                        if patt not in pattern_cnt:
                            pattern_cnt[patt] = set([])
                        pattern_cnt[patt].add(proj.tid)

        fre_patts = set([p for p in pattern_cnt if len(pattern_cnt[p])>self.min_sup])

        for fre_patt in fre_patts:
            new_pre_tree = pre_tree
            new_pre_tree.insert(-fre_patt[1], fre_patt[0])
            new_pre_tree.insert(-fre_patt[1], '-1')
            self.add_result(new_pre_tree)

            pdb = []
            for i in range(len(proj_db)):
                proj = proj_db[i]
                tree = self.tdb[proj.tid]
                for c in range(len(proj.s)):
                    for k in range(proj.s[c], proj.e[c]):
                        if tree[k].label == fre_patt[0]:
                            proj_new = Project(proj.tid)
                            if tree[k+1].label != '-1':
                                proj_new.add(n+1, tree[n].e)
                            ss = tree[k].e + 1
                            while tree[ss].label != '-1' and ss < proj.e[c]:
                                proj_new.add(ss, tree[ss].e)
                                ss = tree[ss].e + 1
                            pdb.append(proj_new)
            self.fre(new_pre_tree, n+1, pdb)

        pass

    def run(self):
        self.t_start = time()
        self.readin()
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
            
            self.fre(prefix_subtree, 1, project_db)
        self.t_stop = time()
        self.output_result()
        pass


def main():
    parser = OptionParser("Help for prerixTreeESpan",
        description="PrefixTreeESpan algorithm implemented in python.",
        version="1.0"
    )
    parser.add_option("-i", "--input", action="store", dest="input", help="Input file")
    parser.add_option("-o", "--output", action="store", dest="output", help="Output file")
    parser.add_option("-m", "--minsup", action="store", dest="ms", type=float, help="Output file")

    options, args = parser.parse_args()

    p = PrefixTreeESpan(options.ms, options.input, options.output)
    p.run()

if __name__ == '__main__':
    main()