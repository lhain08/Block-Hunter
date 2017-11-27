class floor():
    def __init__(self,a,height,left,right):
        self.a = a
        self.left = left
        self.right = right
        self.height = height

#         0                       1                         2                             3                            4                              5                        6                             7                               8                          9                       10                        11                          12                        13                        14                          15                           16                           17                         18
floors = [floor([2],1180,20,1185),floor([4],1180,1215,1780),floor([0,5,6,9],1060,300,600),floor([6,7,8],1060,915,1185),floor([1,7,12],1060,1500,1780),floor([2,13],940,20,300),floor([2,3,8,10],940,600,915),floor([3,4,8,11],940,1185,1500),floor([6,7],840,1000,1100),floor([13],840,520,600),floor([6,14],840,620,700),floor([7,15],840,1400,1480),floor([16],840,1500,1580),floor([9,17],720,300,520),floor([10,17],720,800,1035),floor([11,18],720,1065,1300),floor([12,18],720,1580,1780),floor([13,14],590,520,700),floor([15,16],590,1400,1580)]


def Test(s,f):
    global Path, best
    for i in floors[f].a:
        x = i
        if x not in Path:
            Path.append(x)
            if x == s:
                if len(Path)<len(best):
                    best = Path
            else:
                Test(s,x)
            if x in Path:
                Path.remove(x)

def T(s,f):
    global Path, fast
    for i in floors[f].a:
        if i not in Path:
            Path.append(i)
            if s == Path[len(Path)-1]:
                if not fast or len(Path)<len(fast):
                    fast = []
                    for x in Path:
                        fast.insert(0,x)
            else:
                T(s,i)
            if i in Path:
                Path.remove(i)


def Check(s,f):
    if s != f:
        global Path, fast
        Path = []
        fast = []
        T(s,f)
        fast.append(f)
        return fast
