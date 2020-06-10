from .matrix import Matrix


class IdentityMatrix(Matrix):
    def __init__(self, n):
        tmp_n = n
        tmp = list()
        while tmp_n:
            tmp_tmp = list()
            m = n
            while m:
                tmp_tmp.insert(0, 1 if m == tmp_n else 0)
                m -= 1
            tmp.insert(0, tmp_tmp)
            tmp_n -= 1
        super().__init__(tmp)


ixm = IdentityMatrix
