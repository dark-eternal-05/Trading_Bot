import argparse
import logging
from binance import Client
from binance.exceptions import BinanceAPIException
class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """Initialize the trading bot with API credentials"""
        self.client = Client(
            api_key,
            api_secret,
            testnet=testnet,
            futures_testnet=testnet
        )
        self._setup_logger()
        
    def _setup_logger(self):
        """Configure logging system"""
        self.logger = logging.getLogger('TradingBot')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        
        # File handler
        fh = logging.FileHandler('bot_activity.log')
        fh.setFormatter(formatter)

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
        self.logger.propagate = False

    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Place a futures order with validation and error handling
        Returns order response or raises exception
        """
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': order_type.upper(),
            'quantity': quantity
        }

        if order_type.upper() == 'LIMIT':
            if not price:
                raise ValueError("Price is required for limit orders")
            params.update({
                'price': price,
                'timeInForce': 'GTC'
            })

        try:
            self.logger.info(f"Attempting order: {params}")
            response = self.client.futures_create_order(**params)
            self.logger.info(f"Order successful: {response}")
            return response
        except BinanceAPIException as e:
            self.logger.error(f"API Error {e.status_code}: {e.message}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise

def validate_input(args):
    """Validate command-line arguments"""
    if args.order_type == 'LIMIT' and not args.price:
        raise ValueError("Price is required for limit orders")
    if args.quantity <= 0:
        raise ValueError("Quantity must be positive")
    return args

def main():
    """Command-line interface and order execution"""
    parser = argparse.ArgumentParser(description='Binance Futures Trading Bot')
    parser.add_argument('--api_key', required=True, help='API Key')
    parser.add_argument('--api_secret', required=True, help='API Secret')
    parser.add_argument('--symbol', required=True, help='Trading pair (e.g., BTCUSDT)')
    parser.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('--type', required=True, choices=['MARKET', 'LIMIT'], 
                       dest='order_type', help='Order type')
    parser.add_argument('--quantity', required=True, type=float, help='Order quantity')
    parser.add_argument('--price', type=float, help='Limit price (required for limit orders)')

    try:
        args = parser.parse_args()
        args = validate_input(args)
        
        bot = BasicBot(args.api_key, args.api_secret)
        response = bot.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price
        )

        # Print formatted results
        print("\nOrder Execution Details:")
        print(f"ID: {response['orderId']}")
        print(f"Status: {response['status']}")
        print(f"Symbol: {response['symbol']}")
        print(f"Side: {response['side']}")
        print(f"Type: {response['type']}")
        print(f"Quantity: {response['origQty']}")
        if args.price:
            print(f"Price: {response['price']}")
        print(f"Executed Qty: {response['executedQty']}")

    except Exception as e:
        print(f"\nError: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
    
class AdvancedBot(BasicBot):
    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """
        Enhanced order placement with support for stop-limit orders
        """
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'quantity': quantity,
            'type': order_type.upper()  # Default type, might be overridden
        }

        # Handle different order types
        if order_type.upper() == 'LIMIT':
            if not price:
                raise ValueError("Price is required for limit orders")
            params.update({
                'price': price,
                'timeInForce': 'GTC'
            })
        elif order_type.upper() == 'STOP_LIMIT':
            params['type'] = 'STOP'  # Binance API requires 'STOP' type
            if not price or not stop_price:
                raise ValueError("Both price and stop_price are required for stop-limit orders")
            params.update({
                'price': price,
                'stopPrice': stop_price,
                'timeInForce': 'GTC'
            })

        try:
            self.logger.info(f"Attempting order: {params}")
            response = self.client.futures_create_order(**params)
            self.logger.info(f"Order successful: {response}")
            return response
        except BinanceAPIException as e:
            self.logger.error(f"API Error {e.status_code}: {e.message}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise

def validate_input(args):
    """Enhanced validation for advanced order types"""
    if args.order_type == 'LIMIT' and not args.price:
        raise ValueError("Price is required for limit orders")
    if args.order_type == 'STOP_LIMIT':
        if not args.price or not args.stop_price:
            raise ValueError("Both price and stop_price are required for STOP_LIMIT orders")
    if args.quantity <= 0:
        raise ValueError("Quantity must be positive")
    return args

def main():
    """Enhanced CLI with support for advanced orders"""
    parser = argparse.ArgumentParser(
        description='Binance Futures Trading Bot with Advanced Orders',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--api_key', required=True, help='API Key')
    parser.add_argument('--api_secret', required=True, help='API Secret')
    parser.add_argument('--symbol', required=True, help='Trading pair (e.g., BTCUSDT)')
    parser.add_argument('--side', required=True, 
                       choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('--type', required=True, 
                       choices=['MARKET', 'LIMIT', 'STOP_LIMIT'], 
                       dest='order_type', help='Order type')
    parser.add_argument('--quantity', required=True, type=float, help='Order quantity')
    parser.add_argument('--price', type=float, help='Limit/Stop price')
    parser.add_argument('--stop_price', type=float, 
                       help='Stop price (required for STOP_LIMIT)')

    try:
        args = parser.parse_args()
        args = validate_input(args)
        
        bot = AdvancedBot(args.api_key, args.api_secret)
        response = bot.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )

        # Enhanced output formatting
        print("\n🚀 Order Execution Details:")
        print(f"🔑 ID: {response['orderId']}")
        print(f"📊 Status: {response['status']}")
        print(f"🏷  Symbol: {response['symbol']}")
        print(f"📈 Side: {response['side']}")
        print(f"🔧 Type: {args.order_type} (API Type: {response['type']})")
        print(f"📦 Quantity: {response['origQty']}")
        
        if args.price:
            print(f"💰 Price: {response.get('price', 'N/A')}")
        if args.stop_price:
            print(f"🛑 Stop Price: {response.get('stopPrice', 'N/A')}")
            
        print(f"✅ Executed Qty: {response['executedQty']}")
        print(f"📝 Client Order ID: {response.get('clientOrderId', 'N/A')}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()