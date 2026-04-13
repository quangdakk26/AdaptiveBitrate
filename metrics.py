import numpy as np

def snr_db(x, y):
    noise = x - y
    return 10 * np.log10(np.mean(x**2) / (np.mean(noise**2) + 1e-12))

def mse(x, y):
    return np.mean((x - y) ** 2)

def compression_ratio(original_bits, compressed_bits):
    return original_bits / compressed_bits