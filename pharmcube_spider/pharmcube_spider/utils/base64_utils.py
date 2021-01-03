import base64

# 加密
def encode_base64(info):
    return base64.b64encode(info)

# 解密
def decode_base64(info):
    return base64.decodebytes(info)

if __name__ == '__main__':
    results = encode_base64('1234'.encode('utf-8'))
    print(results)
    decode_results = decode_base64(results)
    print(str(decode_results, encoding='utf-8'))