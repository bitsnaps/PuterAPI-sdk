import json
import urllib.request
import urllib.error
import urllib.parse
import os
import getpass
from pathlib import Path

class PuterAuth:
    def __init__(self):
        self.base_url = "https://puter.com/login"
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://puter.com",
            "Referer": "https://puter.com/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        }

    def login(self, username: str, password: str) -> str:
        data = json.dumps({"username": username, "password": password}).encode('utf-8')
        req = urllib.request.Request(
            self.base_url,
            data=data,
            headers=self.headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get("proceed"):
                    return result['token']
        except urllib.error.URLError as e:
            print(f"Connection error: {e.reason}")
        except json.JSONDecodeError:
            print("Invalid response from server")
        return None

    @staticmethod
    def save_token(token: str) -> None:
        env_path = Path('.env')
        content = f"PUTER_API_KEY={token}\n"
        
        if env_path.exists():
            with open(env_path, 'r') as f:
                lines = f.readlines()
                
            # Remove existing PUTER_API_KEY line if exists
            lines = [line for line in lines if not line.startswith('PUTER_API_KEY=')]
            lines.append(content)
            
            with open(env_path, 'w') as f:
                f.writelines(lines)
        else:
            with open(env_path, 'w') as f:
                f.write(content)

def main():
    print("=== Puter Authentication CLI ===")
    auth = PuterAuth()
    
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")

    print("\nConnecting to Puter...")
    token = auth.login(username, password)

    if token:
        print("\n✓ Login successful!")
        print(f"Token: {token[:20]}...{token[-20:]}")
        
        save = input("\nDo you want to save the token to .env file? (y/N): ").lower().strip()
        if save == 'y':
            try:
                auth.save_token(token)
                print("✓ Token saved to .env file")
            except Exception as e:
                print(f"× Failed to save token: {e}")
    else:
        print("× Login failed. Please check your credentials.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
    except Exception as e:
        print(f"\n× An unexpected error occurred: {e}")
