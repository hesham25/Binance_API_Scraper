import pandas as pd 
from binance.client import Client
from time import sleep

results = []
print('Loading symbols_list from excel file (CryptoTrading_symboles)')
file = open('CREDS.txt','r')
for line in file.readlines():
	if 'secret_key =' in line : secret_key = line.replace('secret_key =','').strip()
	elif 'api_key =' in line : api_key = line.replace('api_key =','').strip()
file.close()


client = Client(api_key=api_key, api_secret=secret_key)
symbols_list = pd.read_excel('CryptoTrading_symboles.xlsx')['symbols'].tolist()

for i, sy in enumerate(symbols_list):
	print(f'Getting symbol {i+1} of {len(symbols_list)} >> {sy}')
	row = {}
	for label in ['BTC', 'USDT'] :
		symbol = f'{sy}{label}'
		try :
			response = client.get_ticker(symbol=symbol)
			row[f'symbol {label}']  = sy
			row[f'Currency_Pair {label}']  = response['symbol']
			row[f'lastPrice {label}']  = float(response['lastPrice'])
			row[f'openPrice {label}']  = float(response['openPrice'])
			row[f'lowPrice {label}']  = float(response['lowPrice'])
			row[f'highPrice {label}']  = float(response['highPrice'])
			row[f'priceChange {label}']  = float(response['priceChange'])
			row[f'priceChangePercent {label}']  = float(response['priceChangePercent'])
			row[f'prevClosePrice {label}']  = float(response['prevClosePrice'])
			row[f'volume {label}']  = float(response['volume'])
			row[f'quoteVolume {label}']  = float(response['quoteVolume'])
		except :
			row[f'symbol {label}']  = sy
			row[f'Currency_Pair {label}']  = symbol
			row[f'lastPrice {label}']  = None
			row[f'openPrice {label}']  = None
			row[f'lowPrice {label}']  = None
			row[f'highPrice {label}']  = None
			row[f'priceChange {label}']  = None
			row[f'priceChangePercent {label}']  = None
			row[f'prevClosePrice {label}']  = None
			row[f'volume {label}']  = None
			row[f'quoteVolume {label}']  = None
	results.append(row)
print('Saving results...')
df = pd.DataFrame(results)
df.to_excel('CryptoTrading_Trades.xlsx', index=False)
print('finished Saving results to CryptoTrading_Trades')
sleep(10)
