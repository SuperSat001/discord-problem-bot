import discord
import os
from discord.ext import commands
from keep_alive import keep_alive
from replit import db
import random
import sys
from test import send_notifs

m = "Bot on brub! " +  str(db["n"])
send_notifs(m)

subjects = ["physics", "maths"]
# info = ["received", "leaderboard", "currPos", "queue"]

def addNewSubj(subj):
    if subj not in db.keys():
        db[subj] = dict()
        db[subj]["receivedNum"] = 0
        db[subj]["leaderboard"] = dict()
        db[subj]["currPosn"] = 0
        db[subj]["queue"] = []
        db[subj]["pairing"] = dict()
        db[subj]["solved"] = dict()
        db[subj]["doneUser"] = []
        db[subj]["doneCounter"] = 0

        
        db[subj]["saveChannelId"] = 869261862762590288  
        db[subj]["postChannelId"] = 869258696763539496
        db[subj]["leadMessageId"] = 869263210124021842

    db[subj]["infoChannelId"] = 869258486037479477

    db[subj]["altChannelId"] = 869261885109850172

    db[subj]["pingRoleId"] = 869263436025065482

    db[subj]["leadChannelId"] = 869263128469315604

for subj in subjects:
    addNewSubj(subj)   

botManager = "CMS Authorized"

doneCounter = 0
doneUser = []
needed = 2

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="?")


async def lbmaker(lb, subj):
    sort_orders = sorted(lb.items(), key=lambda x: x[1], reverse=True)

    s = f"**{subj.title()} Leaderboard**\n ```"
    for i in sort_orders:
        name = i[0]
        pts = i[1]

        user = await bot.fetch_user(int(name))
        #print(user)


        temp = len(str(user)) + len(str(pts))
        
        if temp < 35:
            s += str(user) + " "*(35-temp) + str(pts)
        else:
            s += str(user) + " " + str(pts)
        s += "\n"

    s += "```"
    return s


async def sendNewProblem(ctx, subj, n):
    global doneUser
    q = db[subj]["queue"]

    if len(q) == 0:
        infoChannel = bot.get_channel(db[subj]["infoChannelId"])
        await infoChannel.send("No more problems rn, time for you to send problems.")
        return        

    curr = db[subj]["currPosn"]
    postChannel = bot.get_channel(db[subj]["postChannelId"])
    r = q[n]
    del q[n]
    db[subj]["queue"] = q
    curr += 1
    db[subj]["currPosn"] = curr
    sendText = f"```Problem {curr}\nAuthor - " + db[subj][str(r)][0] +"```"
    pubMess = await postChannel.send(sendText)
    #await pubMess.publish()
    for file in db[subj][str(r)][1]:
        pubMess = await postChannel.send(file)
        #await pubMess.publish()
    #print("pairing" in db[subj].keys(), db[subj].keys())
    db[subj]["pairing"][curr] = r

    marathon = discord.utils.get(ctx.guild.roles, id=db[subj]["pingRoleId"])
    #await postChannel.send(f'{marathon.mention}')
    await ctx.send("Posting new question.")
    db[subj]["doneUser"] = []


@bot.event
async def on_ready():
    k = db["n"]
    db["n"] += 1
    print(f'{bot.user.name} has connected to Discord! {k}')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="your problems"))


if "bdayUser" not in db.keys():
    db["bdayUser"] = []
    db["bdayCount"] = 0

bdayneed = 100
bdayChannelId = 869258939202682940

@bot.command(name="happybirthday", help="Server birthday special")
async def hbd(ctx):
    if ctx.message.author.id in db["bdayUser"]:
        await ctx.send("https://i.imgur.com/g4WFfT3.png")
        return
    await ctx.send(f"Thank you <@{ctx.message.author.id}> !")
    count = db["bdayCount"]
    count += 1
    db["bdayCount"] = count
    await ctx.send(f"{count} wishes received. {bdayneed - count} left.")
    users = db["bdayUser"]
    users.append(ctx.message.author.id)
    db["bdayUser"] = users
    
    t = bdayneed//10
    if ((bdayneed - count) <= 10) or ((bdayneed - count) % t == 0):
        bdayChannel = bot.get_channel(bdayChannelId)
        s = "Now people needed are " + str(bdayneed - count)
        send_notifs(s)
        await bdayChannel.send(s)


    if count == bdayneed:
        await ctx.send("https://i.pinimg.com/originals/e7/4d/93/e74d931893cd73cdd5c54847aa25b369.gif")
        await ctx.send("Happy Birthday Server.")    
    
