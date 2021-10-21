import json
import os
import time
from discord.ext import commands
from discord.utils import get
from operator import itemgetter


class leveling(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
      self.GUILD_ID = int(os.getenv('GUILD_ID'))
      self.ADMIN_CHANNEL_ID = int(os.getenv('ADMIN_CHANNEL_ID'))
      self.room_name = ["Study Yourself Room", "Study With", "Creative study", "Private study"]
  # Create all current member data
  @commands.command(
      brief='Khởi tạo dữ liệu toàn bộ người dùng trong hệ thống.',
      aliases=['cd'])
  async def create(self, ctx):
    if ctx.message.channel == self.bot.get_channel(self.ADMIN_CHANNEL_ID):
      with open('/home/runner/Yang-Bot/users.json', 'r+') as f:
          file = json.load(f)
          users = file['users_list']
          # #Kiem tra member da co trong du lieu chua
          if not users:
            list_mem = [
                member for member in ctx.guild.members if not member.bot
            ]
            for user in list_mem:
              user = {
                  "id": user.id,
                  "name": user.name,
                  "learning_time": 0,
                  "day_learning": 0,
                  "week_learning":0,
                  "month_learning": 0,
                  "current_level":-1,
                  #============
                  "join_time": 0
              }
              users.append(user)
            f.seek(0)
            json.dump(file, f, indent=4)
            f.close()
            await ctx.send(
                "Omedetou Oni-chan!\nYang đã giúp oni-chan tạo hết dữ liệu người dùng rồi đó, khen Yang điii! Hehe 😊"
            )
          else:
              await ctx.send(
                  "Đã có dữ liệu người dùng rồi đó oni-chan! Không cần phải ghi mới đâu, Yang sẽ giúp Oni-chan cập nhật khi có thành viên mới nha."
              )

  def add_user(new_user):
    print("Call add new user")
    try:
      with open('/home/runner/Yang-Bot/users.json', 'r') as f:
        file = json.load(f)
        users_list = file['users_list']
        f.close()
        users_list.append(new_user)
        print("added to list")
        with open('/home/runner/Yang-Bot/users.json','w') as f:
            f.seek(0)
            # convert back to json.
            json.dump(file, f, indent=4)
            f.seek(0)
    except Exception as e:
        print(e)
    
  def romove_user(leave_user):
    try:
      with open('/home/runner/Yang-Bot/users.json', 'r') as f:
        file = json.load(f)
        users_list = file['users_list']
        f.close()
        users_list.romove(leave_user)
        with open('/home/runner/Yang-Bot/users.json','w') as f:
            f.seek(0)
            # convert back to json.
            json.dump(file, f, indent=4)
            f.seek(0)
    except Exception as e:
        print(e)
  
  async def add_role(member):
    print("Add Role Callinnngggggggg")
    levels = []
    with open('/home/runner/Yang-Bot/level.json', 'r') as f:
      file = json.load(f)
      lvs = file['levels']
      f.close()
      levels = sorted(lvs, key = itemgetter('order'))
    with open('/home/runner/Yang-Bot/users.json', 'r') as f:
      file = json.load(f)
      users = file['users_list']
      f.close()
      for user in users:
        if member.id == user["id"]:
          learn_time = user['learning_time']
          for i in range(len(levels)):
            if learn_time >= levels[i]['mark'] and learn_time < levels[i]['end']:
              if i == 0:
                #add new role
                new_role = get(member.guild.roles, id=levels[i]['id'])
                await member.add_roles(new_role)
                user['current_level'] = levels[i]['order']
                break
              else:
                #remove current role
                cur_role = get(member.guild.roles, id=levels[i-1]['id'])
                await member.remove_roles(cur_role)
                #add new role
                new_role = get(member.guild.roles, id=levels[i]['id'])
                await member.add_roles(new_role)
                user['current_level'] = levels[i]['order']
                break
          with open('/home/runner/Yang-Bot/users.json','w') as f:
            #Save to json file
            f.seek(0)
            json.dump(file, f, indent=4)
            f.close()
          break
          
  def startLearning(member):
    print(f"{member.name} start learning section!")
    try:
      with open('/home/runner/Yang-Bot/users.json', 'r') as f:
        file = json.load(f)
        users_list = file['users_list']
        f.close()
        if member.id not in [ user['id'] for user in users_list]:
          print(member.name," not in database.")
          user = {
                "id": member.id,
                "name": member.name,
                "learning_time": 0,
                "day_learning": 0,
                "week_learning":0,
                "month_learning": 0,
                "current_level":-1,
                #============
                "join_time": 0
          }
          leveling.add_user(user)
        for user in users_list:
          if member.id == user["id"]:
            user['join_time'] = time.time()
            break
        with open('/home/runner/Yang-Bot/users.json','w') as f:
          f.seek(0)
          # convert back to json.
          json.dump(file, f, indent=4)
          f.seek(0)
    except Exception as e:
        print(e)
  def endLearning(member):
    print(f"{member.name} end learning section!")
    try:      
      with open('/home/runner/Yang-Bot/users.json', 'r') as f:
        file = json.load(f)
        users_list = file['users_list']
        f.close()
        for user in users_list:
          if member.id == user["id"]:
            if user['join_time'] == 0:
              return 
            #calculate section learn time:
            now = time.time()
            learn_time = (now -
                          user['join_time']) / 3600
            if learn_time < 0.0833333:
              learn_time = 0
            elif learn_time > 6:
              learn_time = 6
            #Update total learning time
            user['learning_time'] += learn_time
            user['day_learning'] += learn_time
            user['month_learning'] += learn_time
            user['week_learning'] += learn_time
            user['join_time'] = 0
        with open('/home/runner/Yang-Bot/users.json','w') as f:
          #Save to json file
          f.seek(0)
          json.dump(file, f, indent=4)
          f.close()
    except Exception as e:
        print(f"Error at: {e}")
  #Khi nguwoi dung
  @commands.Cog.listener()
  async def on_member_join(self, member):
    print(f"Member {member.name} ID: {member.id} join server")
    with open('/home/runner/Yang-Bot/users.json', 'r+') as f:
      file = json.load(f)
      users = file['users_list']
      f.close()
      # #Kiem tra member da co trong du lieu chua
      if not users:
        #run create commands. Run another command in command.
        pass
      else:
        flag = True
        for user in users:
          if member.id == user["id"]:
            flag = False
            break
        if flag:
          user = {
                "id": member.id,
                "name": member.name,
                "learning_time": 0,
                "day_learning": 0,
                "week_learning":0,
                "month_learning": 0,
                "current_level":-1,
                #============
                "join_time": 0
          }
          leveling.add_user(user)

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
  #==================================================
  #Test
  #Check if channel not in before but in after 
    if not before.channel and after.channel:
      #Check after channel is study room or not?
      if any(word in after.channel.name for word in self.room_name):
        #Check video
        if member.voice.self_video or member.voice.self_stream:
          print("Check videos 1")
          leveling.startLearning(member)
    elif before.channel and not after.channel:
      if any(word in before.channel.name for word in self.room_name):
        leveling.endLearning(member) 
        #Check and add new role  
        await leveling.add_role(member)
    #Trc sau deu o trong room voice.
    elif before.channel and after.channel:
      #Trc do Voice Study -> voice bth
      if any(word in before.channel.name for word in self.room_name) and not any(word in after.channel.name for word in self.room_name):
        leveling.endLearning(member)
        #Check and add new role
        await leveling.add_role(member)
      #Trc do voice bth -> Voice Study
      elif not any(word in before.channel.name for word in self.room_name) and any(word in after.channel.name for word in self.room_name):
        leveling.startLearning(member)
      else: 
        #Trg hop trc và sau đều là study_room
        if member.voice.self_video or member.voice.self_stream:
          print("Check videos 2")
          leveling.startLearning(member)
        else:
          print('Off cam')
          leveling.endLearning(member)
          await leveling.add_role(member)
        
       
# delete usser
  @commands.Cog.listener()
  async def on_member_leave(self,member):
    with open('/home/runner/Yang-Bot/users.json', 'r+') as f:
      file = json.load(f)
      users = file['users_list']
      f.close()
    for user in users:
      if member.id == user['id']:
        leveling.remove_user(user)
def setup(bot):
  bot.add_cog(leveling(bot))
