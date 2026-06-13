import requests
import json
import time

UIDPASS_FILE = "uidpass.json"
TOKEN_FILE = "tokens.json"
API_URL = "https://xtytdtyj-jwt.up.railway.app/token"

MAX_RETRY = 2
TIMEOUT = 15

success = 0
failed = 0

def read_uidpass():
    with open(UIDPASS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_token(uid, password, current, total):
    global success, failed

    print("\n" + "=" * 60)
    print(f"[{current}/{total}] PROCESSING UID: {uid}")
    print("=" * 60)

    url = f"{API_URL}?uid={uid}&password={password}"

    for attempt in range(MAX_RETRY + 1):
        try:
            print(f"TRY {attempt+1}/{MAX_RETRY+1}...")

            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()

            data = response.json()
            token = data.get("token")

            if token:
                success += 1

                print("STATUS  : SUCCESS")
                print(f"TOKEN   : {token[:30]}...")
                print(f"SUCCESS : {success}")
                print(f"FAILED  : {failed}")

                return token

            print("STATUS  : TOKEN NOT FOUND")

        except Exception as e:
            print(f"ERROR   : {e}")

        if attempt < MAX_RETRY:
            print("WAITING 2 SEC...")
            time.sleep(2)

    failed += 1

    print("STATUS  : FAILED")
    print(f"SUCCESS : {success}")
    print(f"FAILED  : {failed}")

    return None

def update_token_file(token_list):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_list, f, indent=4)

def main():
    uidpass_list = read_uidpass()
    total = len(uidpass_list)

    print("\n")
    print("╔══════════════════════════════════════╗")
    print("║      TOKEN UPDATE PROCESS START     ║")
    print("╚══════════════════════════════════════╝")
    print(f"TOTAL ACCOUNT : {total}")

    new_tokens = []

    for i, item in enumerate(uidpass_list, start=1):
        token = fetch_token(
            item["uid"],
            item["password"],
            i,
            total
        )

        if token:
            new_tokens.append({
                "uid": item["uid"],
                "token": token
            })

    update_token_file(new_tokens)

    print("\n")
    print("╔══════════════════════════════════════╗")
    print("║           FINAL REPORT              ║")
    print("╚══════════════════════════════════════╝")
    print(f"TOTAL   : {total}")
    print(f"SUCCESS : {success}")
    print(f"FAILED  : {failed}")
    print(f"SAVED   : {len(new_tokens)}")

if __name__ == "__main__":
    main()