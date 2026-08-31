import os
import requests

def get_options_chain_snapshot(ticker="SPY"):
    api_key = os.getenv("FINANCIAL_API_KEY", "YOUR_API_KEY")
    endpoint = f"https://financialmodelingprep.com/api/v3/options-chain/{ticker}"
    
    params = {"apikey": api_key}
    
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        chain = response.json()
        print(f"--- Multi-Leg Options Engine: Snapshot [{ticker}] ---")
        # Display top 3 near-the-money options contracts
        for contract in chain[:3]:
            strike = contract.get("strike")
            option_type = contract.get("type")
            bid = contract.get("bid")
            ask = contract.get("ask")
            implied_vol = contract.get("impliedVolatility")
            
            print(f"Type: {option_type.upper()} | Strike: ${strike} | Bid/Ask: ${bid}/${ask} | IV: {implied_vol}")
    else:
        print(f"Market Data Request Error: HTTP {response.status_code}")

# Example Run
get_options_chain_snapshot("SPY")