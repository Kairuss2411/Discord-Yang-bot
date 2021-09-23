import discord
import json
import os
import time
from discord.ext import commands

class leveling(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  
    self.GUILD_ID = int(os.getenv('GUILD_ID'))
    self.CHANNEL_LOG_ID = int(os.getenv('CHANNEL_LOG_ID'))
    self.user_file_path = '/home/runner/Yang-Bot/users.json'
  # Create all current member data  
  @commands.command(brief='Khởi tạo dữ liệu toàn bộ người dùng trong hệ thống.', aliases = ['cd'] )
  async def create(self, ctx):
    with open('/home/runner/Yang-Bot/users.json','r+') as f:
      file = json.load(f)
      users_list = file['users_list']
      print(users_list)
      # #Kiem tra member da co trong du lieu chua
      if not users_list:
        list_mem = [member for member in ctx.guild.members if not member.bot]
        for user in list_mem:
          user = {
            "id" : user.id,
            "learning_time" : 0,
            "join_time": 0
          }
          users_list.append(user)
        f.seek(0)
        json.dump(file, f, indent = 4)
        await ctx.send("Omedetou Oni-chan!\nYang đã giúp oni-chan tạo hết dữ liệu người dùng rồi đó, khen Yang điii! Hehe 😊")
      else:
        await ctx.send("Đã có dữ liệu người dùng rồi đó oni-chan! Không cần phải ghi mới đâu, Yang sẽ giúp Oni-chan cập nhật khi có thành viên mới nha.")
   
  def add_user(new_data, filename='/home/runner/Yang-Bot/users.json'):
    with open(filename,'r+') as file:
      # First we load existing data into a dict.
      file_data = json.load(file)
      # Join new_data with file_data inside emp_details
      file_data["users_list"].append(new_data)
      # Sets file's current position at offset.
      file.seek(0)
      # convert back to json.
      json.dump(file_data, file, indent = 4)

  #Khi nguwoi dung
  @commands.Cog.listener()
  async def on_member_join(self,member):
    print("Member join server")
    with open('/home/runner/Yang-Bot/users.json','r+') as f:
      file = json.load(f)
      users_list = file['users_list']
      # #Kiem tra member da co trong du lieu chua
      if not users_list:
        #run create commands. Run another command in command.
        pass
      else:
        flag = True
        for user in users_list:
          if member.id == user["id"]:
            flag = False
            break
          else:
            pass
        if flag:
          user = {
            "id" : member.id,
            "learning_time" : 0,
            "join_time": 0
          }
          leveling.add_user(user)

  @commands.Cog.listener()
  async def on_voice_state_update(self,member , before, after):
    print('State Change')
    channel = self.bot.get_guild(self.GUILD_ID).get_channel(self.CHANNEL_LOG_ID)
    print('Channel: '+str(channel))
    if not before.channel and after.channel:
      #Như này nè
      print('Join')
      try:
        with open('/home/runner/Yang-Bot/users.json','r') as f:
          file = json.load(f)
          users_list = file['users_list']
          f.close()
          for user in users_list:
            if member.id == user["id"]:
              user['join_time'] = time.time() #9:06:59 23/9/2021 906592392021
              str_join = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user['join_time']) )
              # Sets file's current position at offset.
              await channel.send(f'Thời gian tham gia vào lúc: {str_join}')
              break #Edited then exit
          with open('/home/runner/Yang-Bot/users.json','w') as f:
            f.seek(0)
            # convert back to json.
            json.dump(file,f,indent=4)
  
      except Exception as e:
        print(e)

    elif before.channel and not after.channel:
      print('Leave')
      #Như này nè
      try:
        with open('/home/runner/Yang-Bot/users.json','r') as f:
          file = json.load(f)
          users_list = file['users_list']
          f.close()
          for user in users_list:
            if member.id == user["id"]:
              #calculate section learn time:
              learn_time = (time.time() - user['join_time'])/3600
              user['join_time'] = 0
              #Update total learning time
              user['learning_time'] += learn_time
              #Test tính time vừa học
              str_learn = str(learn_time)
              await channel.send(f'Thời gian vừa tham gia học: {str_learn}')
              #tổng tim học
              await channel.send(f'Tổng thời gian học: {user["learning_time"]}')
              break #Done then exit
          with open('/home/runner/Yang-Bot/users.json','w') as f:
              #Save to json file
            f.seek(0)
            json.dump(file,f,indent=4)
            
      except Exception as e:
        print(e)
  
def setup(bot):
  bot.add_cog(leveling(bot))


  
  