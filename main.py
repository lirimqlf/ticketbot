import discord
from discord.ext import commands
import datetime
import os
import http.server
import socketserver
from threading import Thread
from dotenv import load_dotenv

# Create a simple HTTP server to keep the bot alive on Render
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'SynthX Payment Bot is running!')

def run_web_server():
    port = int(os.environ.get('PORT', 8080))
    handler = SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Web server running at port {port}")
        httpd.serve_forever()

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")  # This will be set in Render environment variables
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Editable Payment Information
SYNTHX_PRICE = 13.50  # Base price in USD

# Crypto payment information
CRYPTO_WALLETS = {
    "Bitcoin": "bc1q6qgw5plrp9u5fjr8a2d6kw6gymr53p3d73je0z",
    "Ethereum": "0xE4D77C1736c274b413eF126E94CAE86181934C11",
    "Litecoin": "LNrgkx1bxZWmr1hyzX3av8YeQ5kAdcTT1U"
}
CRYPTO_PRICES = {
    "Bitcoin": 0.00011,
    "Ethereum": 0.00055,
    "Litecoin": 0.012, 
}

# Robux payment information
ROBUX_GAMEPASSES = {
    "SynthX Access Pass": "https://www.roblox.com/catalog/133810048920301/Synth-X-HALF",
    "SynthX Premium Pass": "https://www.roblox.com/game-pass/960611644/SynthX-HALF"
}
ROBUX_PRICE = 1200  # Total Robux needed

# PayPal information
PAYPAL_LINK = "paypal.me/wrld2real"

# Gift Card information
GIFT_CARDS = {
    "Amazon": 10,
    "Steam": 10,
    "Xbox": 10,
    "Roblox": 10,
}

# Paysafecard information
PCS_LINK = "https://www.paysafecard.com"
PCS_PRICE = 15

# Bot event handlers
@bot.event
async def on_ready():
    print(f'{bot.user.name} is now online!')
    # Set bot presence
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, 
        name="for payment commands"
    ))

# Helper function to create a standard embed template
def create_embed(title, description):
    embed = discord.Embed(
        title=title,
        description=description,
        color=0xffffff,
        timestamp=datetime.datetime.now()
    )
    embed.set_footer(text="SynthX Payment System")
    return embed

