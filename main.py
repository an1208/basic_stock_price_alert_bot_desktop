import yfinance as yf
from plyer import notification
import schedule
import time
from datetime import datetime

class StockAlertBot:
    def __init__(self, symbol, target_price, alert_type='above'):
        """
        Initialize the alert bot
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            target_price: Price threshold for alert
            alert_type: 'above' or 'below' - when to trigger alert
        """
        self.symbol = symbol.upper()
        self.target_price = target_price
        self.alert_type = alert_type
        self.alert_triggered = False
        
    def get_current_price(self):
        """Fetch current stock price"""
        try:
            stock = yf.Ticker(self.symbol)
            data = stock.history(period='1d')
            
            if not data.empty:
                return data['Close'].iloc[-1]
            return None
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None
    
    def send_notification(self, current_price):
        """Send desktop notification"""
        title = f"🚨 {self.symbol} Price Alert!"
        message = (f"Current Price: ${current_price:.2f}\n"
                   f"Target: ${self.target_price:.2f}\n"
                   f"Condition: {self.alert_type}")
        
        notification.notify(
            title=title,
            message=message,
            app_name='Stock Alert Bot',
            timeout=15
        )
        print(f"\n{'='*50}")
        print(f"ALERT TRIGGERED!")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{message}")
        print(f"{'='*50}\n")
    
    def check_price(self):
        """Check price and send alert if condition is met"""
        current_price = self.get_current_price()
        
        if current_price is None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to fetch price")
            return
        
        # Display current status
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.symbol}: ${current_price:.2f} | Target: ${self.target_price:.2f} ({self.alert_type})")
        
        # Check if alert condition is met
        should_alert = False
        if self.alert_type == 'above' and current_price >= self.target_price:
            should_alert = True
        elif self.alert_type == 'below' and current_price <= self.target_price:
            should_alert = True
        
        # Send alert only once
        if should_alert and not self.alert_triggered:
            self.send_notification(current_price)
            self.alert_triggered = True
        elif not should_alert and self.alert_triggered:
            # Reset alert if price goes back
            self.alert_triggered = False
            print(f"Alert reset - price moved away from target")
    
    def run(self, check_interval_minutes=10):
        """
        Start monitoring the stock price
        
        Args:
            check_interval_minutes: How often to check (default: 10 minutes)
        """
        print(f"\n{'='*60}")
        print(f"Stock Alert Bot Started")
        print(f"{'='*60}")
        print(f"Symbol: {self.symbol}")
        print(f"Target Price: ${self.target_price:.2f}")
        print(f"Alert Type: {self.alert_type.upper()}")
        print(f"Check Interval: Every {check_interval_minutes} minutes")
        print(f"{'='*60}\n")
        
        # Check immediately on start
        self.check_price()
        
        # Schedule periodic checks
        schedule.every(check_interval_minutes).minutes.do(self.check_price)
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nBot stopped by user")

# Example Usage
if __name__ == "__main__":
    # Configuration
    STOCK_SYMBOL = "NVDA"       # Change to any stock symbol
    TARGET_PRICE = 150.00       # Your target price
    ALERT_TYPE = "above"        # "above" or "below"
    CHECK_INTERVAL = 10         # Minutes between checks
    
    # Create and run bot
    bot = StockAlertBot(
        symbol=STOCK_SYMBOL,
        target_price=TARGET_PRICE,
        alert_type=ALERT_TYPE
    )
    
    bot.run(check_interval_minutes=CHECK_INTERVAL)
