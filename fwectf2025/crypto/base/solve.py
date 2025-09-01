with open('emoji.txt', 'r', encoding='utf-8') as f:
    emoji = list(f.read().strip())

# table = {i: ch for i, ch in enumerate(emoji)}
rev_table = {ch: i for i, ch in enumerate(emoji)}

def decode(data):
    data = data.rstrip('🚀')
    bits = ''.join(f'{rev_table[ch]:010b}' for ch in data)
    bits = bits[:len(bits) - (len(bits) % 8)]
    return bytes([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])

if __name__ == '__main__':
    enc = '🪛🔱🛜🫗🚞👞🍁🎩🚎🐒🌬🧨🖱🥚🫁🧶🪛🔱👀🔧🚞👛😄🎩🚊🌡🌬🧮🤮🥚🫐🛞🪛🔱👽🔧🚞🐻🔳🎩😥🪨🌬🩰🖖🥚🫐🪐🪛🔱👿🫗🚞🏵📚🎩🚊🎄🌬🧯🕺🥚🫁📑🪛🔰🐀🫗🚞💿🔳🎩🚲🚟🌬🧲🚯🥚🫁🚰🪛🔱💀🔧🚞🏓🛼🎩🚿🪻🌬🧪🙊🥚🫐🧢🪛🔱🛟🔧🚞🚋🫳🎩😆🏉🌬🧶🚓🥚🫅💛🪛🔱🔌🐃🚞🐋🥍🎩😱🤮🌬🩰🛳🥚🫀📍🪛🔰🐽🫗🚞💿🍁🎩🚊🌋🌬🧵🔷🚀🚀🚀'
    print(decode(decode(enc).decode()).decode())
