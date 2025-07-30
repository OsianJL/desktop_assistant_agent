import os
from tools.audio.open_audio_with_vlc import open_audio_with_vlc
from utils.path_utils import AGENT_ROOT_DIR

def play_audio_by_name(input_str: str) -> str:
    """
    Recursively searches and plays an audio file by name inside AGENT_ROOT_DIR.

    Args:
        input_str (str): Name of the audio file (e.g., 'test.mp3')

    Returns:
        str: Result of playback attempt
    """
    target_name = input_str.strip().strip("'\"")  # remove quotes

    for root, _, files in os.walk(AGENT_ROOT_DIR):
        for file in files:
            if file.lower() == target_name.lower():
                relative_path = os.path.relpath(os.path.join(root, file), AGENT_ROOT_DIR)
                return open_audio_with_vlc(relative_path)

    return f"❌ File '{target_name}' not found anywhere inside AI_File_Testing."
