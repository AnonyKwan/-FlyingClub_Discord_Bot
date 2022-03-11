import os
import requests
import json
import random
import discord
from discord import Color
from discord.ui import Button, View

discord_token = ''
print (discord_token)
api_key_list = ["4JIJWVNR8HJDJF44C37MF5UJAA3NFMZ5R2","FN7RPKGTW7UHXSA6FATIWXQD4M53R9MDF7","5BZDS26XVNHWU4SFJC7E99V7MENRSRSBCJ",'VKXWNXZ134PUJZ9874UU7W72CMYXTE7XG1']
ramdon_api_key = random.choice(api_key_list)

bot = discord.Bot()

def polygonscan_status (wallet_address):
    
    response = requests.get(f"https://api.polygonscan.com/api?module=account&action=tokentx&contractaddress=0x3Fb89b4385779a8513d73Aed99AC6E4b77C34821&address={wallet_address}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={ramdon_api_key}").text
    if int(json.loads(response)["status"]) == 0:
        return False
    else:
        redeem_info = json.loads(response)
        token_spent = 0
        token_remain = 0
        total_income = 0
        for transation in redeem_info['result']:
            if  transation['to'].upper() in wallet_address.upper():
                total_income += int(transation['value'][:-18])
                continue
            else:
                # GET ALL TRANSATIONS
                token_spent += int(transation['value'][:-18])
        token_remain = total_income - token_spent
        return token_remain,total_income

@bot.event
async def on_ready():
    print (f"{bot.user} is connected!")

@bot.slash_command(guild_ids=[925970052174462976,358968997762433024,945103376679596082],description = "Gas Air Supply")
async def gas(ctx,wallet_address):
    
    if polygonscan_status (wallet_address) == False:
        gas_deny_embed = discord.Embed(title="錢包地址錯誤，請重新輸入 | Polygonscan ",description=wallet_address ,colour=Color.red())
        gas_deny_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=gas_deny_embed, delete_after=60)
    else:
        token_remain,total_income = polygonscan_status (wallet_address)
        if total_income > 0:
            nz_holder = "✅"
        else:
            nz_holder = "❌"       
        gas_request_embed = discord.Embed(title=f"請求空中支援 - 錢包地址",description=wallet_address ,colour=Color.red())
        gas_request_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        gas_request_embed.set_thumbnail(url="https://flyingclub.io/assets/paperplane-3245df87512ef7c15e7b91cc0cdeae37109489f2c839fd48cb3674606e5fe0b3.png")
        gas_request_embed.add_field(name="錢包餘額", value=f"{token_remain} NZ", inline=True)
        gas_request_embed.add_field(name="持有NZ", value=nz_holder, inline=True)
        gas_request_embed.add_field(name="援助狀態", value="等待支援中！", inline=True)
        gas_request_embed.set_footer(text="空中支援命令 /gas <錢包地址>")
        accept_button = Button(label="提供援助",style=discord.ButtonStyle.green,emoji="😁")
        
        async def accept_button_callback (interaction):
            
            gas_supply_embed = discord.Embed(title="空中支援處理中 - 錢包地址",description=wallet_address ,colour=Color.yellow())
            gas_supply_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            gas_supply_embed.set_thumbnail(url="https://flyingclub.io/assets/paperplane-3245df87512ef7c15e7b91cc0cdeae37109489f2c839fd48cb3674606e5fe0b3.png")
            gas_supply_embed.add_field(name="錢包餘額", value=f"{token_remain} NZ", inline=True)
            gas_supply_embed.add_field(name="持有NZ", value=nz_holder, inline=True)
            gas_supply_embed.add_field(name="援助狀態", value=interaction.user, inline=True)
            gas_supply_embed.set_footer(text="空中支援命令 /gas <錢包地址>")
            comfirm_button = Button(label="已提供援助",style=discord.ButtonStyle.green,emoji="😁")
            reject_button = Button(label="退出援助",style=discord.ButtonStyle.green,emoji="😥")
            copy_button = Button(label="錢包地址",style=discord.ButtonStyle.green,custom_id=wallet_address,emoji="©️")
            accept_user = interaction.user
            view.remove_item(accept_button)
            view.add_item(comfirm_button)
            view.add_item(reject_button)
            view.add_item(copy_button)
            await ctx.edit(embed=gas_supply_embed,view=view)

            async def copy_button_callback (interaction):
                await ctx.send(wallet_address,delete_after=10)
            
            async def confirm_button_callback (interaction):
                comfirm_user = interaction.user
                if accept_user == comfirm_user:
                    gas_comfim_embed = discord.Embed(title="已完成援助" ,colour=Color.green())
                    gas_comfim_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
                    gas_comfim_embed.set_thumbnail(url="https://flyingclub.io/assets/paperplane-3245df87512ef7c15e7b91cc0cdeae37109489f2c839fd48cb3674606e5fe0b3.png")
                    gas_comfim_embed.add_field(name="援助對象", value=ctx.author, inline=True)
                    gas_comfim_embed.add_field(name="空頭大師", value=interaction.user, inline=True)
                    gas_comfim_embed.set_footer(text="空中支援命令 /gas <錢包地址>")
                    view.remove_item(comfirm_button)
                    view.remove_item(reject_button)
                    view.remove_item(copy_button)
                    await ctx.edit(embed=gas_comfim_embed,view=view)

            async def reject_button_callback (interaction):
                reject_user = interaction.user
                if accept_user == reject_user:
                  view.add_item(accept_button)
                  view.remove_item(comfirm_button)
                  view.remove_item(reject_button)
                  view.remove_item(copy_button)
                  await ctx.edit(embed=gas_request_embed,view=view)

            comfirm_button.callback = confirm_button_callback
            reject_button.callback = reject_button_callback
            copy_button.callback = copy_button_callback

        accept_button.callback = accept_button_callback
        view = View()
        view.add_item(accept_button)
        await ctx.respond ("<@&928430972070932513>",embed=gas_request_embed,view=view)

bot.run(discord_token)
