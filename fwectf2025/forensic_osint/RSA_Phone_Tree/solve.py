import numpy as np
from scipy.io.wavfile import read
from scipy.signal import find_peaks
from itertools import product
from Crypto.Util.number import long_to_bytes, isPrime

# DTMF周波数テーブル
dtmf_freqs = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D',
}

# 周波数の近似マッチング
def match_dtmf(freq1, freq2):
    for (f1, f2), char in dtmf_freqs.items():
        if abs(freq1 - f1) < 20 and abs(freq2 - f2) < 20:
            return char
    return None

# 音声ファイルの解析
def analyze_tone(filename, fs=8000, tone_time=0.08, silence_time=0.10):
    rate, data = read(filename)
    data = data / 32767.0  # 正規化
    samples_per_tone = int(fs * tone_time)
    samples_per_silence = int(fs * silence_time)
    step = samples_per_tone + samples_per_silence

    decoded = []
    for i in range(0, len(data), step):
        tone = data[i:i+samples_per_tone]
        if len(tone) < samples_per_tone:
            break

        # フーリエ変換
        fft = np.fft.rfft(tone)
        freqs = np.fft.rfftfreq(len(tone), 1/fs)
        magnitude = np.abs(fft)

        # ピーク周波数を検出
        peaks, _ = find_peaks(magnitude, height=0.1)
        peak_freqs = freqs[peaks]
        peak_freqs = sorted(peak_freqs[:2])  # 上位2つの周波数を取得

        if len(peak_freqs) == 2:
            char = match_dtmf(peak_freqs[0], peak_freqs[1])
            if char:
                decoded.append(char)
            else:
                decoded.append('?')

    return ''.join(decoded)

# 音声ファイルを解析
p_decoded = analyze_tone("p_dial.wav")
q_decoded = analyze_tone("q_dial.wav")
c_decoded = analyze_tone("message.wav")

# 結果を表示
print("Decoded p:", p_decoded)
print("Decoded q:", q_decoded)
print("Decoded c:", c_decoded)

# ? を0〜9で置き換える候補を生成
def generate_candidates(decoded_str):
    if '?' not in decoded_str:
        return [decoded_str]  # ?がない場合はそのまま返す

    # ? の数だけ0〜9の組み合わせを生成
    num_questions = decoded_str.count('?')
    replacements = product('0123456789', repeat=num_questions)

    # ? を置き換えた候補を生成
    candidates = []
    for replacement in replacements:
        candidate = decoded_str
        for digit in replacement:
            candidate = candidate.replace('?', digit, 1)  # 1つずつ置き換え
        candidates.append(candidate)
    return candidates

# 各候補を生成して試す
def find_valid_values(decoded_str, check_prime=False):
    candidates = generate_candidates(decoded_str)
    valid_values = []
    for candidate in candidates:
        try:
            value = int(candidate)  # 数値に変換
            if check_prime:
                if isPrime(value):  # 素数チェック
                    valid_values.append(value)
            else:
                valid_values.append(value)
        except ValueError:
            continue
    return valid_values

# p, q, c の候補を生成
p_candidates = find_valid_values(p_decoded, check_prime=True)  # pは素数チェック
q_candidates = find_valid_values(q_decoded, check_prime=True)  # qも素数チェック
c_candidates = find_valid_values(c_decoded, check_prime=False)  # cは素数チェック不要

# print("Valid p candidates:", p_candidates)
# print("Valid q candidates:", q_candidates)
# print("Valid c candidates:", c_candidates)

p = p_candidates[0]
q = q_candidates[0]

e = 65537

for c in c_candidates:
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # 秘密鍵 d を計算
    d = pow(e, -1, phi_n)

    # 平文を復号
    m = pow(c, d, n)

    # 平文をバイト列に変換
    plaintext = long_to_bytes(m)

    # 結果を表示
    print(plaintext)
