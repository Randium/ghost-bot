'''                                                                                         _             
   _____ _               _     _______            _         _____           _              | |             
  / ____| |             | |   |__   __|          | |       / ____|         | |             | |_ _ __ ___  
 | |  __| |__   ___  ___| |_     | |_ __ __ _  __| | ___  | |     ___ _ __ | |_ ___ _ __   | __| '_ ` _ \
 | | |_ | '_ \ / _ \/ __| __|    | | '__/ _` |/ _` |/ _ \ | |    / _ \ '_ \| __/ _ \ '__|  | |_| | | | | |
 | |__| | | | | (_) \__ \ |_     | | | | (_| | (_| |  __/ | |___|  __/ | | | ||  __/ |      \__|_| |_| |_|
  \_____|_| |_|\___/|___/\__|    |_|_|  \__,_|\__,_|\___|  \_____\___|_| |_|\__\___|_| 
'''

M_CHANNEL = "409085003503239169"
BOT_TOKEN = "I remembered to remove this deffo"

from discord.ext import commands
import sqlite3
import os 
import re 


bot = commands.Bot(command_prefix='$')

def setup_db():
	# Open and read the file as a single buffer
	fd = open('marketplace_sql_schema.sql', 'r')
	sqlFile = fd.read()
	fd.close()

	# all SQL commands (split on ';')
	sqlCommands = sqlFile.split(';')

	# Execute every command from the input file
	for command in sqlCommands:
		# This will skip and report errors
		# For example, if the tables do not yet exist, this will skip over
		# the DROP TABLE commands
		try:
			c.execute(command)
		except:
			print("Command skipped")


async def check_if_investor(user_id):
	c.execute("SELECT balance FROM players WHERE user_id = ?;", (user_id,))
	rows = c.fetchall()
	if rows:
		return(True)
	else:
		return(False)

async def get_inv_by_id(user_id):
	print("Getting inv of " + user_id)
	c.execute("SELECT * FROM inventory_items WHERE user_id = ?;", (user_id,))
	print("Fetched from db")
	rows = c.fetchall()
	print(rows)
	print("Returning...")
	return(rows)

async def add_item_to_inventory(user_id, item, quantity):
	try:
		r = c.execute("INSERT INTO inventory_items (user_id, item, quantity) VALUES (?, ?, ?);", (user_id, item, quantity))
		print(r)
		conn.commit()
	except:
		try:
			print("UPDATE not INSERT")
			r = c.execute("UPDATE inventory_items SET quantity = ? WHERE user_id = ? AND item = ?;", (quantity, user_id, item))
			print(r)
			conn.commit()
		except:
			await bot.say("Something went wrong! Try again or contact a bot dev.")
			return("broken")

async def setup_player(user_id, starterpack):
	if starterpack:
		c.execute("INSERT INTO players (user_id, balance) VALUES (?, 10);", (user_id,))
		#c.execute("INSERT INTO inventory_items (user_id, item, quantity) VALUES (?, ?, ?);", (user_id, emoji, quantity) #test code; ignore
		#Starter pack code goes here

		conn.commit()


setup = os.path.isfile('./marketplace.db')
conn = sqlite3.connect('marketplace.db')
c = conn.cursor()
if setup == False:
	print("setting up DB")
	setup_db()
else:
	print("Already set up DB")




async def username(user_id):
	print("Getting username of " + user_id)
	mem = await bot.get_user_info(user_id)
	return mem.name


@bot.command(pass_context=True)
async def add_item(ctx, user_id, item, quantity):
	if user_id.isdigit() == False:
		user_id = re.findall('\d+', user_id)[0]
	await add_item_to_inventory(user_id, item, quantity)
	await bot.say("Done. (I hope)")


@bot.command(pass_context=True)
async def inv(ctx, user_id=None):
	if user_id == None:
		print("Setting UID")
		user_id = ctx.message.author.id

	if user_id.isdigit() == False:
		user_id = re.findall('\d+', user_id)[0]
	rows = await get_inv_by_id(user_id)
	
	if not rows:
		await bot.say("That user has no inventory!")
	else:
		#await bot.say("**" + username(user_id) + "**:")
		inventory = "**" + await username(user_id) + "**:\n"
		for row in rows:
			inventory+=str(row[1]) + " x " + str(row[2]) + "\n"
			#await bot.say(" - " + str(row[1]) + " x " + str(row[2]))
		await bot.say(inventory)









@bot.command(pass_context=True)
async def test(ctx):
	await bot.say("ree")



print("running bot")
bot.run(BOT_TOKEN)