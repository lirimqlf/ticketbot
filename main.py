import discord
import os
from discord import app_commands
from discord.ui import Select, View, Button
import asyncio
from typing import Optional
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Create a Flask web server
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord bot is running!"

def run_web_server():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Load environment variables
load_dotenv()

# Configuration - using environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Will be set in Render environment variables
GUILD_ID = int(os.getenv("GUILD_ID", "1342232027851784243"))
TICKET_CATEGORY_ID = int(os.getenv("TICKET_CATEGORY_ID", "1364300307823198268"))
STAFF_ROLE_ID = int(os.getenv("STAFF_ROLE_ID", "1364300522349265026"))

# QLF Stock services
QLF_SERVICES = {
    "SynthX": {"name": "SynthX - Tha Bronx 3", "emoji": "<:qlf:1364046376249462825>"},
    "Boosts Reward": {"name": "Boosts - Reward", "emoji": "<:qlf:1364046376249462825>"},
}

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)
        self.synced = False
        self.tickets = {}  # Store ticket information in memory
            
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=GUILD_ID))
            self.synced = True
        print(f"Logged in as {self.user}")
        
        # Set bot presence
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="for tickets"
        ))

client = Client()
tree = app_commands.CommandTree(client)

# Create the service selection menu
class ServiceSelectMenu(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=service["name"],
                value=service_id,
                emoji=service["emoji"]
            ) for service_id, service in QLF_SERVICES.items()
        ]
        super().__init__(
            placeholder="Select Which Service You Want To Buy",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="service_select"
        )
        
    async def callback(self, interaction: discord.Interaction):
        # Get the selected service
        service_id = self.values[0]
        service = QLF_SERVICES[service_id]
        
        # Create a ticket channel
        guild = interaction.guild
        member = interaction.user
        
        # Create ticket name
        ticket_name = f"ticket-{member.name}-{service_id.lower()}"
        
        # Check if ticket category exists
        category = guild.get_channel(TICKET_CATEGORY_ID)
        if not category:
            await interaction.response.send_message("Ticket category not found! Please contact an administrator.", ephemeral=True)
            return
            
        # Create permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.get_role(STAFF_ROLE_ID): discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # Create the ticket channel
        ticket_channel = await guild.create_text_channel(
            name=ticket_name,
            category=category,
            overwrites=overwrites,
            topic=f"Ticket for {member.name} - Service: {service['name']}"
        )
        
        # Save ticket information in memory
        client.tickets[str(ticket_channel.id)] = {
            "user_id": member.id,
            "service": service_id,
            "status": "open",
            "claimed_by": None
        }
            
        # Send confirmation message
        await interaction.response.send_message(f"Ticket created! Check {ticket_channel.mention}", ephemeral=True)
        
        # Create ticket controls
        class TicketControlButtons(View):
            def __init__(self):
                super().__init__(timeout=None)
                
            @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.secondary, custom_id="claim_ticket")
            async def claim_button(self, button_interaction: discord.Interaction, button: Button):
                staff_member = button_interaction.user
                
                # Update ticket claim status in memory
                client.tickets[str(ticket_channel.id)]["claimed_by"] = staff_member.id
                
                # Notify the ticket creator
                try:
                    ticket_creator = guild.get_member(member.id)
                    if ticket_creator:
                        try:
                            await ticket_creator.send(f"Your ticket for {service['name']} has been claimed by {staff_member.name}. They are ready to provide the service.")
                        except discord.Forbidden:
                            await ticket_channel.send(f"{member.mention}, your ticket has been claimed by {staff_member.mention}. They are ready to provide the service.")
                except Exception as e:
                    await ticket_channel.send(f"Could not notify the ticket creator: {e}")
                
                # Update ticket message
                await ticket_channel.send(f"Ticket claimed by {staff_member.mention}. They are ready to provide the service.")
                await button_interaction.response.defer()
                
            @discord.ui.button(label="Delete Ticket", style=discord.ButtonStyle.secondary, custom_id="delete_ticket")
            async def delete_button(self, button_interaction: discord.Interaction, button: Button):
                if button_interaction.user.guild_permissions.manage_channels or button_interaction.user.get_role(STAFF_ROLE_ID) is not None:
                    await button_interaction.response.send_message("Deleting this ticket in 5 seconds...", ephemeral=True)
                    
                    # Update status in memory
                    if str(ticket_channel.id) in client.tickets:
                        client.tickets[str(ticket_channel.id)]["status"] = "deleted"
                    
                    await asyncio.sleep(5)
                    await ticket_channel.delete()
                else:
                    await button_interaction.response.send_message("You don't have permission to delete this ticket.", ephemeral=True)
        
        # Send initial message in the ticket channel
        embed = discord.Embed(
            title=f"Ticket opened, Wait for any admin to claim the ticket.",
            description=f"Service: {service['name']}\nUser: {member.mention}",
            color = discord.Color(0xffffff)
        )
        
        # Create and send the view with ticket control buttons
        ticket_controls = TicketControlButtons()
        await ticket_channel.send(embed=embed, view=ticket_controls)

# Create the ticket creation system command
@tree.command(name="setup_tickets", description="Set up the ticket system", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def setup_tickets(interaction: discord.Interaction):
    # Create the embed for the ticket system
    embed = discord.Embed(
        title="Buy QLF Stock",
        description="Buy QLF Stock - Scripts.\nClick the button and choose which Script your ticket concerns.",
        color = discord.Color(0x000000)
    )
    embed.set_footer(text="Powered by QLF Stock")
    embed.set_thumbnail(url="https://i.ibb.co/k2FYRBCM/New-Project-2025-04-22-T022705-720.jpg") 
    
    # Create the view with the service selection menu
    view = View(timeout=None)
    view.add_item(ServiceSelectMenu())
    
    await interaction.response.send_message("Setting up ticket system...", ephemeral=True)
    await interaction.channel.send(embed=embed, view=view)

# Add a command to create a new ticket
@tree.command(name="ticket", description="Create a new support ticket", guild=discord.Object(id=GUILD_ID))
async def create_ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Assistance",
        description="Support - Guildes.\nClique sur le bouton et choisis quelle guilde ton ticket concerne-t-il",
        color = discord.Color(0xffffff)
    )
    embed.set_footer(text="Powered by ticketsbot.cloud")
    
    # Create the view with the service selection menu
    view = View(timeout=None)
    view.add_item(ServiceSelectMenu())
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Add a permissions check command
@tree.command(name="check_permissions", description="Check bot permissions", guild=discord.Object(id=GUILD_ID))
async def check_permissions(interaction: discord.Interaction):
    guild = interaction.guild
    bot_member = guild.get_member(client.user.id)
    
    permissions = []
    for perm, value in bot_member.guild_permissions:
        if value:
            permissions.append(perm)
    
    await interaction.response.send_message(f"Bot permissions: {', '.join(permissions)}", ephemeral=True)

# Error handler for app_commands
@tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
        raise error

# Run the bot
if __name__ == "__main__":
    # Start web server in a separate thread
    print("Starting web server...")
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True  # This ensures the thread will close when the main program exits
    server_thread.start()
    
    # Run the Discord bot
    print("Starting Discord bot...")
    client.run(BOT_TOKEN)
