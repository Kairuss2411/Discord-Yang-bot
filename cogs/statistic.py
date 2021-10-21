import discord
import json
import os
import datetime
from discord.ext import commands
from operator import itemgetter

class statistic(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  
    self.GUILD_ID = int(os.getenv('GUILD_ID'))
    self.guild = self.bot.get_guild(self.GUILD_ID)
    self.ADMIN_CHANNEL_ID = int(os.getenv('ADMIN_CHANNEL_ID'))

  @commands.command(brief='Xuất bảng xếp theo yêu cầu.', aliases = ['s','st'], description = "Hiển thị")
  async def stats(self, ctx, top_type:str="month"):
    if ctx.message.channel == self.bot.get_channel(self.ADMIN_CHANNEL_ID):
      with open('/home/runner/Yang-Bot/users.json','r') as f:
        file = json.load(f)
        users = file['users_list']
        f.close()
        top_tuple = []
        top_title = ""
        value = ''
        #Sort Users by top learning time
        if top_type == "month":
          top_tuple = sorted(users, key = itemgetter('month_learning'), reverse=True)
          now = datetime.datetime.now()
          top_title = f"TOP RANK - MONTH {now.month}\nCOUNT TO {now.strftime('%d/%m/%Y')}"
          value = 'month_learning'
        elif top_type == "week":
          top_tuple = sorted(users, key = itemgetter('week_learning'), reverse=True)
          top_title = "WEEK RANKING"
          value = 'week_learning'
        elif top_type == "day":
          top_tuple = sorted(users, key = itemgetter('day_learning'), reverse=True)
          top_title = "DAY RANKING"
          value = 'day_learning'
        elif top_type == "all":
          top_tuple = sorted(users, key = itemgetter('learning_time'), reverse=True)
          top_title = "TOP RANK - ALL"
          value = 'learning_time'
        #Get index of requested user.
        str_title = "".ljust(20)+top_title+"\n"+"TOP RANK".ljust(13)+"TIME".ljust(8)+"USER".ljust(25)+"USER ID"
        top_str = [str_title]
        for user in top_tuple:
          str_user = (("_"*80)+"\n"+
          "Top "+str(top_tuple.index(user)+1).ljust(10)+
          (str(round(user[value],2))+"h").ljust(7)+
          str(user['name']).ljust(30)+
          ("ID:"+str(user['id'])))
          top_str.append(str_user)
        # test1 = [str_title, top_str]
        with open('/home/runner/Yang-Bot/top_result.txt','w') as txt:
          for element in top_str:
            txt.write(element + "\n")
          txt.close()
        with open('/home/runner/Yang-Bot/top_result.txt', "rb") as file:
          await ctx.send("Đây là file thống kê của bạn nè nheee ", file=discord.File(file, 'top_result.txt'))

             
def setup(bot):
  bot.add_cog(statistic(bot))