@bot.command(name="bdayreset", help="reset bday users")
@commands.has_role(botManager)
async def bdayreset(ctx, num:int):
    db["bdayUser"] = []
    db["bdayCount"] = num
    await ctx.send("changed")

pingC = 0
@bot.command(name="ping", help="pings delta")
@commands.has_role(botManager)
async def ping(ctx):
    global pingC
    pingC += 1
    send_notifs("Pinged you "+str(pingC))
    await ctx.send("Pong")

@bot.command(name="add", help="adds two numbers (testing)")
@commands.has_role(botManager)
async def add(ctx, num: int, num2: int):
    await ctx.send("Sum is " + str(num + num2))

@bot.command(name="yaw")
@commands.has_role(botManager)
async def yaw(ctx):
    await ctx.send("https://media.discordapp.net/attachments/865430707756728321/865564348592160778/710978188506955867.png")

@bot.command(name="sendmessage", help="send message to a channel")
@commands.has_role(botManager)
async def sendmessage(ctx, num:int):
    sendChannel = bot.get_channel(num)
    text = ctx.message.content.split(" ")[2:]
    s = " ".join(text)
    await sendChannel.send(s)

@bot.command(name="editmessage", help="edits a message")
@commands.has_role(botManager)
async def editmessage(ctx, num1:int, num2:int):
    sendChannel = bot.get_channel(num1)
    msg = await sendChannel.fetch_message(num2) 
    text = ctx.message.content.split(" ")[3:]
    s = " ".join(text)
    await msg.edit(content=s)
    await ctx.send("Edited")

@bot.command(name="curr", help="number of problems posted")
@commands.has_role(botManager)
async def curr(ctx, subj:str, num:int):
    db[subj]["currPosn"] = num
    await ctx.send(f"{subj} number set to {num}")

@bot.command(name="queue", help="add problem to queue")
@commands.has_role(botManager)
async def queue(ctx, subj:str, num: int):
    db[subj]["queue"].append(num)
    posn = len(db[subj]["queue"])
    #print(db[subj]["queue"])
    await ctx.send(f"{subj} problem {num} added to queue at position {posn}")

@bot.command(name="printq", help="prints the queue")
@commands.has_role(botManager)
async def printq(ctx, subj:str):
    q = db[subj]["queue"]
    s = f"{subj} queue - "
    for i in q:
        s += str(i) + " "
    await ctx.send(s)

@bot.command(name="remove", help="removes ith position from the queue 1-based indexing")
@commands.has_role(botManager)
async def remove(ctx, subj :str, num:int):
    q = db[subj]["queue"]
    if num < 1 or num > len(q):
        await ctx.send("Invalid position")
    else:
        r = q[num-1]
        del q[num-1]
        db[subj]["queue"] = q
        await ctx.send(f"{subj} Deleted problem {r} from queue")

@bot.command(name="shuffle", help="shuffles the queue")
@commands.has_role(botManager)
async def shuffle(ctx, subj:str):
    q = db[subj]["queue"]
    random.shuffle(q)
    db[subj]["queue"] = q
    await ctx.send(f"{subj} queue shuffled")


@bot.command(name="post", help="admin only post problem from queue")
@commands.has_role(botManager)
async def post(ctx, subj:str, num: int):
    q = db[subj]["queue"]
    if num > len(q):
        await ctx.send("Insuffient problems in queue")
    elif num < 1:
        await ctx.send("Bruh")
    else:
        r = q[num-1]
        curr = db[subj]["currPosn"]
        await ctx.send(f"{subj} problem {r}/{num} posted at place {curr+1}")
        await sendNewProblem(ctx, subj, num-1)
        