# Command handlers
@bot.command()
async def crypto(ctx):
    embed = create_embed(
        "<:Bitcoin:1364313502277177414>SynthX - Crypto Payment",
        "To purchase SynthX using cryptocurrency, please send the exact amount to one of the following wallets:"
    )
    
    for crypto_name, wallet in CRYPTO_WALLETS.items():
        embed.add_field(
            name=f"{crypto_name} Payment",
            value=f"**Wallet:** `{wallet}`\n**Amount:** `{CRYPTO_PRICES[crypto_name]} {crypto_name}`",
            inline=False
        )
    
    embed.add_field(
        name="Important Note",
        value="Please make sure to send the exact amount listed. After sending, message an admin with your transaction ID for verification.",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def robux(ctx):
    embed = create_embed(
        "<:Robux:1364314076368605277> SynthX - Robux Payment",
        f"To purchase SynthX using Robux, please purchase the following game passes (total: {ROBUX_PRICE} Robux):"
    )
    
    for pass_name, pass_link in ROBUX_GAMEPASSES.items():
        embed.add_field(
            name=pass_name,
            value=f"[Click here to purchase]({pass_link})",
            inline=False
        )
    
    embed.add_field(
        name="After Purchase",
        value="Once you've purchased the game passes, please message an admin with your Roblox username and proof of payment for verification.",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def paypal(ctx):
    embed = create_embed(
        "<:Paypal:1364314384079257654> SynthX - PayPal Payment",
        f"To purchase SynthX using PayPal, please follow these instructions:"
    )
    
    embed.add_field(
        name="PayPal Link",
        value=f"[{PAYPAL_LINK}]({PAYPAL_LINK})",
        inline=False
    )
    
    embed.add_field(
        name="Amount",
        value=f"${SYNTHX_PRICE:.2f} USD",
        inline=False
    )
    
    embed.add_field(
        name="<:Attention:1364597274180714507> IMPORTANT <:Attention:1364597274180714507>",
        value="**You MUST send payment as 'Friends & Family'**\nFailure to do so may result in delayed or denied access to SynthX.",
        inline=False
    )
    
    embed.add_field(
        name="After Payment",
        value="Once payment is sent, please message an admin with your PayPal email/transaction ID for verification.",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def giftcard(ctx):
    embed = create_embed(
        "<:GiftCard:1364441655083667456> SynthX - Gift Card Payment",
        f"To purchase SynthX using gift cards, you can use any of the following options:"
    )
    
    for card_name, card_value in GIFT_CARDS.items():
        embed.add_field(
            name=f"{card_name} Gift Card",
            value=f"Required value: ${card_value:.2f} USD",
            inline=True
        )
    
    embed.add_field(
        name="Redemption Process",
        value="1. Purchase the gift card of your choice\n2. Message an admin with the gift card code\n3. Once verified, you'll receive SynthX access",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def pcs(ctx):
    embed = create_embed(
        "<:PaySafe:1364314798342410401> SynthX - Paysafecard Payment",
        f"To purchase SynthX using Paysafecard, please follow these instructions:"
    )
    
    embed.add_field(
        name="Paysafecard Official Website",
        value=f"{PCS_LINK}",
        inline=False
    )
    
    embed.add_field(
        name="Required Amount",
        value=f"€{PCS_PRICE:.2f} EUR",
        inline=False
    )
    
    embed.add_field(
        name="How to Pay",
        value="1. Purchase a Paysafecard voucher from an authorized retailer\n2. Message an admin with the Paysafecard code\n3. Once verified, you'll receive SynthX access",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def list(ctx):
    embed = create_embed(
        "SynthX - Payment Methods",
        "Available payment methods for purchasing SynthX:"
    )
    
    # Add Crypto payment methods
    crypto_text = ""
    for crypto_name, price in CRYPTO_PRICES.items():
        crypto_text += f"**{crypto_name}:** `{price} {crypto_name}`\n"
    embed.add_field(name="<:Bitcoin:1364313502277177414> Cryptocurrency", value=crypto_text, inline=False)
    
    # Add Robux payment method
    embed.add_field(
        name="<:Robux:1364314076368605277> Robux",
        value=f"**Required amount:** `{ROBUX_PRICE} Robux`",
        inline=False
    )
    
    # Add PayPal payment method
    embed.add_field(
        name="<:Paypal:1364314384079257654> PayPal",
        value=f"**Price:** `${SYNTHX_PRICE:.2f} USD`\n**Link:** {PAYPAL_LINK}",
        inline=False
    )
    
    # Add Gift Card payment methods
    gift_text = ""
    for card_name, value in GIFT_CARDS.items():
        gift_text += f"**{card_name}:** `${value:.2f} USD`\n"
    embed.add_field(name="<:GiftCard:1364441655083667456> Gift Cards", value=gift_text, inline=False)
    
    # Add Paysafecard payment method
    embed.add_field(
        name="<:PaySafe:1364314798342410401> Paysafecard",
        value=f"**Price:** `€{PCS_PRICE:.2f} EUR`",
        inline=False
    )
    
    # Add call-to-action
    embed.add_field(
        name="<:Dollar:1364440332468752415> More Information",
        value="Use the following commands for detailed payment instructions:\n`!crypto`, `!robux`, `!paypal`, `!giftcard`, `!pcs`",
        inline=False
    )
    
    await ctx.send(embed=embed)

# Adding a help command to list all available commands
@bot.command()
async def help(ctx):
    embed = create_embed(
        "SynthX Payment Bot - Help",
        "Here are all the available commands for the SynthX Payment System:"
    )
    
    embed.add_field(
        name="!list",
        value="Shows all available payment methods at a glance",
        inline=False
    )
    
    embed.add_field(
        name="!crypto",
        value="Detailed instructions for cryptocurrency payments",
        inline=False
    )
    
    embed.add_field(
        name="!robux",
        value="Detailed instructions for Robux payments",
        inline=False
    )
    
    embed.add_field(
        name="!paypal",
        value="Detailed instructions for PayPal payments",
        inline=False
    )
    
    embed.add_field(
        name="!giftcard",
        value="Detailed instructions for gift card payments",
        inline=False
    )
    
    embed.add_field(
        name="!pcs",
        value="Detailed instructions for Paysafecard payments",
        inline=False
    )
    
    await ctx.send(embed=embed)

# Run the bot and web server
if __name__ == "__main__":
    # Start web server in a separate thread
    print("Starting web server...")
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True  # This ensures the thread will close when the main program exits
    server_thread.start()
    
    # Run the Discord bot
    print("Starting Discord bot...")
    bot.run(BOT_TOKEN)
