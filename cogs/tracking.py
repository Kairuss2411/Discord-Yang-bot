
import discord
import json
import os
import datetime
from discord.ext import commands
from operator import itemgetter

class tracking(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  
    self.GUILD_ID = int(os.getenv('GUILD_ID'))
    self.CHANNEL_LOG_ID = int(os.getenv('CHANNEL_LOG_ID'))
  @commands.command(brief='Thời gian học của bạn', aliases = ['me'] )
  async def studytime(self, ctx):
    with open ('/home/runner/Yang-Bot/users.json','r') as f:
      file = json.load(f)
      users_list = file['users_list']
      f.close()
      #Get request member
      member = ctx.message.author
      for user in users_list:
        if member.id == user["id"]:
          embed=discord.Embed(title="Thời gian học")
          if user['learning_time'] < 1:
            #Minutes
            studytime = round( round(user['learning_time'],2) * 60,1)
            str_studytime = str(studytime) + " phút"
            embed.add_field(name="Tổng thời gian ", value=f'{str_studytime}', inline=True)
          else:
            studytime = user['learning_time']
            #Time in Hours
            hours = str(int(studytime)) +" giờ "
            #Time in Minute
            round_time = round(studytime,2)
            print(round_time)
            mins = round(round_time % int(studytime),2)
            print(mins)
            minutes = str(int(round(mins*60,0)))  +" phút"
            #Message
            embed.add_field(name="Tổng thời gian ", value=f'{hours + minutes}', inline=False)

          #get top
          top_tuple = sorted(users_list, key = itemgetter('learning_time'), reverse=True)
            #Get index of requested user.
          for user in top_tuple:
            if user['id'] == member.id:
              index = top_tuple.index(user)
          #dont touch
          embed.add_field(name="Xếp Hạng Tổng ", value=f"\t #{index+1}", inline=False)
          embed.set_footer(text=f'Người dùng {member.name}',icon_url=member.avatar_url)
          await ctx.send(embed=embed)
          break

  @commands.command(brief='Bảng xếp hạng', aliases = ['t','lb'])
  async def top(self, ctx):
    with open('/home/runner/Yang-Bot/users.json','r') as f:
      file = json.load(f)
      users = file['users_list']
      f.close()
      #Sort Users by top learning time
      top_tuple = sorted(users, key = itemgetter('learning_time'), reverse=True)
      #Get index of requested user.
      list_result = []
      user_id = ctx.message.author.id
      index = -1
      for user in top_tuple:
        if user['id'] == user_id:
          index = top_tuple.index(user)
          list_result.append(user)
          break
      #Get 10 user around request user in leaderboard
      #get above user in top
      i = index
      count = 0
      limit = 4
      # Num ofuser left
      if index == (len(users)-1):
        limit = 10
      while (i!=0) and (count!=limit):
        i -= 1 
        count += 1
        list_result.append(top_tuple[i])
      user_left = 10 - count
      i = index 
      while( i != (len(users)-1) ) and (i != user_left):
        i+=1
        list_result.append(top_tuple[i])
      #Resorted result list
      list_result = sorted(list_result, key = itemgetter('learning_time'), reverse=True)
      grades = []
      for user in list_result:
        if user['id'] == user_id:
          grades.append(f"**{round(user['learning_time'],2)}h - {str(top_tuple.index(user)+1)}. {self.bot.get_user(user['id']).name} **")
        else:
          grades.append(f"{str(top_tuple.index(user)+1)}. {self.bot.get_user(user['id']).name} ({round(user['learning_time'],2)}h)")
      text = "\n ".join(grades)
      embed = discord.Embed(title = "RANK TIME",description = f"Bảng xếp hạng thành viên chăm chỉ", color=0x002aff, timestamp = datetime.datetime.utcnow() )
      embed.add_field(name="\u200b", value=f"{text}", inline=True)
      await ctx.send(embed=embed)
  
def setup(bot):
  bot.add_cog(tracking(bot))