import discord
import os
from discord import app_commands
from src import responses
from src import log

logger = log.setup_logger(__name__)

isPrivate = False
isReplyAll = True
discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")


class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(
            type=discord.ActivityType.playing, name="gay")


async def send_message(message, user_message):
    global isReplyAll
    if not isReplyAll:
        author = message.user.id
        await message.response.defer(ephemeral=isPrivate)
    else:
        author = message.author.id
    try:
        # response = '> **' + user_message + '** - <@' + \
        #     str(author) + '>'
        # response = f"{response}{await responses.response(user_message)}"
        response = f"{await responses.response(user_message)}"
        if len(response) > 1900:
            # Split the response into smaller chunks of no more than 1900 characters each(Discord limit is 2000 per chunk)
            if "```" in response:
                # Split the response if the code block exists
                parts = response.split("```")
                # Send the first message
                if isReplyAll:
                    await message.channel.send(parts[0])
                else:
                    await message.followup.send(parts[0])
                # Send the code block in a seperate message
                code_block = parts[1].split("\n")
                formatted_code_block = ""
                for line in code_block:
                    while len(line) > 1900:
                        # Split the line at the 50th character
                        formatted_code_block += line[:1900] + "\n"
                        line = line[1900:]
                    formatted_code_block += line + "\n"  # Add the line and seperate with new line

                # Send the code block in a separate message
                if (len(formatted_code_block) > 2000):
                    code_block_chunks = [formatted_code_block[i:i+1900]
                                         for i in range(0, len(formatted_code_block), 1900)]
                    for chunk in code_block_chunks:
                        if isReplyAll:
                            await message.channel.send("```" + chunk + "```")
                        else:
                            await message.followup.send("```" + chunk + "```")
                else:
                    if isReplyAll:
                        await message.channel.send("```" + formatted_code_block + "```")
                    else:
                        await message.followup.send("```" + formatted_code_block + "```")
                # Send the remaining of the response in another message

                if len(parts) >= 3:
                    if isReplyAll:
                        await message.channel.send(parts[2])
                    else:
                        await message.followup.send(parts[2])
            else:
                response_chunks = [response[i:i+1900]
                                   for i in range(0, len(response), 1900)]
                for chunk in response_chunks:
                    if isReplyAll:
                        await message.channel.send(chunk)
                    else:
                        await message.followup.send(chunk)

        else:
            if isReplyAll:
                await message.channel.send(response)
            else:
                await message.followup.send(response)
    except Exception as e:
        if isReplyAll:
            await message.channel.send("> **Error: Something went wrong, please try again later!**")
        else:
            await message.followup.send("> **Error: Something went wrong, please try again later!**")
        logger.exception(f"Error while sending message: {e}")


async def send_start_prompt(client):
    import os.path

    config_dir = os.path.abspath(__file__ + "/../../")
    prompt_name = 'starting-prompt.txt'
    prompt_path = os.path.join(config_dir, prompt_name)
    try:
        if os.path.isfile(prompt_path) and os.path.getsize(prompt_path) > 0:
            with open(prompt_path, "r") as f:
                prompt = f.read()
                if (discord_channel_id):
                    # logger.info(f"Send starting prompt with size {len(prompt)}")
                    # responseMessage = await responses.response(prompt)
                    responseMessage = 'Started!'
                    channel = client.get_channel(int(discord_channel_id))
                    await channel.send(responseMessage)
                else:
                    logger.info(
                        "No Channel selected. Skip sending starting prompt.")
        else:
            logger.info(f"No {prompt_name}. Skip sending starting prompt.")
    except Exception as e:
        logger.exception(f"Error while sending starting prompt: {e}")


def run_discord_bot():
    client = aclient()

    @client.event
    async def on_ready():
        # await send_start_prompt(client)
        await client.tree.sync()
        logger.info(f'{client.user} is now running!')

    @client.tree.command(name="moichatadd", description="Thêm phòng chat tự động")
    async def moichatadd(interaction: discord.Interaction):
        channel = str(interaction.channel.id)
        f = open("channels.txt", "a")
        f.write(channel + "\n")
        f.close()
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("> **Đã thêm phòng này để chat tự động, MoiChat sẽ trả lời mọi tin nhắn từ phòng này!**")
        logger.info(f"Thêm phòng mới {channel}!")

    @client.tree.command(name="moichatremove", description="Xóa phòng chat tự động")
    async def moichatremove(interaction: discord.Interaction):
        channel = str(interaction.channel.id)
        with open("channels.txt", "r") as f:
            lines = f.readlines()
        with open("channels.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != channel:
                    f.write(line)
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("> **Đã xóa phòng chat tự động.**")
        logger.info(f"Xóa phòng {channel}!")

    @client.tree.command(name="help", description="Hiển thị trợ giúp của bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(":star:**BASIC COMMANDS** \n\n    - `/moichatadd` Thêm phòng chat tự động!\n    - `/moichatremove` Xóa phòng chat tự động.")
        logger.info(
            "\x1b[31mSomeone need help!\x1b[0m")

    @client.event
    async def on_message(message):
        with open("channels.txt", "r") as f:
            channels = f.read().split('\n')
        if message.author.bot:
            return
        if not isinstance(message.channel, discord.channel.DMChannel):
            if not str(message.channel.id) in channels:
                return
        if message.author == client.user:
            return
        if isReplyAll:
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)
            logger.info(
                f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
            await send_message(message, user_message)

    TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    client.run(TOKEN)
