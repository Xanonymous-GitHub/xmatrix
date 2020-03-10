"""
    Copyright (C) 2020 By Xanonymous All Rights Reserved.
    Visit My GitHub:https://github.com/Xanonymous-GitHub
    This package is formatted by python official coding style linter (PEP8).
    More style details on:https://www.python.org/dev/peps/pep-0008
"""

from math import isclose


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
            new = self.__make_copy(self.__storage)
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
            new = self.__make_copy(self.__storage)
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
        # if self is an identity matrix or power assign 1, than return self.
        if self.is_unit_matrix(self.__storage) or power == 1:
            return Matrix(self.__make_copy(self.__storage))
        # if power == 0, than return identity matrix.
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
        # if the matrix is not a square or invalid, return error.
        if not len(self.__storage) == len(self.__storage[0]):
            self.__error_handler("Unable to calculate power, not square.")
            return
        # if the power < 0, recursive the positive power by self inverse.
        tmp = Matrix(self.__make_copy(self.__storage))
        if power < 0:
            tmp = tmp.inverse
            if tmp is not None:
                return tmp ** (power * -1)
            return self.__error_handler("Unable to calculate power, determinant is zero.")
        # calculate the positive power value of this matrix.
        for x in range(power - 1):
            self.__storage = self.__mul__(tmp).raw
        new = self.__make_copy(self.__storage)
        self.__storage = self.__make_copy(tmp.raw)
        return Matrix(new)

    def __eq__(self, other):
        return other.raw == self.__storage

    @property
    def inverse(self):
        determinant = self.__determinant(self.__storage)
        if not determinant:
            self.__error_handler("The determinant is zero, can't be inverse.")
            return
        new = self.__make_copy(self.__storage)
        if len(self.__storage) == 1:
            new[0][0] = new[0][0] ** -1
            return Matrix(new)
        if len(self.__storage) == 2:
            new[0][0], new[1][1] = new[1][1], new[0][0]
            new[0][1] *= -1
            new[1][0] *= -1
            return Matrix(self.__rate(new, 1 / determinant))
        ans = list()
        for i, x in enumerate(self.__storage):
            ans_tmp = list()
            for j, y in enumerate(x):
                h = (-1 if i % 2 else 1) * (-1 if j % 2 else 1)
                ans_tmp.append(h * self.__determinant(self.__get_ans_range(i, j, new)))
            ans.append(ans_tmp)
        ans = self.__transpose(ans)
        return Matrix(self.__rate(ans, 1 / determinant))

    @property
    def transpose(self):
        return Matrix(self.__transpose(self.__make_copy(self.__storage)))

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

    def __pretty(self, r) -> str:
        # Detect if the value can be more short.
        for i, x in enumerate(r):
            for j, y in enumerate(x):
                # try to turn the data to integer.
                if abs(r[i][j] - int(r[i][j])) < 10 ** -4:
                    r[i][j] = int(r[i][j])
                # the max floating point length in python is 16 so we use 15 to calculate.
                if isinstance(r[i][j], float):
                    r[i][j] = self.__get_near_number(r[i][j], 15)
        # format the value then return
        return '\n'.join(map(str, r)) + '\n'

    @staticmethod
    def __error_handler(msg):
        return print(msg)

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

    @staticmethod
    def __make_copy(old: list) -> list:
        new = list()
        for _, x in enumerate(old):
            new_tmp = list()
            for _, y in enumerate(x):
                new_tmp.append(y)
            new.append(new_tmp)
        return new

    # find the max nearly round number of the float value.
    def __get_near_number(self, data: float, pos: int) -> int or float:
        if not isclose(data, round(data, pos), rel_tol=1e-4):
            return round(data, pos + 1)
        return self.__get_near_number(data, pos - 1)


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
