from not_followers import NotUnfollowers
from redis_client import RedisClient
from email_sender import EmailSender
from time import sleep

from constants import IGUSERNAME, IGACCOUNT, IGPASSWORD


# Entry-Point
print("--------------------------------")
print("Instagram Unfollow-Checker V2")
print("--------------------------------\n")

# Run bot
sleep(1)
not_followers = NotUnfollowers(username=IGUSERNAME, password=IGPASSWORD, account=IGACCOUNT)
not_followers.check()
not_following_back = not_followers.not_following_back

# Redis
redis_client = RedisClient()
redis_client.connect()

last_not_followers = redis_client.get("not_followers")
last_not_followers = [not_follower.decode('utf-8') for not_follower in last_not_followers]
recent_unfollowers = list(set(not_following_back) - set(last_not_followers))
redis_client.delete("not_followers")
redis_client.rpush("not_followers", *not_following_back)
redis_client.disconnect()

# Email sender
if recent_unfollowers:
    email_sender = EmailSender()
    email_sender.send_email(recent_unfollowers)
