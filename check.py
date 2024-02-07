import binascii
import hashlib
from time import sleep

import base58
import requests
import json

import ecdsa

from btcaddr import Wallet
from time import sleep
from fake_user_agent import user_agent
from fake_useragent import UserAgent
import random
import proxies


def generate_addresses(count):
    addresses = {}
    for i in range(count):
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = b'\04' + private_key.get_verifying_key().to_string()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(public_key).digest())
        r = b'\0' + ripemd160.digest()
        checksum = hashlib.sha256(hashlib.sha256(r).digest()).digest()[0:4]
        address = base58.b58encode(r + checksum)
        addresses[address.decode()] = binascii.b2a_hex(private_key.to_string()).decode()

        """
        wallet = Wallet()
        pub = wallet.address.__dict__["mainnet"].__dict__["pubaddr1"]
        prv = wallet.key.__dict__["mainnet"].__dict__["wif"]
        addresses[pub] = prv
        """

    return addresses


def check_balance_btc():
    try:
        data = generate_addresses(random.randint(1, 50))
        ua = UserAgent()
        addresses = "|".join(data.keys())
        status_code = 0
        url = f"https://blockchain.info/multiaddr?active={addresses}"
        response = None
        while status_code != 200:
            if not len(proxies.proxy_list):
                proxies.download_proxy_list()
            took_proxy = random.choice(proxies.proxy_list)
            proxy = {"http": took_proxy}
            headers = {
                "User-Agent": ua.getRandom
            }
            response = requests.get(url, headers, proxies=proxy)
            if response.status_code == 200:
                status_code = 200
                response = response.json()
            else:
                with open("results/errors.txt", "a") as f:
                    f.write(
                        f"error while trying to check wallets, status code = {response.status_code}, proxy = {took_proxy}\n{response.request}\n"
                    )
                proxies.proxy_list.remove(took_proxy)
        sleep(0.5)
        extract = []
        for address in response["addresses"]:
            # add all data into a list
            extract.append({
                "address": address["address"],
                "balance": address["final_balance"],
                "private": data[address["address"]]
            })
        return extract
    except:
        pass


"""def last_seen_bc(address):

    try:
        address = address
        reading_state = 1
        while reading_state:
            try:
                htmlfile = urlopen(
                    f"https://blockchain.info/q/addressfirstseen/{address}?format=json",
                    timeout=10,
                )
                htmltext = htmlfile.read().decode("utf-8")
                reading_state = 0
            except:
                reading_state += 1
                sleep(60 * reading_state)
        ts = int(htmltext)
        if ts == 0:
            return 0
        return str(datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"))
    except:
        return None
"""
