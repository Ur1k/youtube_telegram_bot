YouTube → Telegram Auto‑Poster Bot

A lightweight, reliable Python bot that monitors a YouTube channel’s RSS feed and automatically posts new videos to a Telegram channel.

It includes:

\- Daily “bot is alive” heartbeat messages

\- Error notifications sent directly to the admin

\- Log rotation to prevent large log files

\- Environment‑variable‑based configuration (safe for GitHub)

\- Production‑grade reliability features

\- Clean, readable code



🚀 Features

✔ Automatic YouTube monitoring

The bot checks a YouTube RSS feed every 30 minutes and posts new videos to a Telegram channel.

✔ Telegram notifications

When a new video appears, the bot sends:

🔥 New YouTube video!

<video title>

<video link>

✔ Daily heartbeat

Once every 24 hours, the bot sends a message to the admin:

💡 Bot is alive and running normally.

✔ Error reporting

If anything goes wrong (network error, feed failure, unexpected exception), the bot sends a detailed error message to the admin chat.

✔ Log rotation

The bot writes logs to bot.log and automatically rotates them when they reach 5 MB.

✔ Safe configuration

All secrets (Telegram token, admin chat ID) are stored in .env or environment variables — never in the code.



📦 Project Structure

youtube\_telegram\_bot/

│

├── tel\_bot.py          # Main bot script

├── requirements.txt    # Python dependencies

├── .gitignore          # Prevents secrets/logs from being committed

└── README.md           # Project documentation





Your virtual environment (.venv/) stays outside this folder.



🔧 Installation

1\. Clone the repository

git clone https://github.com/YOUR\_USERNAME/youtube\_telegram\_bot.git

cd youtube\_telegram\_bot





2\. Create a virtual environment (optional but recommended)

python -m venv .venv

source .venv/bin/activate   # Linux/macOS

.\\.venv\\Scripts\\activate    # Windows





3\. Install dependencies

pip install -r requirements.txt







🔐 Environment Variables

Create a .env file in the project folder:

TELEGRAM\_TOKEN=your\_bot\_token\_here

ADMIN\_CHAT\_ID=your\_telegram\_user\_id





These values are loaded automatically using python-dotenv.



▶️ Running the Bot Locally

python tel\_bot.py





The bot will:

\- Check YouTube every 30 minutes

\- Send new video notifications

\- Send daily heartbeat

\- Log everything to bot.log



🖥️ Running on a Server (Oracle Cloud / Linux)

1\. Export environment variables

echo 'export TELEGRAM\_TOKEN="your\_token\_here"' >> ~/.bashrc

echo 'export ADMIN\_CHAT\_ID="your\_user\_id"' >> ~/.bashrc

source ~/.bashrc





2\. Create a systemd service

Example:

\[Unit]

Description=YouTube Telegram Bot

After=network.target



\[Service]

User=opc

WorkingDirectory=/home/opc/youtube\_telegram\_bot

ExecStart=/usr/bin/python3 /home/opc/youtube\_telegram\_bot/tel\_bot.py

Restart=always



\[Install]

WantedBy=multi-user.target





Enable and start:

sudo systemctl daemon-reload

sudo systemctl enable telbot.service

sudo systemctl start telbot.service







📝 Logging

Logs are stored in:

bot.log

bot.log.1

bot.log.2

...





The bot automatically rotates logs when they reach 5 MB.

To view logs:

tail -f bot.log





Or via systemd:

sudo journalctl -u telbot.service -f







🛠️ Customization

You can easily modify:

\- YouTube channel ID

\- Telegram channel ID

\- Check interval

\- Heartbeat interval

\- Log rotation size

\- Error handling

Everything is inside tel\_bot.py and clearly commented.



🤝  Contributing

Pull requests and suggestions are welcome.

This project is intentionally simple and easy to extend.



📄 License

This project is released under the MIT License.



