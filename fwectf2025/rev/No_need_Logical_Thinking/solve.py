with open('./output.txt', 'rb') as f:
    data = bytes([c for c in f.read() if c != 0xC2])
    original_data = b''
    for i in range(len(data)):
        original_data += bytes([data[i] - (i+1)])
    print(original_data)
