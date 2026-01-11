#!/bin/sh

docker build -t phone_to_user_bot .
docker tag phone_to_user_bot kolenich/telegram-bots:phone_to_user_bot
docker push kolenich/telegram-bots:phone_to_user_bot