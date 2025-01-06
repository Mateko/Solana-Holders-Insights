import requests

class TopHoldersInsights:
    def __init__(self, api_key, ca):
        self.api_key = api_key
        self.ca = ca
        self.url = f'https://mainnet.helius-rpc.com/?api-key={api_key}'
        self.headers = {"Content-Type": "application/json"}
        self.base_payload = {
            "jsonrpc": "2.0",
            "id": "helius-request"
        }

    def _post_request(self, payload):
        response = requests.post(self.url, headers=self.headers, json=payload)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        if 'error' in data:
            error_message = data['error'].get('message', 'Unknown error occurred.')
            print(f"An error occurred: {error_message}")
            raise ValueError(error_message)

        return data

    def _get_paginated_results(self, method, params, result_key):
        results = []
        payload = self.base_payload.copy()  # Create a fresh payload copy
        payload["method"] = method
        payload["params"] = params

        while True:
            print(payload)
            data = self._post_request(payload)

            if method == 'getAsset':
                items = data.get(result_key, [])
                results.append(items)
            else:   
                items = data['result'].get(result_key, [])
                results.extend(items)


            cursor = data['result'].get('cursor')
            if cursor is None:
                break
            payload["params"]["after"] = cursor

        return results
    
    def get_token_info(self):
        params = {"id": self.ca}
        token_info = self._get_paginated_results("getAsset", params, "result")

        return token_info

    def get_crypto_holders(self):
        """Retrieve crypto holders and their token amounts."""
        params = {"mint": self.ca,
                  "limit": 1000}
        
        token_accounts = self._get_paginated_results("getTokenAccounts", params, "token_accounts")
        top_holders = [
            [account['owner'], int(account['amount'])]
            for account in token_accounts
            if account['owner'] not in ['5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1']
        ]

        return sorted(top_holders, key=lambda x: x[1], reverse=True)

    def get_holder_fungibles(self, holders, n):
        """Retrieve fungible tokens for the top N holders."""
        owner_assets = {}

        for holder in holders[:n]:
            params = {
                "ownerAddress": holder[0],
                "options": {"showFungible": True},
                "limit": 1000
            }
            items = self._get_paginated_results("getAssetsByOwner", params, "items")

            fungibles = [
                [
                    token['content']['metadata'].get('name', 'Unknown'),
                    token['content']['metadata'].get('symbol', 'Unknown'),
                    token['token_info'].get('balance', 0) / (10 ** token['token_info'].get('decimals', 0)),
                    round(token['token_info'].get('price_info', {}).get('total_price', 0), 2),
                    token['token_info'].get('price_info', {}).get('currency', 'Unknown')
                ]
                for token in items if token.get('interface') == 'FungibleToken'
            ]

            owner_assets[holder[0]] = sorted(set(tuple(f) for f in fungibles), key=lambda x: x[3], reverse=True)[0:5]

        return owner_assets
