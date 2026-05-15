import machine
import uos
from machine import I2S, Pin

# --- I2S Configuration ---
I2S_ID     = 0
SCK_PIN    = 26   # BCLK
WS_PIN     = 27   # LRC / WSEL
SD_PIN     = 28   # DIN

SAMPLE_RATE    = 22050
SAMPLE_BITS    = 16
CHANNELS       = 1  # Mono
BUFFER_LENGTH  = 2048  # bytes, adjust for RAM

# --- Init I2S ---
audio_out = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.TX,
    bits=SAMPLE_BITS,
    format=I2S.MONO,
    rate=SAMPLE_RATE,
    ibuf=BUFFER_LENGTH,
)

def play_wav(filename):
    wav = open(filename, "rb")

    # Skip 44-byte WAV header
    wav.seek(44)

    buf = bytearray(BUFFER_LENGTH)
    print(f"Playing: {filename}")

    while True:
        num_read = wav.readinto(buf)
        if num_read == 0:
            break  # End of file
        if num_read < len(buf):
            # Zero-pad the last chunk
            for i in range(num_read, len(buf)):
                buf[i] = 0
        audio_out.write(buf)

    wav.close()
    print("Done.")

# --- Play the file ---
play_wav("output.wav")

# --- Deinit when finished ---
audio_out.deinit()