a = [1651145643879, 1651134414777, 1651134273695, 1651127223290, 1651127252476, 1651127125532, 1651145935395, 1651127334402]
a.sort()
print(a)
# 2022-4-28 18:51:51
def evaluate(arg):
    arg.sort()
    ret = [1 for i in range(len(arg))]

    for i in range(0,len(arg)):
        num = 1
        for j in range(i+1,len(arg)):
            if arg[j]-arg[i]<=3600000:
                num +=1
                ret[i] = num
            else:
                break
    return max(ret)


if __name__ == '__main__':
    c = evaluate(a)
    print(c)
    len(a)

    # 2022 - 4 - 28
    # 14: 25:25