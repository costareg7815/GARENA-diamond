
# 🛒 Shop2Game Automation Tool

A process automation tool for the [Shop2Game](https://shop2game.com) website using Python and an image-based graphical interface via PyAutoGUI.

---

## 💡 The Idea

The script opens the browser in Incognito mode and repeats a certain number of attempts, which include:

- Opening the website.
- Entering the **player ID**.

<img width="405" height="147" alt="Image" src="https://github.com/user-attachments/assets/463533e8-fe7e-468f-b10e-38e3079e2431" />

- Selecting specific options that appear on the screen.
- Entering a 16-digit (random) card number.
- Performing the rest of the steps automatically.

---

## ⚙️ Requirements

- Python 3.8 or higher.
- Google Chrome (default path:
`C:\Program Files\Google\Chrome\Application\chrome.exe`)
- The following Python libraries:
- `pyautogui`
- `colorama`
- `threading` (included)
- `subprocess` (included)
- `os`, `sys`, `random`, `time`

**To install missing packages:**

```bash
pip install pyautogui colorama
````

---

## 🌍 Language Support

The script supports two languages:

* 🇺🇸 English
* 🇪🇬 Arabic

When running the script, you can select the language.

---

## 🧾 Important Note – The Constant Number (Player ID)

Inside the code, in this section:

```python
pyautogui.write("12????????")
```

You must **replace** `"12????????"` with **your Player ID** that you use in Shop2Game.

---

## 🔌 Proxy Support (Optional)

You can use a text file containing a list of proxies (proxy list) in the form:

```
123.123.123.123:8080
111.111.111.111:3128
...
```

When you run the script, you will be prompted:

* Do you want to use the proxy? (y/n)
* File name? (Example: `proxies.txt`)

---

## 🖼️ Required Images

The following images must be placed in the same folder as the script:

* `step1.png` → ID entry button image
* `step2.png` → Next button image
* `step3.png` → Confirmation button or step
* `step4.png` → Card number entry field
* `step5.png` → Final button

These images must closely match the screen for the `pyautogui.locateCenterOnScreen()` feature to work.

---

## 🚀 How to Run

1. Ensure Google Chrome is running and installed in the correct path.
2. Run the script from Terminal or CMD:

```bash
python shop2game.py
```

3. Select the language.
4. Specify the number of attempts.
5. Choose whether or not to use a proxy.

---

## 🎨 Launch Appearance

When running, you'll see a colorful banner, an animated spinner during searches, and success or failure messages explaining the steps.

---

## ⚠️ Legal Warning

> This project is for educational purposes only. Do not use the script to perform fake operations or on accounts you don't own.
> Misuse may result in your account being banned or a violation of the site's Terms of Use.

---

## 👨‍💻 Made by

**KIRA99**
Powered by Python 🐍

