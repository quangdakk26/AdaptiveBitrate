from pathlib import Path
import pandas as pd
import torch
import torchaudio
import soundfile as sf

from encodec import EncodecModel
from encodec.utils import convert_audio
from metrics import snr_db, mse, compression_ratio

INPUT = Path("data/input/sample.wav")
OUT_DIR = Path("data/output")
TABLE_DIR = Path("results/tables")

BANDWIDTHS = [1.5, 3, 6, 12, 24]

def main():
    wav, sr = torchaudio.load(str(INPUT))

    model = EncodecModel.encodec_model_24khz()
    model.eval()

    wav = convert_audio(wav, sr, model.sample_rate, model.channels)
    wav = wav.unsqueeze(0)

    ref = wav.squeeze(0).numpy()
    duration = ref.shape[-1] / model.sample_rate
    original_bits = ref.shape[-1] * model.channels * 16

    rows = []

    for bw in BANDWIDTHS:
        model.set_target_bandwidth(bw)

        with torch.no_grad():
            encoded = model.encode(wav)
            decoded = model.decode(encoded)

        rec = decoded.squeeze(0).numpy()

        sf.write(f"data/output/out_{bw}.wav", rec.T, model.sample_rate)

        m = mse(ref.flatten(), rec.flatten())
        s = snr_db(ref.flatten(), rec.flatten())

        compressed_bits = bw * 1000 * duration
        cr = compression_ratio(original_bits, compressed_bits)

        rows.append({
            "bitrate": bw,
            "mse": m,
            "snr": s,
            "compression_ratio": cr
        })

    df = pd.DataFrame(rows)
    df.to_csv("results/tables/result.csv", index=False)

    print(df)

if __name__ == "__main__":
    main()