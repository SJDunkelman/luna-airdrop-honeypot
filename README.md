# Terra airdrop honeypot

Aim: Transfer any luna that the compromised wallet receives to a secure second address.

### Set up
1. Copy the .env.template file and rename it .env
2. For the SEED_PHRASE variable add your compromised wallet seed within the quotation marks
3. For the SECURE_WALLET_ADDRESS variable add the public wallet address of the second secure wallet
4. Create a virtualenv & install requirements
5. Run main.py