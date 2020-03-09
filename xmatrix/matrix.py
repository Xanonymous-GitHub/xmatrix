"""
    Copyright (C) 2020 By Xanonymous All Rights Reserved.
    Visit My GitHub:https://github.com/Xanonymous-GitHub
    This package is formatted by python official coding style linter (PEP8).
    More style details on:https://www.python.org/dev/peps/pep-0008
"""


class Matrix:
    """Define the Matrix class"""

    def __init__(self, u: str or list):
        if not isinstance(u, list):
            u = u.split(";")
            for i, _ in enumerate(u):
                u[i] = u[i].split(",")
                for j, y in enumerate(u[i]):
                    try:
                        tmp = float(y)
                        u[i][j] = tmp if tmp != int(tmp) else int(tmp)
                    except ValueError:
                        self.__error_handler("Invalid inputs.")
                        self.__del__()
                        return
        if not self.__valid(u):
            self.__error_handler("Error: Invalid matrix.")
            self.__del__()
            return
        self.__storage = u

    def __str__(self):
        return self.__pretty(self.__storage)

    def __del__(self):
        del self

    # Matrix addition or subtraction.
    def __add__(self, other, t=True):
        # If the matrices cannot be added or subtracted, throw an error.
        other = other.raw
        if not (self.__valid(self.__storage) and self.__valid(other) and (
                len(self.__storage) == len(other) and len(self.__storage[0]) == len(other[0]))):
            return self.__error_handler("These two matrices cannot be added or subtracted together.")
        new = list()
        for i, x in enumerate(other):
            new_tmp = list()
            for j, y in enumerate(x):
                new_tmp.append(self.__storage[i][j] + y * (1 if t else -1))
            new.append(new_tmp)
        return Matrix(new)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(other, False)

    # Matrix multiplication
    def __mul__(self, other):
        if isinstance(other, int):
            # method accept single integer to be calculated.
            new = list()
            for i, x in enumerate(self.__storage):
                new_tmp = list()
                for _, y in enumerate(x):
                    new_tmp.append(y)
                new.append(new_tmp)
            return Matrix(self.__rate(new, other))
        # If the matrices cannot be multiplied, throw an error.
        resource = other.raw
        if not self.__valid(resource):
            self.__error_handler("Invalid matrix.")
            return
        for g in self.__storage:
            if not len(g) == len(resource):
                self.__error_handler("Cannot be multiplied.")
                return
        # if the second matrix is an identity_matrix, the answer will be the same as first matrix.
        if self.is_unit_matrix(resource):
            new = self.__storage[:].copy()
            return Matrix(new)
        new = list()
        for i, x in enumerate(self.__storage):
            tmp_slice = list()
            for n in self.__transpose(resource):
                tmp_num = list()
                for j, y in enumerate(x):
                    tmp_num.append(y * n[j])
                tmp_slice.append(sum(tmp_num))
            new.append(tmp_slice)
        return Matrix(new)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power: int, modulo=None):
        if self.is_unit_matrix(self.__storage) or power == 1:
            new = self.__storage[:].copy()
            return Matrix(new)
        if not power:
            n = len(self.__storage)
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
            return Matrix(tmp)
        if not len(self.__storage) == len(self.__storage[0]):
            self.__error_handler("Unable to calculate power, not square.")
            return
        tmp = Matrix(self.__storage[:].copy())
        for x in range(power - 1):
            self.__storage = self.__mul__(tmp).raw
        new = self.__storage[:].copy()
        self.__storage = tmp.raw[:].copy()
        return Matrix(new)

    def __eq__(self, other):
        return other.raw == self.__storage

    @property
    def inverse(self):
        def make_new(old):
            new_thing = list()
            for _, xx in enumerate(old):
                new_tmp = list()
                for _, yy in enumerate(xx):
                    new_tmp.append(yy)
                new_thing.append(new_tmp)
            return new_thing

        determinant = self.__determinant(self.__storage)
        if not determinant:
            self.__error_handler("The determinant is zero, can't be inverse.")
            return
        if len(self.__storage) == 1:
            new = make_new(self.__storage[:].copy())
            new[0][0] = new[0][0] ** -1
            return Matrix(new)
        if len(self.__storage) == 2:
            new = make_new(self.__storage[:].copy())
            new[0][0], new[1][1] = new[1][1], new[0][0]
            new[0][1] *= -1
            new[1][0] *= -1
            new = self.__rate(new, 1 / determinant)
            return Matrix(new)
        ans = list()
        new = make_new(self.__storage[:].copy())
        for i, x in enumerate(self.__storage):
            ans_tmp = list()
            for j, y in enumerate(x):
                h = (-1 if i % 2 else 1) * (-1 if j % 2 else 1)
                ans_tmp.append(h * self.__determinant(self.__get_ans_range(i, j, new)))
            ans.append(ans_tmp)
        ans = self.__transpose(ans)
        new = self.__rate(ans, 1 / determinant)
        return Matrix(new)

    @property
    def transpose(self):
        new = self.__storage[:].copy()
        return Matrix(self.__transpose(new))

    def __determinant(self, r) -> int or float:
        if not self.__valid(r):
            self.__error_handler("Invalid matrix.")
            return
        if not len(r) == len(r[0]):
            self.__error_handler("Can't get the determinant of this matrix.")
            return
        if len(r) == 1:
            return r[0]
        if len(r) == 2:
            return r[0][0] * r[1][1] - r[0][1] * r[1][0]
        result = list()
        for i, x in enumerate(r[0]):
            h = (-1 if i % 2 else 1)
            result.append(
                self.__determinant(self.__magnification_iteration(self.__get_ans_range(0, i, r), h * x)))
        return sum(result)

    def __valid(self, r) -> bool:
        if not r:
            self.__error_handler("Empty matrix")
            return False
        for p in range(len(r) - 1):
            if len(r[p]) != len(r[p + 1]):
                return False
        return True

    @property
    def raw(self) -> list:
        # get the real value of the object
        return self.__storage

    @staticmethod
    def __pretty(r) -> str:
        # Detect if the value can be an integer.
        for i, x in enumerate(r):
            for j, y in enumerate(x):
                if abs(r[i][j] - int(r[i][j])) < 10 ** -3:
                    r[i][j] = int(r[i][j])
        # format the value then return
        return '\n'.join(map(str, r)) + '\n'

    @staticmethod
    def __error_handler(msg):
        print(msg)

    @staticmethod
    def __transpose(resource: list) -> list:
        return list(map(list, zip(*resource)))

    @staticmethod
    def is_unit_matrix(resource: list) -> bool:
        for i, x in enumerate(resource):
            for j, y in enumerate(x):
                if i == j and resource[i][j] != 1:
                    return False
                if y != 0:
                    return False
        return True

    @staticmethod
    def __get_ans_range(ii, jj, resource: list) -> list:
        ans = list()
        for i, x in enumerate(resource):
            tmp_slice = list()
            for j, y in enumerate(x):
                if not (i == ii or j == jj):
                    tmp_slice.append(y)
            if tmp_slice:
                ans.append(tmp_slice)
        return ans

    @staticmethod
    def __rate(r, rate) -> list:
        new = r[:].copy()
        for i, x in enumerate(new):
            for j, y in enumerate(x):
                new[i][j] = rate * r[i][j]
        return new

    @staticmethod
    def __magnification_iteration(r: list, rate) -> list:
        for i, x in enumerate(r):
            r[i][0] *= rate
        return r


class UnitMatrix(Matrix):
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

    def __str__(self):
        return super().__str__()
