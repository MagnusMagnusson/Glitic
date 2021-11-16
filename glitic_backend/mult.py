a = 6
b = 13

def mult(a,b):
    c = 0
    i = 0
    while(a > 0):    
        i+=1
        if a % 2 == 1:
            c += b
        a = a // 2
        b = b * 2
    return c

def div(a,b):
    if(b == 1):
        return a
    g = b
    max = a
    min = 0
    gold = 0
    i = 0
    while g != gold:
        i += 1
        c = mult(g,b)
        print(i, hex(g), hex(max), hex(min), hex(c))
        gold = g
        if c == a:
            print("Answer")
            break
        elif c >= a:
            max = g
        else:
            min = g
        g = (max + min) >> 1
        
    return g

def sub(a,b):
    if(a==b):
        return 0
    if a < b:
        raise "What the fuck"

    n = a



ass = 9
bss = 119

def fastPow(b,e,m):
    if m == 1:
        return 0

    r = 1
    b = b % m
    while(e > 0):
        if e % 2 == 1:
            r = (r * b) % m
        b = (b*b) % m 
        e = e >> 1
    return r

a = 3 
b = 0xABABABABABABABABABABABABABABABAB
m = 0xAAAAAAAAAAAAAAAA
print(hex(fastPow(a,b,m)))