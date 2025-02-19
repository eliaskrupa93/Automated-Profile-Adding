# Instagram Account Adder

This project automates the process of logging into multiple Instagram accounts, each using a unique proxy through dynamically created Chrome extensions. It uses Python and Selenium to launch separate Chrome profiles, handle login credentials, and apply proxies for each session.

## Files Included

- **addingaccounts.py**  
  The main Python script that:
  - Reads account credentials and proxies from text files (user-modified paths).
  - Creates and loads a custom Chrome extension for each proxy.
  - Launches a separate Chrome profile for each account.
  - Simulates human-like typing and handles the Instagram login flow.

- **background.js**  
  A background script (template) used in the Chrome extension to set the proxy and optionally handle authentication events.

- **manifest.json**  
  A basic Chrome extension manifest that requests permissions and specifies the background script.

## How It Works

1. **Reading Credentials and Proxies:**  
   - The script expects a file containing Instagram login credentials in the format `username:password`.
   - Another file lists proxies in the format `IP:PORT:USERNAME:PASSWORD` or `IP:PORT`.

2. **Creating Chrome Extension for Each Proxy:**  
   - The script dynamically generates a ZIP file containing `manifest.json` and a modified `background.js` that configures the proxy settings.
   - If a username and password are provided for the proxy, it sets up proxy authentication.

3. **Launching Separate Profiles:**  
   - Each account is assigned a unique Chrome profile directory, ensuring isolated sessions.
   - A custom proxy extension is loaded for each session, so traffic routes through that specific proxy.

4. **Human-Like Typing:**  
   - The script simulates human typing delays when entering login credentials, making it appear more natural.

5. **Handling 2FA (if required):**  
   - If Instagram prompts for two-factor authentication, the user must complete it manually in the opened Chrome window.

6. **Logging Accounts:**  
   - Once an account is successfully launched, it’s recorded in a separate file to prevent re-login attempts.

## Prerequisites

- **Python 3.x**  
- **Selenium** (`pip install selenium`)  
- **ChromeDriver** (download from [ChromeDriver](https://chromedriver.chromium.org/) and place it in your system PATH)  
- **Google Chrome** installed

## Setup & Usage

1. **Clone or Download this Repository:**  
   Place `addingaccounts.py`, `background.js`, and `manifest.json` in the same folder.

2. **Install Dependencies:**
   ```bash
   pip install selenium
   ```

3. **Prepare Input Files:**
   - A file containing Instagram credentials, each in `username:password` format.
   - A file containing proxies, each in `IP:PORT` or `IP:PORT:USERNAME:PASSWORD` format.
   - (Optional) A file to keep track of already logged-in accounts (if desired).

4. **Configure the Script:**
   - Update `addingaccounts.py` with the correct file paths (e.g., `MODIFY` placeholders).
   - Set the output directory for separate Chrome profiles (`base_profiles_dir`).
   - Adjust any additional parameters like time delays as needed.

5. **Run the Script:**
   ```bash
   python addingaccounts.py
   ```
   - Multiple Chrome windows will open, each attempting to log in to a different Instagram account using its assigned proxy.
   - If Instagram prompts for two-factor authentication, complete it manually.

6. **Monitor and Manage:**
   - Check the console output for any errors or skipped accounts.
   - Once finished, close the Chrome windows or let the script quit them automatically.

## Notes & Customization

- **Proxy Authentication:**  
  If your proxies require a username and password, ensure the script detects and sets them correctly.
- **Two-Factor Authentication (2FA):**  
  Currently, this script does not automate 2FA. You must handle it manually if prompted.
- **Error Handling:**  
  The script attempts to skip and log any accounts that fail or have incorrect credentials.

## Disclaimer

This script is provided for educational and personal use. Be aware of Instagram’s terms of service and usage policies. The author is not responsible for any account bans, restrictions, or other consequences arising from misuse.
