import hashlib
import random
from math import gcd, ceil, log


# 整数到字节串的转换。
def int_to_bytes(x, k):
    if pow(256, k) <= x:
        raise Exception("无法实现整数到字节串的转换，目标字节串长度过短！")
    s = hex(x)[2:].rjust(k * 2, '0')
    M = b''
    for i in range(k):
        M = M + bytes([eval('0x' + s[i * 2:i * 2 + 2])])
    return M


# 字节串到整数的转换。
def bytes_to_int(M):
    k = len(M)
    x = 0
    for i in range(k - 1, -1, -1):
        x += pow(256, k - 1 - i) * M[i]
    return x


# 比特串到字节串的转换。
def bits_to_bytes(s):
    k = ceil(len(s) / 8)
    s = s.rjust(k * 8, '0')
    M = b''  # M存储要返回的字节串
    for i in range(k):
        M = M + bytes([eval('0b' + s[i * 8: i * 8 + 8])])
    return M


# 字节串到比特串的转换。
def bytes_to_bits(M):
    s_list = []
    for i in M:
        s_list.append(bin(i)[2:].rjust(8, '0'))  # 每次循环存储1个字节。左填充补0
    s = ''.join(s_list)
    return s


# 域元素到字节串的转换。域元素是整数，转换成字节串要明确长度。文档规定域元素转换为字节串的长度是ceil(ceil(log(q, 2)/8))。接收的参数是域元素a，返回字节串M
def fielde_to_bytes(e):
    q = eval('0x' + '8542D69E 4C044F18 E8B92435 BF6FF7DE 45728391 5C45517D 722EDB8B 08F1DFC3'.replace(' ', ''))
    t = ceil(log(q, 2))
    l = ceil(t / 8)
    return int_to_bytes(e, l)


# 点到字节串的转换。接收的参数是椭圆曲线上的点p，元组表示。输出字节串S。选用未压缩表示形式
def point_to_bytes(P):
    xp, yp = P[0], P[1]
    x = fielde_to_bytes(xp)
    y = fielde_to_bytes(yp)
    PC = bytes([0x04])
    s = PC + x + y
    return s


# 字节串到点的转换。接收的参数是字节串s，返回椭圆曲线上的点P，点P的坐标用元组表示
def bytes_to_point(s):
    if len(s) % 2 == 0:
        raise Exception("无法实现字节串到点的转换，请检查字节串是否为未压缩形式！")
    l = (len(s) - 1) // 2
    PC = s[0]
    x = s[1: l + 1]
    y = s[l + 1: 2 * l + 1]
    xp = bytes_to_int(x)
    yp = bytes_to_int(y)
    P = (xp, yp)  # 此处缺少检验点p是否在椭圆曲线上
    return P


# 附加数据类型转换
# 域元素到比特串
def fielde_to_bits(a):
    a_bytes = fielde_to_bytes(a)
    a_bits = bytes_to_bits(a_bytes)
    return a_bits


# 点到比特串
def point_to_bits(P):
    p_bytes = point_to_bytes(P)
    p_bits = bytes_to_bits(p_bytes)
    return p_bits


# 整数到比特串
def int_to_bits(x):
    x_bits = bin(x)[2:]
    k = ceil(len(x_bits) / 8)  # 8位1组，k是组数。目的是方便对齐
    x_bits = x_bits.rjust(k * 8, '0')
    return x_bits


# 字节串到十六进制串
def bytes_to_hex(m):
    h_list = []  # h_list存储十六进制串中的每一部分
    for i in m:
        e = hex(i)[2:].rjust(2, '0')  # 不能把0丢掉
        h_list.append(e)
    h = ''.join(h_list)
    return h


# 比特串到十六进制
def bits_to_hex(s):
    s_bytes = bits_to_bytes(s)
    s_hex = bytes_to_hex(s_bytes)
    return s_hex


# 十六进制串到比特串
def hex_to_bits(h):
    b_list = []
    for i in h:
        b = bin(eval('0x' + i))[2:].rjust(4, '0')  # 增强型for循环，是i不是h
        b_list.append(b)
    b = ''.join(b_list)
    return b


# 十六进制到字节串
def hex_to_bytes(h):
    h_bits = hex_to_bits(h)
    h_bytes = bits_to_bytes(h_bits)
    return h_bytes


# 域元素到十六进制串
def fielde_to_hex(e):
    h = hex(e)[2:]
    return h


