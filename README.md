# Binance Futures Trading Bot (Testnet)

A Python-based trading bot for Binance Futures Testnet with support for market, limit, and stop-limit orders. Designed for strategy testing and educational purposes.

![CLI Example](https://via.placeholder.com/800x200.png?text=CLI+Execution+Demo) 
*(Replace with actual screenshot if available)*

## Features

- 🚀 **Order Types Supported**
  - Market Orders
  - Limit Orders
  - Stop-Limit Orders (Advanced)
- 📊 **Testnet Integration**
  - Full compatibility with Binance Futures Testnet
  - Safe environment for trading experiments
- 📝 **Comprehensive Logging**
  - File-based activity logging (`bot_activity.log`)
  - Detailed API request/response tracking
- 🛡 **Robust Error Handling**
  - Input validation
  - API error catching
  - Graceful failure handling
- 💻 **CLI Interface**
  - Emoji-enhanced output
  - Interactive argument parsing
  - Clear execution feedback

## Requirements

- Python 3.6+
- Binance Testnet Account
- Testnet API Credentials

## Installation

1. **Clone Repository**

git clone https://github.com/yourusername/binance-trading-bot.git
cd binance-trading-bot

2. **Install Dependencies**

pip install python-binance argparse

3. **Set Up Testnet Account**

Register at Binance Testnet

Generate API keys in Testnet Account Settings

## Usage
1. **Basic Command Structure**

python bot.py \
  --api_key YOUR_API_KEY \
  --api_secret YOUR_API_SECRET \
  --symbol SYMBOL \
  --side SIDE \
  --type ORDER_TYPE \
  --quantity QUANTITY \
  [--price PRICE] \
 
## Configuration
1. **Required Parameters**
Argument	            Description	                Example
--api_key	          Testnet API key	            test123
--api_secret         Testnet API secret	            test456
--symbol	            Trading pair                BTCUSDT
--side	         Order direction (BUY/SELL)	          BUY
--type	   Order type (MARKET/LIMIT/STOP_LIMIT)    STOP_LIMIT
--quantity	           Order quantity	              0.01
2. **Optional Parameters**
Argument	            Description	               Required For
--price	                Limit price	             LIMIT/STOP_LIMIT
--stop_price	Activation price for stop-loss	    STOP_LIMIT