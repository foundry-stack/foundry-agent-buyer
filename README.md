# ⚡ Foundry Agent Buyer (`foundry-agent-buyer`)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Base Mainnet](https://img.shields.io/badge/network-Base%20(8453)-0052FF.svg)](https://base.org)
[![Avalanche C-Chain](https://img.shields.io/badge/network-Avalanche%20(43114)-E84142.svg)](https://avax.network)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Zero-configuration Python client library allowing autonomous AI agents, LLM pipelines, and automated bots to execute instant HTTP 402 cryptocurrency purchases on Base and Avalanche.**

Built by [Foundry Stack](https://foundrystack.co.uk) — Turnkey Commercial Infrastructure for the Autonomous Agent Economy.

---

## ⚡ The Problem: Why Agents Need This

Traditional payment processors (Stripe, PayPal, banking APIs) require:
- ❌ Human identity verification / KYC
- ❌ Corporate registration & merchant bank accounts
- ❌ Complex OAuth / credit card capture forms impossible for headless agents

**HTTP 402** changes this. When an AI agent encounters a paid API or digital asset, the server returns `402 Payment Required` with a cryptographic challenge. `foundry-agent-buyer` enables any Python agent to:
1. Detect the 402 challenge automatically.
2. Sign the challenge nonce with its EVM key.
3. Broadcast USDC on Base or Avalanche C-Chain.
4. Download the unlocked payload in seconds.

---

## 🚀 Quickstart (3 Lines of Code)

```bash
pip install foundry-agent-buyer
```

```python
from foundry_agent_buyer import AutonomousBuyer

# 1. Initialize with your agent's private key
buyer = AutonomousBuyer(private_key="0xYOUR_AGENT_PRIVATE_KEY")

# 2. Autonomously purchase and download the digital asset
buyer.purchase("https://foundrystack.co.uk/tools/latency-oracle", output_path="tool.zip")
```

---

## 🛠️ Multichain Support (Base & Avalanche)

By default, purchases execute on **Base Mainnet** (`chainId: 8453`). To purchase on **Avalanche C-Chain**:

```python
buyer = AutonomousBuyer(
    private_key="0xYOUR_AGENT_PRIVATE_KEY",
    chain_id=43114 # Avalanche C-Chain
)

buyer.purchase("https://foundrystack.co.uk/item/sample", output_path="item.zip")
```

Custom private RPCs (Alchemy, Infura, QuickNode) are fully supported:

```python
buyer = AutonomousBuyer(
    private_key="0x...",
    chain_id=8453,
    rpc_url="https://base-mainnet.g.alchemy.com/v2/YOUR_API_KEY"
)
```

---

## 🏗️ Want to Sell to AI Agents? Monetize Your Own APIs & Models

This repository provides the **Client (Buyer)** SDK. If you are building an AI agent, tool, or API and want to **charge agents in crypto**:

### Option 1: Turnstile Engine ($19 USDC)
Drop-in FastAPI / Flask decorator for your existing backend.
- Full EIP-712 cryptographic verification.
- Replay-attack prevention & PostgreSQL/SQLite receipt logging.
- Dual-chain Base & Avalanche settlement directly into your wallet.
👉 **[Get the Turnstile Engine ($19)](https://foundrystack.co.uk/#turnstile-engine)**

### Option 2: Turnkey Autonomous Digital Vending Machine (£289 / $365 USDC)
The complete, self-hosted autonomous digital vending machine.
- 1-click Web3 modal browser storefront + HTTP 402 autonomous endpoint.
- 24/7 background SMTP email dispatcher & download link generator.
- Multi-node federation, telemetry radar, and zero-maintenance architecture.
👉 **[Deploy the Franchise Pack (£289)](https://foundrystack.co.uk/#franchise-pack)**

---

## 📄 License
MIT License. Created by [Foundry Stack](https://foundrystack.co.uk).
*"You bring the agent. We give them the shop."*
