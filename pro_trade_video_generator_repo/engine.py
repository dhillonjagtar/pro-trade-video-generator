import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoClip, AudioFileClip, CompositeVideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import uuid
import os

# Mock GPT response
MOCK_SCRIPT = """A put credit spread is a bullish options strategy.
You sell a put at a higher strike and buy another at a lower strike to define your risk.
Selling the 430 put and buying the 420 put creates a $10-wide spread.
If the underlying stays above 430, you keep the premium.
Your max loss is limited to the width minus the credit received.
This trade benefits from time decay and neutral-to-bullish bias."""

# Mock voiceover (replace with ElevenLabs API in production)
def generate_mock_voice(script_text):
    return "static/sample_audio.mp3"

def generate_animation(prices, payoffs, duration):
    fig, ax = plt.subplots()

    def make_frame(t):
        i = int(t * 30)
        ax.clear()
        ax.set_xlim(prices.min(), prices.max())
        ax.set_ylim(-12, 4)
        ax.set_xlabel("SPY Price at Expiration")
        ax.set_ylabel("Profit / Loss")
        ax.set_title("Put Credit Spread Payoff")
        ax.plot(prices[:i], payoffs[:i], color="blue", lw=2)
        return mplfig_to_npimage(fig)

    video = VideoClip(make_frame, duration=duration)
    video_path = f"static/outputs/video_{uuid.uuid4().hex}.mp4"
    video.write_videofile(video_path, fps=30, audio=False)
    return video_path

def generate_trade_video(user_prompt):
    script = MOCK_SCRIPT
    audio_path = generate_mock_voice(script)

    prices = np.linspace(400, 460, 300)
    short_strike, long_strike, credit = 430, 420, 2.00
    def payoff(price):
        return np.maximum(short_strike - price, 0) - np.maximum(long_strike - price, 0) + credit
    payoffs = np.array([payoff(p) for p in prices])

    video_path = generate_animation(prices, payoffs, duration=10)

    final_video_path = video_path.replace("video_", "final_")
    final = VideoClip(lambda t: mplfig_to_npimage(plt.gcf()), duration=10).set_audio(AudioFileClip(audio_path))
    final.write_videofile(final_video_path, fps=30)
    return final_video_path
