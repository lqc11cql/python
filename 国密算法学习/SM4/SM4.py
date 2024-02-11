import hashlib
import hmac
import random

import time
from yun import ssh
import database
import json


class sm4():
    # 固定参数
    CK = [0x00070F15, 0x1c232a31, 0x383f464d, 0x545b6269,
          0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
          0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
          0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
          0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
          0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
          0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
          0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279]
    # 常数
    FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]
    # S盒
    S_box = [
        0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
        0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
        0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
        0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
        0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
        0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
        0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
        0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
        0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
        0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
        0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
        0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
        0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
        0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
        0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
        0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48]
    # 拓展密钥
    K = []
    MK = []
    # 密钥
    key = 0
    # 数据流
    txtdata = []
    # 文件缺失长度
    lenth = 0

    def __init__(self):
        pass

    # 第一步
    # 密钥生成
    # 经过拓展，rk0=K4，rk1=K5，以此类推
    def key_expand(self, key):
        self.MK = []
        self.K = []
        Mkey = self.apart_128_hex(key)
        for i in range(0, 4):
            self.MK.append(Mkey[i])
        for i in range(4):
            self.K.append(self.MK[i] ^ self.FK[i])
        for i in range(32):
            a = (self.K[i + 1] ^ self.K[i + 2] ^ self.K[i + 3] ^ self.getCK(i)) & 0xffffffff
            b = self.apart_hex(a)
            c = [self.getSbox(i) for i in b]
            d = self.union_hex(c)
            e = (d ^ (d << 13) ^ (d << 23)) & 0xffffffff
            self.K.append(self.K[i] ^ e)

    # 将在4个8位数据合并一个32位数据
    def union_hex(self, data):
        return int((data[0] << 24) | (data[1] << 16) | (data[2] << 8) | (data[3]))

    # 将一个128位数据拆开位4个32位数据
    def apart_128_hex(self, data):
        return [int((data >> 96) & 0xffffffff), int((data >> 64) & 0xffffffff), int((data >> 32) & 0xffffffff),
                int((data) & 0xffffffff)]

    def apart_hex(self, data):
        return [int((data >> 24) & 0xff), int((data >> 16) & 0xff), int((data >> 8) & 0xff), int((data) & 0xff)]

    # 获取S盒的元素
    def getSbox(self, i):
        return self.S_box[i]

    # 获取固定参数
    def getCK(self, i):
        return self.CK[i]

    # 获取文件路径
    def get_address(self, name):
        len_address = name.rfind('/')
        return name[:len_address + 1]

    # 获取文件名
    def get_filename(self, name):
        len_address = name.rfind('/')
        len_name = name.rfind('.')
        a = name[len_address + 1:len_name]
        if a.find('.') != -1:
            a = self.get_filename(a)
        return a.encode()

    # 加密解密
    def deal(self, txtdata, key, ctr):
        self.key_expand(key)
        X = []
        Y = []
        J = []
        for p in range(0, len(txtdata), 16):
            # 密文分组
            plaintxt = txtdata[p:p + 16]
            X = self.apart_128_hex(ctr)
            j = 4
            # 求明文/密文
            a = 0
            for i in range(0, 32):
                a = X[i + 1] ^ X[i + 2] ^ X[i + 3] ^ self.K[j]
                j = j + 1
                b = self.apart_hex(a)
                c = [self.getSbox(i) for i in b]
                d = self.union_hex(c)
                e = d ^ (d << 2) ^ (d << 10) ^ (d << 18) ^ (d << 24)
                X.append(X[i] ^ e)
            # 明文/密文逆序
            t = X[35]
            X[35] = X[32]
            X[32] = t
            t = X[34]
            X[34] = X[33]
            X[33] = t
            # 明文/密文储存
            for i in range(32, 36):
                X[i] = X[i] & 0xffffffff
                Y.append(X[i])
            J.extend([Y[p // 4] ^ self.union_hex(plaintxt[0: 4]), Y[p // 4 + 1] ^ self.union_hex(plaintxt[4: 8]),
                      Y[p // 4 + 2] ^ self.union_hex(plaintxt[8: 12]),
                      Y[p // 4 + 3] ^ self.union_hex(plaintxt[12: 16])])
            ctr = ctr + 1
        return J

    # 加密文件名
    def en_filename(self, seed1, address):
        filename = self.get_filename(address)
        C_name = []
        for x in filename:
            C_name.append(x)
        lenth = 48 - len(C_name)
        # 补齐48bit
        for i in range(lenth):
            C_name.append(0)
        nkey = hashlib.sha256(str(C_name).encode()).hexdigest()
        C_name = self.deal(C_name, int(nkey, 16) >> 128, 0)
        R = int(
            (C_name[4] << 224) | (C_name[5] << 192) | (C_name[6] << 160) | (C_name[7] << 128) | (C_name[8] << 96) | (
                    C_name[9] << 64) | (C_name[10] << 32) | (C_name[11]))
        L = ((C_name[0] << 96) | (C_name[1] << 64) | (C_name[2] << 32) | (C_name[3]))
        hashkey = hashlib.sha256(str(L).encode()).hexdigest()
        random.seed(seed1)
        s = random.randbytes(16)
        FK = hmac.new(int(hashkey, 16).to_bytes(length=32, byteorder='big'), s, digestmod='sha256').hexdigest()
        S = int.from_bytes(s, byteorder='big')
        Cname = ((L << 256) | R) ^ ((S << 256) | int(FK, 16))
        return [hex(Cname)[2:], hashkey, hex(int(nkey, 16) >> 128)[2:]]

    # 搜索
    def search(self, a, k):
        filename = a.encode()
        C_name = []
        for x in filename:
            C_name.append(x)
        lenth = 48 - len(C_name)
        # 补齐48bit
        for i in range(lenth):
            C_name.append(0)
        nkey = hashlib.sha256(str(C_name).encode()).hexdigest()
        C_name = self.deal(C_name, int(nkey, 16) >> 128, 0)
        X = ((C_name[0] << 352) | (C_name[1] << 320) | (C_name[2] << 288) | (C_name[3] << 256) | (C_name[4] << 224) | (
                C_name[5] << 192) | (C_name[6] << 160) | (C_name[7] << 128) | (C_name[8] << 96) | (
                     C_name[9] << 64) | (C_name[10] << 32) | (C_name[11]))
        with open('hostdata.txt', 'r') as f:
            a = json.loads(f.read())
        hostdata = {
            'ip': a.get('ip'),
            'port': 22,
            'user': a.get('user'),
            'passwd': a.get('passwd'),
        }
        f = ssh(hostdata)
        l = []
        for i in f.ser()[:-1]:
            x = 0
            if i.find('.') != -1:
                i = i[:i.find('.')]
                x = x + 1
            C = int(i, 16)
            T = X ^ C
            TL = T >> 256

            TR = hmac.new(k.to_bytes(length=32, byteorder='big'), TL.to_bytes(length=16, byteorder='big'), digestmod='sha256').hexdigest()
            if TR == hex(T & 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)[2:]:
                if x == 0:
                    l.append(i + '.txt')
                else:
                    for j in range(x):
                        i = i + '.txt'
                    l.append(i + '.txt')
        return l

    # 解密文件名
    def de_filename(self, seed1, name, nkey):
        filename = self.get_filename(name)
        Cname = int(filename, 16)
        random.seed(seed1)
        s = random.randbytes(16)
        CL = Cname >> 256
        CR = Cname & 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        L = CL ^ int.from_bytes(s, byteorder='big')
        hashkey = hashlib.sha256(str(L).encode()).hexdigest()
        FK = hmac.new(int(hashkey, 16).to_bytes(length=32, byteorder='big'), s, digestmod='sha256').hexdigest()
        R = int(FK, 16) ^ CR
        X = L << 256 | R
        X_name = [X >> 352, X >> 320 & 0xffffffff, X >> 288 & 0xffffffff, X >> 256 & 0xffffffff, X >> 224 & 0xffffffff,
                  X >> 192 & 0xffffffff, X >> 160 & 0xffffffff, X >> 168 & 0xffffffff, X >> 96 & 0xffffffff,
                  X >> 64 & 0xffffffff, X >> 32 & 0xffffffff, X & 0xffffffff]
        M = []
        for i in X_name:
            M.extend(self.apart_hex(i))
        M_name = self.deal(M, nkey, 0)
        byte = []
        for i in M_name:
            a = self.apart_hex(i)
            for j in a:
                byte.append(j)
        byte1 = []
        byte1.extend(byte[:byte.index(0)])
        str1 = str(bytes(byte1), 'utf-8')
        return str1

    # 加密文件
    def encrypt(self, seed1, key, address):
        modle = 'encrypt'
        txt = self.file_open(modle, address)
        H = 0
        for i in txt:
            H = H << 8 | i
        data_sha = hashlib.sha256(hex(H).encode('utf-8')).hexdigest()
        database.insert(data_sha)
        C = self.deal(self.txtdata, key, 0)
        i = self.en_filename(seed1, address)
        name = self.get_address(address) + i[0] + '.txt'
        self.file_save(modle, name, C)
        return [name, i[1], hex(key << 128 | int(i[2], 16))[2:]]

    # 解密文件
    def decrypt(self, seed1, key, address):
        modle = 'decrypt'
        self.file_open(modle, address)
        key1 = key >> 128
        nkey = key & 0xffffffffffffffffffffffffffffffff
        M = self.deal(self.txtdata, key1, 0)
        ver = 0
        name = self.get_address(address) + 'M_' + self.de_filename(seed1, address, nkey) + '.txt'
        txt = self.file_save(modle, name, M)
        for i in txt:
            ver = ver << 8 | i
        data_sha = hashlib.sha256(hex(ver).encode('utf-8')).hexdigest()
        s = time.time()

        if database.search(data_sha):
            e = time.time()
            return e - s
        else:
            return False

    # 打开文件
    def file_open(self, modle, name):
        self.txtdata = []
        with open(name, 'rb') as f:
            a = f.read()
        for i in a:
            self.txtdata.append(i)
        txt = []
        txt.extend(self.txtdata)
        if modle == 'encrypt':
            self.lenth = 16 - len(self.txtdata) % 16
            # 补齐32bit
            for i in range(self.lenth + 15):
                self.txtdata.append(0)
            self.txtdata.append(self.lenth)
        return txt

    # 保存文件
    def file_save(self, modle, name, Y):
        byte = []
        for i in Y:
            a = self.apart_hex(i)
            for j in a:
                byte.append(j)
        if modle == 'decrypt':
            self.lenth = byte[-1]
            byte = byte[:len(byte) - self.lenth - 16]
        with open(name, 'wb') as f:
            f.write(bytes(byte))
        return byte







