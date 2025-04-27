# 🎟️ QLF Stock Ticket Bot

A powerful and clean Discord bot for **QLF Stock** to manage support tickets, service purchases, and staff claims — fully powered with **slash commands** and **dropdown menus**.  
Built with ❤️ using `discord.py` and deployed with a lightweight web server.

---

## 🚀 Features

- 🎫 **Create Tickets** with dropdown service selection
- 🛒 **Select Services** (e.g., SynthX, Boosts Reward) easily
- 🛡️ **Staff Claim System** with notifications
- ❌ **Ticket Deletion** by staff
- 🖥️ **Simple Web Server** to keep bot alive on hosting platforms (Render, etc.)
- ⚡ **Slash Commands** for easy setup and ticket creation
- 🔐 **Permission Management** for secure ticket channels

---

## 📜 Commands

| Command | Description |
|:-------|:------------|
| `/setup_tickets` | Set up the ticket system with service selection |
| `/ticket` | Create a new support ticket manually |
| `/check_permissions` | Check bot permissions in the server |

---

## 🛠️ Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/qlf-ticket-bot.git
cd qlf-ticket-bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file and configure your environment variables:

```env
BOT_TOKEN=your_discord_bot_token
GUILD_ID=your_discord_server_id
TICKET_CATEGORY_ID=your_ticket_category_channel_id
STAFF_ROLE_ID=your_staff_role_id
PORT=8080
```

4. Run the bot:

```bash
python bot.py
```

---

## ⚙️ Environment Variables

| Variable | Description |
|:---------|:------------|
| `BOT_TOKEN` | Your Discord bot token |
| `GUILD_ID` | ID of your Discord server |
| `TICKET_CATEGORY_ID` | ID of the category where tickets will be created |
| `STAFF_ROLE_ID` | Role ID that can claim/delete tickets |
| `PORT` | Port for the web server (default: `8080`) |

---

## 📦 Libraries Used

- [`discord.py`](https://github.com/Rapptz/discord.py)
- [`python-dotenv`](https://pypi.org/project/python-dotenv/)
- Built-in modules: `http.server`, `socketserver`, `threading`, `asyncio`, `os`

---

## 🖼️ Preview

> When users click the "Buy QLF Stock" button, they are prompted to select a service and a private ticket channel is automatically created for them and the staff.

![Bot Preview](https://i.ibb.co/k2FYRBCM/New-Project-2025-04-22-T022705-720.jpg)

---

## 🧠 Notes

- Designed for hosting on **Render** or any other platform that needs a web server "keep-alive" trick.
- Tickets are stored **in-memory** — meaning if the bot restarts, the memory resets (consider persistent storage if needed).
- All permissions and security best practices are enforced to keep ticket management professional.

---

## 🔥 Hosting Friendly

- Includes a keep-alive web server
- Ready for Render, Replit, Railway, Heroku
- Designed to be lightweight and efficient

---

## 🤝 Contribution

Contributions, suggestions, and PRs are **highly welcome**!  
Let's build better tools together. 🚀

---

## 📜 License

[MIT License](https://discord.gg/vHyQTBZJDd)

---

# ⚡ Powered by QLF Stock

---
