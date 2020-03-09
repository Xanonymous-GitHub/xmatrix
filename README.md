# Xmatrix
<p align="center">
  <a href="https://vuetifyjs.com" target="_blank">
    <img alt="xmatrixy Logo" width="80%" src="https://shakgq.bn.files.1drv.com/y4mzPvS0o0AAP6iY562jnqb5ySw_gNZmIFWDZeRCA1s2kManlXFgnVgvl6Ujj3YHtJUXoA6KByG4sfd75FDccHT_3qXa7oL7phHvCt_EypVlmbQs917gPxU1zelKr1UKvUSavFOInBi3lNEclw6h9lB2oA_azKhgbaRoGrlRm36OsWXLmhD2mXlA_jzJFDAla8TjsRhkVAEbsH7KR6WyTUA6g?width=1024&height=678&cropmode=none">
  </a>
</p>

![](https://img.shields.io/pypi/v/xmatrix.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/xanonymous-github/xmatrix/badge)](https://www.codefactor.io/repository/github/xanonymous-github/xmatrix)
- A python package to calculate Matrix math problems.
- python version: 3.6 and above.

### Usage
#### install
```bash
pip install xmatrix
```
#### Add import in your file
```python
import xmatrix as Mx
from xmatrix import * # This would be better.
```
#### create a matrix
- Matrix("<b>row</b> ; <b>row</b> ...")
```python
my_matrix = Mx.Matrix("1,2;3,4")

#result:
[1, 2]
[3, 4]
```
#### we also support bigger matrix
```python
my_matrix = Mx.Matrix("1,2,3;4,5,6;7,8,9")

#result:
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
```

#### simple calculate
```python
my_matrix = Mx.Matrix("1,2;3,4")
my_matrix2 = Mx.Matrix("4,6;2,9")

print(my_matrix + my_matrix2)
#result:
[5, 8]
[5, 13]

print(my_matrix - my_matrix2)
#result:
[-3, -4]
[1, -5]

print(my_matrix * my_matrix2)
#result:
[8, 24]
[20, 54]

print(my_matrix * 87)
#result:
[87, 174]
[261, 348]

print(my_matrix ** 7)
#result:
[30853, 44966]
[67449, 98302]

print(my_matrix == my_matrix2)
#result:
False
```
#### Transpose Matrix
```python
my_matrix = Mx.Matrix("1,2,3;4,5,6;7,8,9")

print(my_matrix)
#result:
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]

print(my_matrix.transpose)
#result:
[1, 4, 7]
[2, 5, 8]
[3, 6, 9]

my_matrix2 = Matrix("1,2,3,4;5,6,7,8;9,10,11,12;13.1,14.2,15.3,16.4")

print(my_matrix2)
#result:
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13.1, 14.2, 15.3, 16.4]

print(my_matrix2.transpose)
#result:
[1, 5, 9, 13.1]
[2, 6, 10, 14.2]
[3, 7, 11, 15.3]
[4, 8, 12, 16.4]
```
#### Inverse
```python
my_matrix = Mx.Matrix("1,2;3,4")

print(my_matrix)
#result:
[1, 2]
[3, 4]

print(my_matrix.inverse)
#result:
[-2, 1]
[1.5, -0.5]

my_matrix2 = Mx.Matrix("1,2,3;4,5,6;7,8,9")

print(my_matrix2)
#result:
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]

print(my_matrix2.inverse)
#result:
#The determinant is zero, can't be inverse.
#None

my_matrix3 = Mx.Matrix("1,1,1;1,2,3;1,4,5")

print(my_matrix3)
#result:
[1, 1, 1]
[1, 2, 3]
[1, 4, 5]

print(my_matrix3.inverse)
#result:
[1, 0.5, -0.5]
[1, -2, 1]
[-1, 1.5, -0.5]

my_matrix4 = Mx.Matrix("1,1,2,1;1,1,0,0;1,1,0,1;1,0,1,0")

print(my_matrix4)
#result:
[1, 1, 2, 1]
[1, 1, 0, 0]
[1, 1, 0, 1]
[1, 0, 1, 0]

print(my_matrix4.inverse)
#result:
[-0.5, 0, 0.5, 1]
[0.5, 1, -0.5, -1]
[0.5, 0, -0.5, 0]
[0, -1, 1, 0]

#and more...

```
#### get the matrix by list
```python
my_matrix = Mx.Matrix("1,2,3;4,5,6;7,8,9")

print(my_matrix.raw)
#result:
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

#### get identity Matrix
```python
i = Mx.UnitMatrix(3)

#result:
print(i)
[1, 0, 1]
[0, 0, 1]
[0, 0, 1]
```