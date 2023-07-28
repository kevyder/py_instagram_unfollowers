from not_followers import NotUnfollowers
from time import sleep

from constants import IGUSERNAME, IGACCOUNT, IGPASSWORD


# Entry-Point
print("--------------------------------")
print("Instagram Unfollow-Checker V2")
print("--------------------------------\n")

# Run bot
sleep(1)
my_bot = NotUnfollowers(username=IGUSERNAME, password=IGPASSWORD, account=IGACCOUNT)
my_bot.check()
