from pathlib import Path
import torch
import torchaudio
import soundfile as sf
from encodec import EncodecModel
from encodec.utils import convert_audio

INPUT = Path("data/input/sample.wav")
OUTPUT = Path("data/output/reconstructed_6kbps.wav")

def main():
    wav, sr = torchaudio.load(str(INPUT))

    model = EncodecModel.encodec_model_24khz()
    model.set_target_bandwidth(6.0)
    model.eval()

    wav = convert_audio(wav, sr, model.sample_rate, model.channels)
    wav = wav.unsqueeze(0)

    with torch.no_grad():
        encoded = model.encode(wav)
        decoded = model.decode(encoded)

    decoded = decoded.squeeze(0).cpu()
    sf.write(str(OUTPUT), decoded.T.numpy(), model.sample_rate)

    print("Done!")

if __name__ == "__main__":
    main()