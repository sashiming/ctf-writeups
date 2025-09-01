with open('./output.txt', 'rb') as f:
    data = f.read()
    original_data = b''
    countc2 = 0
    for i in range(len(data)):
        if data[i] == 0xC2:
            countc2 += 1
        else:
            original_data += bytes([data[i] - (i+1 - countc2)])
    print(original_data)
