from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions
from terra_sdk.core.bank import MsgSend
from terra_sdk.core.tx import SignMode
from terra_sdk.key.key import SignOptions
from terra_sdk.core.bech32 import AccAddress
from terra_sdk.core import Coins
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Initialize wallet with associated mnemonic key.
mk = MnemonicKey(mnemonic=os.environ.get("SEED_PHRASE"))
RECIPIENT_ADDRESS = AccAddress(os.environ.get("SECURE_WALLET_ADDRESS"))

CHAIN_ID = "pisco-1"


def main():
    # Terra blockchain client
    terra = LCDClient(
        url="https://pisco-lcd.terra.dev/",
        chain_id=CHAIN_ID
    )
    wallet = terra.wallet(mk)

    print('Connected to network')
    while True:
        try:
            coins = terra.bank.balance(mk.acc_address)
            luna_balance = coins[0]['uluna']
            print('Luna balance:', luna_balance)

            try:
                if luna_balance.amount > 0 and luna_balance.amount > 1000000:  # Must be greater than 1 LUNA balance
                    print('\n\n\nSENDING LUNA OUT OF WALLET\n\n\n')

                    # Send 99% to leave some for gas
                    luna_to_send = luna_balance.mul(0.99).to_int_coin()

                    msg = MsgSend(
                        mk.acc_address,
                        AccAddress(RECIPIENT_ADDRESS),
                        Coins(uluna=luna_to_send.amount),
                    )
                    tx_opt = CreateTxOptions(
                        msgs=[msg], memo="send test", gas_adjustment=1.5
                    )

                    signer_opt = SignerOptions(
                        address=mk.acc_address,
                    )

                    acc_info = terra.auth.account_info(mk.acc_address)

                    sign_opt = SignOptions(
                        account_number=acc_info.account_number,
                        sequence=acc_info.sequence,
                        sign_mode=SignMode.SIGN_MODE_DIRECT,
                        chain_id=CHAIN_ID
                    )

                    tx = terra.tx.create([signer_opt], tx_opt)

                    signed_tx = mk.sign_tx(tx, sign_opt)

                    # broadcast tx
                    result = terra.tx.broadcast(signed_tx)
                    print(result)
            except:
                print('Failed to send tx')

        except:
            print('Failed to get balance')

        # Run twice a second
        time.sleep(0.5)


if __name__ == "__main__":
    main()