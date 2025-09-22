# Telegram Echo Bot with Fancy Fonts 🎨

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com)

A stylish **Telegram echo bot** that repeats all your messages in **different fancy font styles** and formats!

---

## ✨ Features

- 🎨 **Stylized Texts** – echoes messages in multiple fonts
- ✨ **30+ Font Styles**: Bold, Italic, Script, Fraktur, Double, Monospace, Circled, Squared, Smallcaps, Tiny, Upside Down, Gothic, Outline, Strikethrough, Underline, Overline, Dots, Tildes, Accents, and many more
- 🌟 **Beautiful Emojis** – each reply comes with unique symbols
- 🔮 **Random Styles** – new style every time
- 🎨 **First Response** – shows all styles at once
- 🖼️ Echoes **photos with captions**
- 📄 Echoes **documents**
- 😊 Echoes **stickers**
- 🎤 Echoes **voice messages**
- 🎥 Echoes **videos**
- 📝 **Logs all actions** in console

---

## 🚀 Installation

### 1. Install Python
Make sure you have **Python 3.7+** installed.

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a bot in Telegram
1. Open [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Enter a bot name
4. Choose a username (must end with `bot`)
5. Copy the generated token

### 4. Configure bot token
Edit `config.py` and insert your token:
```python
BOT_TOKEN = "your_token_here"
```

### 5. Run the bot
```bash
python echo_bot.py
```

---

## 💬 Usage

1. Find your bot in Telegram by its username
2. Send `/start`
3. Send any message – bot will reply in a random style

---

## 🎨 Examples

### First response (shows all styles):
```
🎨 ALL FONT STYLES 🎨

✨ Bold: 𝐇𝐞𝐥𝐥𝐨
🌟 Italic: 𝑯𝒆𝒍𝒍𝒐
💫 Script: 𝒮𝑒𝓃𝒹
⭐ Circled: ⒽⒺⓁⓁⓞ
🔮 Fraktur: 𝔥𝔢𝔩𝔩𝔬
💎 Double: 𝕙𝕖𝕝𝕝𝕠
🔥 Smallcaps: ʜᴇʟʟᴏ
⚡ Tiny: ʰᵉˡˡᵒ
🌀 Upside Down: ollǝH
❌ Strikethrough: H̶e̶l̶l̶o̶
📝 Underline: H̲e̲l̲l̲o̲
... and many more!

🔮 Each reply = random style! 🔮
```

### Next replies (random style each time):
```
✨ 𝐇𝐞𝐥𝐥𝐨 (Bold)
🌟 𝑯𝒆𝒍𝒍𝒐 (Italic)
💫 𝒮𝑒𝓃𝒹 (Script)
⭐ ⒽⒺⓁⓁⓞ (Circled)
🔮 𝔥𝔢𝔩𝔩𝔬 (Fraktur)
💎 𝕙𝕖𝕝𝕝𝕠 (Double)
🔥 ʜᴇʟʟᴏ (Smallcaps)
⚡ ʰᵉˡˡᵒ (Tiny)
🌀 ollǝH (Upside Down)
```

---

## 📁 Project Structure

```
telegram-echo-bot/
├── echo_bot.py          # Main bot script
├── config.py            # Bot configuration (token)
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

---

## 📊 Logging

The bot logs all actions, including:
- User info
- Message text
- File types

---

## ⏹️ Stopping the bot

Press `Ctrl + C` in terminal to stop.

---

## 🆘 Support

If you encounter issues:
- Verify your bot token
- Ensure Python 3.7+ is installed
- Check your internet connection
- Review console logs

---

## 📄 License

This project is created for educational purposes. Use at your own discretion.

---

## 🚀 Future plans

- [ ] Add inline buttons for style selection
- [ ] User-configurable preferred font
- [ ] Save user history of styles
- [ ] Add more font styles
- [ ] Web interface for bot management

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=username/telegram-echo-bot&type=Date)](https://star-history.com/#username/telegram-echo-bot&Date)

---

<div align="center">

**Made with ❤️ for the Telegram community**

[⬆ Back to top](#telegram-echo-bot-with-fancy-fonts-)

</div>