@bot.command(name="reqd", help="number of people reqd for new problem")
@commands.has_role(botManager)
async def reqd(ctx, num: int):
    global needed
    needed = num
    for subj in subjects:
        db[subj]["doneUser"] = []
        db[subj]["doneCounter"] = 0
    await ctx.send(f"{needed} user(s) are now required")

@bot.command(name="donereset", help="done reset")
@commands.has_role(botManager)
async def donereset(ctx, subj:str):
    db[subj]["doneUser"] = []
    await ctx.send(f"{subj} done reset")

           
@bot.command(name="addpoints", help="adds points to a person on leaderboard")
@commands.has_role(botManager)
async def addpoints(ctx, member: discord.Member, subj:str, num: int):
    pts = num
    if str(member.id) not in db[subj]["leaderboard"].keys():
        db[subj]["leaderboard"][str(member.id)] = num
    else:
        pts += db[subj]["leaderboard"][str(member.id)] 
        db[subj]["leaderboard"][str(member.id)] = pts
    await ctx.send(f"{num} are added to {member.name} in {subj} total {pts} pts")

    newLb = await lbmaker(db[subj]["leaderboard"], subj)
    leadChannel = bot.get_channel(db[subj]["leadChannelId"])
    leadMessage = await leadChannel.fetch_message(str(db[subj]["leadMessageId"]))
    await leadMessage.edit(content = newLb)


@bot.command(name="seelb", help="shows leaderboard")
@commands.has_role(botManager)
async def seelb(ctx, subj:str):
    text = await lbmaker(db[subj]["leaderboard"], subj)
    await ctx.send(text)

# @bot.command(name="makenewsubject", help="add new subject to the marathon")
# @commands.has_role(botManager)

#user commands

@bot.command(name="length", help="number of problems added to queue")
async def length(ctx, subj:str=None):
    if subj==None:
        await ctx.send("Missing arguements, enter subject")
        return
    x = len(db[subj]["queue"])
    await ctx.send(f"{subj} queue has {x} problems")

@bot.command(name="done", help="requests for new problem")
async def done(ctx, subj:str=None):
    if subj==None:
        await ctx.send("Missing arguements, enter subject")
        return
    if len(db[subj]["queue"]) == 0:
        await ctx.send("No more problems rn, time for you to send problems.")
        return 

    r = db[subj]["doneCounter"]

    doneSender = ctx.message.author.id
    if doneSender in db[subj]["doneUser"]:
        await ctx.send("You are too fast for others sir")
        await ctx.send(f"Need {needed-r} more user(s)")
        return 
    
    r += 1
    r %= needed
    db[subj]["doneCounter"] = r
    db[subj]["doneUser"].append(doneSender)

    if r%needed==0:
        await sendNewProblem(ctx, subj, 0)
    else:
        await ctx.send(f"Need {needed-r%needed} more user(s)")

@bot.command(name="solved", help="shows problems solved")
async def solved(ctx, member: discord.Member = None, subj:str = None):
    if member == None or subj == None:
        await ctx.send("Missing arguements, enter member and subject")
        return
    if str(member.id) not in db[subj]["solved"].keys():
        db[subj]["solved"][str(member.id)] = []
    ar = list(db[subj]["solved"][str(member.id)])
    ar = [int(x) for x in ar]
    ar.sort()
    ar = [str(x) for x in ar]
    s = "solved - " + " ".join(ar)
    await ctx.send(f"{member.name} has {s} in {subj}")

