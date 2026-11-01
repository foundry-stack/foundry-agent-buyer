"""
FOUNDRY AGENT BUYER (PYTHON) — Production Ready Client Library
--------------------------------------------------------------
Enables AI agents, Python bots, and autonomous scripts to complete
RFC-compliant HTTP 402 challenge-response cryptocurrency purchases on Base and Avalanche.

Features:
- Handles standard RFC HTTP 402 Payment Required challenges.
- Signs cryptographic challenge nonces with the agent's EVM private key.
- Builds, signs, and broadcasts on-chain ERC-20 USDC payments automatically.
- Waits for on-chain block receipt confirmation.
- Submits cryptographic proof of payment and claims digital payload.
- Saves downloaded payload directly to disk or returns raw content.

Author: Foundry Stack (https://foundrystack.co.uk)
License: MIT
"""

import os
import sys
import json
import base64
import time
import requests
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

# Official Standard ERC-20 Minimal ABI (transfer, balanceOf, decimals)
ERC20_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]

# Supported Networks & Verified Contract Addresses
SUPPORTED_CHAINS = {
    8453: {
        "name": "Base Mainnet",
        "caip": "eip155:8453",
        "rpc": "https://mainnet.base.org",
        "fallback_rpcs": [
            "https://base.llamarpc.com",
            "https://base-rpc.publicnode.com"
        ],
        "usdc": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "decimals": 6
    },
    43114: {
        "name": "Avalanche C-Chain",
        "caip": "eip155:43114",
        "rpc": "https://api.avax.network/ext/bc/C/rpc",
        "fallback_rpcs": [
            "https://avalanche-c-chain-rpc.publicnode.com",
            "https://1rpc.io/avax/c"
        ],
        "usdc": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
        "decimals": 6
    }
}


class AutonomousBuyer:
    """
    Autonomous HTTP 402 Client for AI Agents.
    """

    def __init__(self, private_key: str, chain_id: int = 8453, rpc_url: str = None):
        """
        Initialize the autonomous buyer with an EVM private key.
        """
        if not private_key:
            raise ValueError("Private key is required to initialize AutonomousBuyer.")

        if not private_key.startswith("0x"):
            private_key = "0x" + private_key

        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.chain_id = chain_id

        if self.chain_id not in SUPPORTED_CHAINS:
            raise ValueError(f"Unsupported chain_id: {chain_id}. Supported: {list(SUPPORTED_CHAINS.keys())}")

        self.chain_info = SUPPORTED_CHAINS[self.chain_id]
        primary_rpc = rpc_url or self.chain_info["rpc"]
        self.w3 = Web3(Web3.HTTPProvider(primary_rpc))

        # Fallback RPC verification if primary fails
        if not self.w3.is_connected():
            for fallback in self.chain_info.get("fallback_rpcs", []):
                self.w3 = Web3(Web3.HTTPProvider(fallback))
                if self.w3.is_connected():
                    break

        self.usdc_address = Web3.to_checksum_address(self.chain_info["usdc"])
        self.usdc_contract = self.w3.eth.contract(address=self.usdc_address, abi=ERC20_ABI)

    def get_usdc_balance(self) -> float:
        """Fetch current USDC balance for the agent wallet."""
        raw_bal = self.usdc_contract.functions.balanceOf(self.address).call()
        return raw_bal / (10 ** self.chain_info["decimals"])

    def get_eth_balance(self) -> float:
        """Fetch native gas coin balance (ETH or AVAX)."""
        raw_bal = self.w3.eth.get_balance(self.address)
        return float(self.w3.from_wei(raw_bal, "ether"))

    def purchase(self, product_url: str, output_path: str = None, timeout: int = 60) -> bytes:
        """
        Execute full autonomous purchase flow against an HTTP 402 protected URL.
        """
        # 1. Probe endpoint to receive 402 Payment Required Challenge
        resp = requests.get(product_url, timeout=timeout)
        if resp.status_code == 200:
            print("[+] Endpoint returned 200 OK without payment required.")
            data = resp.content
            if output_path:
                with open(output_path, "wb") as f:
                    f.write(data)
            return data

        if resp.status_code != 402:
            raise RuntimeError(f"Unexpected status code {resp.status_code}: {resp.text}")

        # 2. Parse Challenge Header
        challenge_header = resp.headers.get("X-Challenge")
        if not challenge_header:
            raise RuntimeError("Missing 'X-Challenge' header in HTTP 402 response.")

        challenge_data = json.loads(base64.b64decode(challenge_header).decode("utf-8"))
        merchant_wallet = Web3.to_checksum_address(challenge_data["wallet"])
        price_usdc = float(challenge_data["price_usdc"])
        nonce = challenge_data["nonce"]

        # 3. Cryptographically Sign the Challenge Nonce
        msg_hash = encode_defunct(text=nonce)
        signed_nonce = self.account.sign_message(msg_hash).signature.hex()

        # 4. Check balances
        current_usdc = self.get_usdc_balance()
        if current_usdc < price_usdc:
            raise RuntimeError(f"Insufficient USDC. Required: {price_usdc}, Available: {current_usdc}")

        # 5. Broadcast On-Chain USDC Transfer
        amount_atomic = int(price_usdc * (10 ** self.chain_info["decimals"]))
        nonce_tx = self.w3.eth.get_transaction_count(self.address)
        gas_price = self.w3.eth.gas_price

        tx = self.usdc_contract.functions.transfer(
            merchant_wallet,
            amount_atomic
        ).build_transaction({
            "chainId": self.chain_id,
            "from": self.address,
            "nonce": nonce_tx,
            "gas": 100000,
            "gasPrice": int(gas_price * 1.2)
        })

        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hex = tx_hash.hex()
        print(f"[+] Payment broadcasted: {tx_hex} on {self.chain_info['name']}")

        # 6. Wait for On-Chain Confirmation
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        if receipt.status != 1:
            raise RuntimeError(f"On-chain transaction reverted: {tx_hex}")

        print(f"[+] Payment confirmed in block {receipt.blockNumber}!")

        # 7. Claim and Download Payload
        claim_payload = {
            "tx_hash": tx_hex,
            "nonce_signature": signed_nonce,
            "wallet_address": self.address,
            "chain_id": self.chain_id
        }

        claim_resp = requests.post(
            product_url,
            json=claim_payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )

        if claim_resp.status_code != 200:
            raise RuntimeError(f"Failed to claim product ({claim_resp.status_code}): {claim_resp.text}")

        content = claim_resp.content
        if output_path:
            with open(output_path, "wb") as f:
                f.write(content)
            print(f"[+] Successfully saved payload to {output_path} ({len(content)} bytes)")

        return content
