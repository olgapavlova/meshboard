bridge:
	python3 bridge.py

socket:
	socat - UNIX-CONNECT:/tmp/meshtastic.sock