# 密钥派生函数KDF。
def KDF(Z, klen):
    v = 256  # 密码杂凑函数采用hash-sha256
    if klen >= (pow(2, 32) - 1) * v:
        raise Exception('请检查klen的大小')
    ct = 0x00000001
    if klen % v == 0:
        l = klen // v
    else:
        l = klen // v + 1
    Ha = []
    for i in range(l):  # i从0到 klen/v-1（向上取整）,共l个元素
        s = Z + int_to_bits(ct).rjust(32, '0')  # s存储 Z || ct 的比特串形式 # 注意，ct要填充为32位
        s_bytes = bits_to_bytes(s)  # s_bytes存储字节串形式
        hash_hex = hashlib.sha256(s_bytes).hexdigest()
        hash_bin = hex_to_bits(hash_hex)
        Ha.append(hash_bin)
        ct += 1
    if klen % v != 0:
        Ha[-1] = Ha[-1][:klen - v * (klen // v)]
    k = ''.join(Ha)
    return k


# 模逆算法。返回M模m的逆。在将分式模运算转换为整数时用，分子分母同时乘上分母的模逆。
def ni(M, m):
    if m == 0:
        return 1, 0
    x, y = ni(m, M % m)
    return y, x - (M // m) * y


# 将分式模运算转换为整数。输入 up/down mod m, 返回该分式在模m意义下的整数。点加和二倍点运算时求λ用。
def frac_to_int(up, down, p):
    num = gcd(up, down)
    up //= num
    down //= num         # 分子分母约分
    return up * ni(down, p)[0] % p


# 椭圆曲线上的点加运算。接收的参数是元组P和Q，表示相加的两个点，p为模数。返回二者的点加和
def add_point(P, Q, p):
    if P == 0:
        return Q
    if Q == 0:
        return P
    x1, y1, x2, y2 = P[0], P[1], Q[0], Q[1]
    e = frac_to_int(y2 - y1, x2 - x1, p)  # e为λ
    x3 = (e * e - x1 - x2) % p  # 注意此处也要取模
    y3 = (e * (x1 - x3) - y1) % p
    ans = (x3, y3)
    return ans


# 二倍点算法。不能直接用点加算法，否则会发生除零错误。接收的参数是点P，素数p，椭圆曲线参数a。返回P的二倍点。
def double_point(P, p, a):
    if P == 0:
        return P
    x1, y1 = P[0], P[1]
    e = frac_to_int(3 * x1 * x1 + a, 2 * y1, p)  # e是λ
    x3 = (e * e - 2 * x1) % p  # 取模！！！！！
    y3 = (e * (x1 - x3) - y1) % p
    Q = (x3, y3)
    return Q


# 多倍点算法。通过二进制展开法实现。接收的参数[k]p是要求的多倍点，m是模数，a是椭圆曲线参数。
def mult_point(P, k, p, a):
    s = bin(k)[2:]  # s是k的二进制串形式
    Q = 0
    for i in s:
        Q = double_point(Q, p, a)
        if i == '1':
            Q = add_point(P, Q, p)
    return Q


# 验证某个点是否在椭圆曲线上。接收的参数是椭圆曲线系统参数fq和要验证的点P(x, y)。
def on_curve(fq, P):
    p, a, b, h, G, n = fq
    x, y = P
    if pow(y, 2, p) == ((pow(x, 3, p) + a * x + b) % p):
        return True
    return False


# 加密算法。接收的参数是椭圆曲线系统参数fq(p, a, b, h, G, n)。其中n是基点G的阶。PB是B的公钥，M是明文消息。
def encry_sm2(fq, PB, M):
    p, a, b, h, G, n = fq  # 序列解包
    M_bytes = bytes(M, encoding='ascii')
    k = random.randint(1, n - 1)
    C1 = mult_point(G, k, p, a)
    C1_bits = point_to_bits(C1)
    S = mult_point(PB, h, p, a)
    if add_point(S, G, p) == G:
        print('S是无穷远点')
    x2, y2 = mult_point(PB, k, p, a)
    x2_bits = fielde_to_bits(x2)
    y2_bits = fielde_to_bits(y2)
    M_hex = bytes_to_hex(M_bytes)
    klen = 4 * len(M_hex)
    t = KDF(x2_bits + y2_bits, klen)
    if eval('0b' + t) == 0:
        raise Exception('KDF返回了全零串，请检查KDF算法！')
    C2 = eval('0x' + M_hex + '^' + '0b' + t)
    x2_bytes = bits_to_bytes(x2_bits)
    y2_bytes = bits_to_bytes(y2_bits)
    C3 = hashlib.sha256(x2_bytes + M_bytes + y2_bytes).hexdigest()
    C1_hex = bits_to_hex(C1_bits)
    C2_hex = hex(C2)[2:]
    C3_hex = C3
    C_hex = C1_hex + C2_hex + C3_hex
    print('----------------------\n加密得到的密文是：', C_hex)
    return C_hex


# 解密算法。接收的参数为椭圆曲线系统参数fq(p, a, b, h, G, n)。dB是B的私钥，C是密文消息。
def decry_sm2(fq, dB, C):
    p, a, b, h, G, n = fq
    l = ceil(log(p, 2) / 8)  # l是一个域元素（比如一个点的横坐标）转换为字节串后的字节长度.则未压缩的密文第一部分C1长度为2l+1
    bytes_l1 = 2 * l + 1
    hex_l1 = bytes_l1 * 2  # hex_l1是密文第一部分C1的十六进制串的长度
    C_bytes = hex_to_bytes(C)
    C1_bytes = C_bytes[0:2 * l + 1]
    C1 = bytes_to_point(C1_bytes)
    if not on_curve(fq, C1):  # 检验C1是否在椭圆曲线上
        raise Exception('在解密算法B1中，取得的C1不在椭圆曲线上！')
    S = mult_point(C1, h, p, a)
    if add_point(S, G, p) == G:
        print('S是无穷远点')
    temp = mult_point(C1, dB, p, a)
    x2, y2 = temp[0], temp[1]
    x2_hex, y2_hex = fielde_to_hex(x2), fielde_to_hex(y2)
    hex_l3 = 64  # hex_l3是密文第三部分C3的十六进制串的长度。C3是通过hash-sha256得到的hash值，是64位十六进制串。
    hex_l2 = len(C) - hex_l1 - hex_l3  # hex_l2是密文第二部分C2的十六进制串的长度。
    klen = hex_l2 * 4  # klen是密文C2中比特串的长度
    x2_bits, y2_bits = hex_to_bits(x2_hex), hex_to_bits(y2_hex)
    t = KDF(x2_bits + y2_bits, klen)
    if eval('0b' + t) == 0:
        raise Exception('在解密算法B4中，得到的t是全0串！')
    t_hex = bits_to_hex(t)
    C2_hex = C[hex_l1: -hex_l3]
    M1 = eval('0x' + C2_hex + '^' + '0x' + t_hex)  # M1是M'，M′ = C2 ⊕ t
    M1_hex = hex(M1)[2:].rjust(hex_l2, '0')  # 注意位数要一致
    M1_bits = hex_to_bits(M1_hex)
    cmp_bits = x2_bits + M1_bits + y2_bits  # cmp_bits存储用于计算哈希值以对比C3的二进制串
    cmp_bytes = bits_to_bytes(cmp_bits)
    u = hashlib.sha256(cmp_bytes).hexdigest()
    C3_hex = C[-hex_l3:]
    if u != C3_hex:
        raise Exception('在解密算法B6中，计算的u与C3不同！')
    M_bytes = hex_to_bytes(M1_hex)
    M = str(M_bytes, encoding='ascii')
    print('----------------------\n解密出的明文是：', M)
    return M


def key_pair(fq):
    p, a, b, h, G, n = fq
    d = random.randint(1, n - 2)
    P = mult_point(G, d, p, a)

    if add_point(P, G, p) == G:
        print('P是无穷远点')
    if on_curve(fq, P) == False:
        raise Exception('P没在曲线上')
    if add_point(mult_point(P, n, p, a), G, p) == G:

        print('n倍的P是无穷远点')
    return P, d


print('椭圆曲线方程为：y^2 = x^3 + ax + b')
p, a, b, h, G, n = 60275702009245096385686171515219896416297121499402250955537857683885541941187, 54492052985589574080443685629857027481671841726313362585597978545915325572248, 45183185393608134601425506985501881231876135519103376096391853873370470098074, 1, (
    29905514254078361236418469080477708234343499662916671209092838329800180225085,
    2940593737975541915790390447892157254280677083040126061230851964063234001314), 60275702009245096385686171515219896415919644698453424055561665251330296281527
fq = (p, a, b, h, G, n)
p, a, b, h, xG, yG, n = tuple(map(lambda x: hex(x)[2:], (p, a, b, h, G[0], G[1], n)))  # 将参数转换为十六进制串便于输出
print('----------------------\n椭圆曲线系统所在素域的p是：', p)
print('----------------------\n椭圆曲线系统的参数a是：', a)
print('----------------------\n椭圆曲线系统的参数b是：', b)
print('----------------------\n椭圆曲线系统的余因子h是：', h)
print('----------------------\n椭圆曲线系统的基点G的横坐标xG是：', xG)
print('----------------------\n椭圆曲线系统的基点G的纵坐标yG是：', yG)
'''PB, dB = (0x435B39CCA8F3B508C1488AFC67BE491A0F7BA07E581A0E4849A5CF70628A7E0A,
          0x75DDBA78F15FEECB4C7895E2C1CDF5FE01DEBB2CDBADF45399CCF77BBA076A42), 0x1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0
'''
PB, dB = key_pair(fq)
with open('10.txt', 'r') as f:
    M = f.read()
print('----------------------\n明文是：', M)
C = encry_sm2(fq, PB, M)  # 加密算法
de_M = decry_sm2(fq, dB, C)  # 解密算法
print('----------------------\n验证:', end='')
if M == de_M:
    print('解密成功')
else:
    print('解密失败')


