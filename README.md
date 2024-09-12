# ✨ Quickstart

### 🛠️ Installation

```sh
pip install web3
pip insstall loguru
pip install 
```

### 📃 General Usage
**Providing the private key and RPC client is not mandatory if you only intend to execute functions for retrieving data.<br>
Otherwise, this is required, for instance, to open a DCA account or to close one.**

**You can set custom URLs for any self-hosted Jupiter APIs. Like the [V6 Swap API](https://station.jup.ag/docs/apis/self-hosted) or [QuickNode's Metis API](https://marketplace.quicknode.com/add-on/metis-jupiter-v6-swap-api).**

If you encounter ```ImportError: cannot import name 'sync_native' from 'spl.token.instructions``` error when trying to import Jupiter, Jupiter_DCA from jupiter_python_sdk.jupiter, follow these steps:
1. Go to https://github.com/michaelhly/solana-py/tree/master/src/spl/token and download ```instructions.py```
2. In your packages folder, replace ```spl/token/instructions.py``` with the one you just downloaded.
