# ECC-ECDHE-Chat-Example
Example of the ephemeral form of ECDH exchange with forward secrecy
# Features
 - [x] Re-usable core crypto module
 - [x] ECDH Exchange (+ Key derviation) with manual key rotation for ephemeral encryption
 - [x] AES Encryption/Decryption
 - [x] CLI UI
# Future
 - [ ] (In progress) Session management
 - [ ] (TODO) Semi-auto exchange using tunnels (peer-to-peer)
 - [ ] (TODO) GUI
# Prerequisites
1. `pip install cryptography`
2. `python main.py`
# Usage
1. Share your pubkey to your peer (end party)
2. Enter your peer pubkey to terminal input
3. Use `encrypt` to encrypt your text message, `decrypt` to decrypt, `rotate` to rotate keys
