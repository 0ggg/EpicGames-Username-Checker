from curl_cffi import requests
import threading, random, string

length = input("Enter Username Length (3-16) : ")
threads = input("Threads : ")

def thread():
    while True:
        user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=int(length)))
        session = requests.Session(impersonate="chrome120")
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            "priority": "u=1, i",
            "sec-ch-ua": '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        session.get('https://www.epicgames.com/id/register', headers=headers)
        r1 = session.get('https://www.epicgames.com/id/api/authenticate', headers=headers)
        try:
            xsrf = session.cookies.get_dict().get("XSRF-TOKEN")
            if xsrf:
                headers["x-xsrf-token"] = xsrf
        except:
            pass
        r = session.post('https://www.epicgames.com/id/api/account/displayName/validate', headers=headers, json={'displayName': user})
        if r.status_code == 200:
            print(f"[+] Available : {user}")
        elif 'duplicate_display_name' in r.text:
            print(f"[-] Taken : {user}")
        elif '</html>' in r.text or r.status_code or 'errors.com.epicgames.accountportal.csrf_token_invalid' in r.text == 429:
            print(f"[-] Rate Limited : {user}")
        else:
            print(r.text)

for _ in range(int(threads)):
    threading.Thread(target=thread, daemon=True).start()
print("Dev : Legend ~ .gg/cupspy")
input("Press Enter To Stop\n")
