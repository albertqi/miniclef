import os
import subprocess
import threading
import time
from pythonosc import udp_client


# Open prebuilt 'scsynth' server.
scsynth = subprocess.Popen(
    [f"{os.getcwd()}/miniclef/prebuilt/Resources/scsynth", "-u", "57110"],
    stdout=subprocess.PIPE,
)
threading.Thread(target=scsynth.wait, daemon=True).start()
time.sleep(1)  # Wait for the server to start.

# Create a client to send OSC messages to SuperCollider.
client = udp_client.SimpleUDPClient("127.0.0.1", 57110)

# Load all of the synthdefs.
client.send_message("/d_loadDir", [f"{os.getcwd()}/miniclef/scd/compiled"])
time.sleep(1)  # Wait for the synthdefs to load.
