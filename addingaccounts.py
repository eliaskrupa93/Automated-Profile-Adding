import os
import zipfile
import tempfile
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_proxy_extension(proxy_host, proxy_port, proxy_user, proxy_pass): # chrome proxy exetension - code used from internet
    """
    Dynamically creates a Chrome extension (as a .zip file) that sets up a fixed proxy.
    If proxy_user and proxy_pass are provided (non-empty), proxy authentication will be used.
    """
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy Extension",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """
    
    if proxy_user and proxy_pass:
        background_js = f"""
        var config = {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{proxy_host}",
                    port: parseInt({proxy_port})
                }},
                bypassList: ["localhost"]
            }}
        }};
    
        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{ }});
    
        chrome.webRequest.onAuthRequired.addListener(
            function(details) {{
                return {{
                    authCredentials: {{
                        username: "{proxy_user}",
                        password: "{proxy_pass}"
                    }}
                }};
            }},
            {{urls: ["<all_urls>"]}},
            ['blocking']
        );
        """
    else:
        background_js = f"""
        var config = {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{proxy_host}",
                    port: parseInt({proxy_port})
                }},
                bypassList: ["localhost"]
            }}
        }};
    
        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{ }});
        """
    
    plugin_file = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    plugin_file_name = plugin_file.name
    plugin_file.close()
    
    with zipfile.ZipFile(plugin_file_name, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_file_name

def human_type(element, text, delay_min=0.1, delay_max=0.3): # humanize the typing
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(delay_min, delay_max))

def main():
    with open("MODIFY", "r") as f: # read the login credentials - in format username:password - MODIFY
        logins = [line.strip() for line in f if line.strip()]
    
    with open("MODIFY", "r") as f: # read proxies from file - in format ip:port:username:password or ip:port(may have auth issues using this method) - MODIFY
        proxy_lines = [line.strip() for line in f if line.strip()]
    
    logged_in_accounts_file = "MODIFY" # read the account from logged in accounts file - this file is a file with the accounts that are already logged in. if an account is not in here then a login will be attempted - MDOIFY
    logged_in_accounts = set()
    if os.path.exists(logged_in_accounts_file):
        with open(logged_in_accounts_file, "r") as f:
            logged_in_accounts = set(line.strip() for line in f if line.strip())
    
    base_profiles_dir = r"MODIFY" # folder for your seperate profile directories - each profile gets their own profile on chrome - directory in the format C:\x\y\z\n
    os.makedirs(base_profiles_dir, exist_ok=True)
    
    drivers = [] # keep track of the driver instance
    
    for i, login in enumerate(logins):
        try:
            username, password = login.split(":", 1)
        except Exception as e: # line parsing error
            print(f"error for {login} - skipping")
            continue
        
        if login in logged_in_accounts: # skips accounts that are already logged in
            print(f"account {username} is already logged in")
            continue
        
        if i < len(proxy_lines): # makes sure to match a proxy for the account - each account has a unique proxy that is seemlessly linked to it
            proxy_parts = proxy_lines[i].split(":")
            if len(proxy_parts) == 4:
                proxy_host, proxy_port, proxy_user, proxy_pass = proxy_parts
            elif len(proxy_parts) == 2:
                proxy_host, proxy_port = proxy_parts
                proxy_user, proxy_pass = "", ""
            else:
                print(f"Proxy format incorrect for line: {proxy_lines[i]}. Skipping account {username}.")
                continue
        else:
            print(f"No proxy found for account {username}. Skipping.")
            continue
        
        profile_name = f"Profile {i+1}" # creates the profile directory for each account
        profile_dir = os.path.join(base_profiles_dir, profile_name)
        os.makedirs(profile_dir, exist_ok=True)
        
        chrome_options = Options() # chrome options for the account
        chrome_options.add_argument(f"--user-data-dir={profile_dir}")
        chrome_options.add_argument(f"--profile-directory={profile_name}")
        chrome_options.add_argument("--disable-notifications")
        
        proxy_extension_path = create_proxy_extension(proxy_host, proxy_port, proxy_user, proxy_pass) # add the proxy extenstioin to make sure that the account always uses it assigned proy
        chrome_options.add_extension(proxy_extension_path)
        
        print(f"launching browser for {username} using {profile_name} with proxy {proxy_host}:{proxy_port}")
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"error launching chrome for {username}: {e}")
            continue
        
        drivers.append(driver)
        
        driver.get("https://www.instagram.com") # go to instagram.com
        
        try: # wait for the fields to login to appear
            username_field = WebDriverWait(driver, 20).until( 
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
        except Exception as e:
            print(f"Error loading login page for {username}: {e}")
            continue
        
        time.sleep(2) 
        
        username_field.clear()
        password_field.clear() # get rid of any auto fill 
        human_type(username_field, username) # huamnized random typing
        time.sleep(random.uniform(0.5, 1.0))
        human_type(password_field, password)
        time.sleep(random.uniform(0.5, 1.0))
        
        try: # click login button
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
        except Exception as e:
            print(f"issue clicking the login button for {username}: {e}")
        
        print(f"{username} - complete any required 2FA manually in the opened window") # manually enter 2fa information
        
        logged_in_accounts.add(login) # adds the account to the logged in file and set a new file line - there may be an issue with the newlines if you delete a newline in the file
        with open(logged_in_accounts_file, "a") as f:
            f.write(login + "\n")
        
        time.sleep(5)
    
    print("all browser have been launched")
    
    for driver in drivers:
        driver.quit()

if __name__ == "__main__":
    main()