@bot.command(name="problem", help="submit new problem")
async def problem(ctx, subj : str = None, ans:str = None):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Command only works in DM")
        return

    if ans == None or subj == None:
        await ctx.send("Missing arguements, enter subject and ans")
        return
    
    try:
        ans = float(ans)
    except:
        await ctx.send("Submitted answer not numeric. Send numeric answer for standardisation.")
        return

    if subj not in subjects:
        s = "` `".join(subjects)
        await ctx.send(f"Subject doesn't exist. These are available subjects - `{s}`.")
        return

    
    receivedNum = db[subj]["receivedNum"]
    receivedNum += 1
    db[subj]["receivedNum"] = receivedNum

    await ctx.send(f"Problem {receivedNum} received")

    saveChannel = bot.get_channel(db[subj]["saveChannelId"])
    altChannel = bot.get_channel(db[subj]["altChannelId"])        


    sendText = f"```Problem {receivedNum} received from {ctx.message.author} {ctx.message.author.id}```\n||{ans}||"    

    
    allFiles = []
    await saveChannel.send(content=sendText)
    await altChannel.send(content=sendText)
    for file in ctx.message.attachments:
        allFiles.append(file.url)
        #print(file.url)
        await saveChannel.send(file)
        await altChannel.send(file)

    # p = problem(message.author.name, text, allFiles)
    # print(p, receivedNum)
    savingArray = [ctx.message.author.name, allFiles, ans]
    #print(savingArray)

    db[subj][receivedNum] = savingArray      
    #print("Done")

@bot.command(name="submit", help="submit answer")
async def submit(ctx, subj : str = None, num : str = None, ans : str = None):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Command only works in DM")
        return

    if ans == None or subj == None or num == None:
        await ctx.send("Missing arguements, enter subject, problem number and answer")
        return
    
    try:
        ans = float(ans)
    except:
        await ctx.send("Submitted answer not numeric.")
        return

    try:
        num = int(num)
    except:
        await ctx.send("Problem number incorrect.")
        

    if subj not in subjects:
        s = "` `".join(subjects)
        await ctx.send(f"Subject doesn't exist. These are available subjects - `{s}`.")
        return

    try:
        origProb = db[subj]["pairing"][str(num)]
        #origProb = num
    except:
        await ctx.send("This question is not answerable via bot")
        return 
    
    correctAns = db[subj][str(origProb)][2]
    #print(correctAns)
    try:
        if float(correctAns) == float(ans):
            await ctx.send("Correct!")
            infoChannel = bot.get_channel(db[subj]["infoChannelId"])
            await infoChannel.send(f"<@{ctx.message.author.id}> got Problem {num} correct!")

            print(num, db[subj]["currPosn"])

            if str(num) == str(db[subj]["currPosn"]):
                # global doneCounter, doneUser
                #print("abhi", doneUser, doneCounter)

                if ctx.message.author.id not in db[subj]["doneUser"]:
                    db[subj]["doneCounter"] += 1
                    #print("new", doneCounter)
                    db[subj]["doneUser"].append(ctx.message.author.id)

                    if db[subj]["doneCounter"]%needed == 0:
                        await sendNewProblem(infoChannel, subj, 0)

            if str(ctx.message.author.id) not in db[subj]["solved"].keys():
                db[subj]["solved"][str(ctx.message.author.id)] = []

            #print("1")
            
            if num not in db[subj]["solved"][str(ctx.message.author.id)]:
                solvedProbs = db[subj]["solved"][str(ctx.message.author.id)]
                solvedProbs.append(num)
                db[subj]["solved"][str(ctx.message.author.id)] = solvedProbs

                pts = 1
                if str(ctx.message.author.id) not in db[subj]["leaderboard"].keys():
                    db[subj]["leaderboard"][str(ctx.message.author.id)] = 1
                else:
                    pts += db[subj]["leaderboard"][str(ctx.message.author.id)] 
                    db[subj]["leaderboard"][str(ctx.message.author.id)] = pts
                await ctx.send(f"1 point added total {pts} pts")  

                newLb = await lbmaker(db[subj]["leaderboard"], subj)
                leadChannel = bot.get_channel(db[subj]["leadChannelId"])
                leadMessage = await leadChannel.fetch_message(str(db[subj]["leadMessageId"]))
                await leadMessage.edit(content = newLb)


        else:
            await ctx.send("That's wrong")

    except Exception as e:
        print(e.__class__)
        print(f"Error {origProb} {ctx.message.author.name} {ctx.message.author.id}")
        await ctx.send("Error, please contact server staff")

    




@bot.event
async def on_message(message):
    global doneCounter, doneUser
    if message.author == bot.user:
        return
    await bot.process_commands(message)

keep_alive()
bot.run(TOKEN)
