a1 = """
1
65
16
0
10
0
49
1
1
45
26
10
176
11
39
33
0
11
2
0
286
0
65
8
0
0
27
7
88
0
25
24
1
12
8
"""
a = []
for i in a1.split():
    a.append(i)
sum = 0
for i in set(a):
    sum +=int(i)
print(sum)

# print((0.059/27.4)*100)
#
# def test(a):
#     tmp = 17
#     ret = []
#     for i in a:
#         tmp -=1
#         if i == '1':
#             ret.append(tmp)
#     return ret
#
# if __name__ == '__main__':
#     a = test('1000000000010001')
#     print(a)