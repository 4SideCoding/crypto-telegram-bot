
import aiohttp

# Official USDT TRC20 contract on TRON mainnet
USDT_CONTRACT = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"

TRON_API = "https://api.trongrid.io"


async def check_payment(wallet_address, expected_amount, order_created_ms):
    """
    Check recent USDT transfers to our wallet.
    Returns a transaction ID if a matching transfer is found.
    """

    url = (
        f"{TRON_API}/v1/accounts/{wallet_address}"
        f"/transactions/trc20"
    )

    params = {
        "only_to": "true",
        "limit": 50,
        "contract_address": USDT_CONTRACT,
        "min_timestamp": order_created_ms,
        "order_by": "block_timestamp,asc"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:

            if response.status != 200:
                return None

            result = await response.json()

    for tx in result.get("data", []):
        if tx.get("token_info", {}).get("address") != USDT_CONTRACT:
            continue

        amount = int(tx.get("value", 0)) / 1_000_000

        if abs(amount - expected_amount) < 0.000001:
            if tx.get("to") == wallet_address:
                if tx.get("block_timestamp", 0) >= order_created_ms:
                    return tx.get("transaction_id")

    return None
