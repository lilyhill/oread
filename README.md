# OREAD

A simple telegram bot for collating my URLs for me to help in write my [readlog](https://www.suriyaganesh.com/readlog).

## TODO:
- [ ] updates for editing messages.
- [x] simple sub pointers by quoting the message.
- [x] 
- [x] Sort in reverse order in the UI. remember it as well. (React?)
- [ ] API for integrating with other services. eg. at the end of everyday I want oread to trigger a github action that would get the readlist from yesterday and deploy it on my website.
- [x] simple web interface to show all links
- [x] Working MVP with base features

## Features:

- Recognise seperate URLs in a message and store them in seperate sections
- Simple web interface to look at the URLs

## Issues:

- [x] Datetime is not properly working. While saving the timezone is messing up  

### A bit on motivation:
When I started writing my readlog. I was unable to share the links that I read in my phone. I send to myself using whatsapp and then re-add them in my laptop. This bot collates all the links sent to it and provides a web interface to visit it. The bot can be accessed from [@oread_bot](t.me/oread_bot) in telegram.

### Running in Dev mode

Add secret key in env file, or docker-compose.yml file and then run, `docker-compose up`


## fly scp to a machine

proxy the machine using
```shell
fly proxy 10022:22
```

then in another terminal 
connect using the pub file.
```shell
scp -i <path_to_ssh_file> -P 10022 root@localhost:/home/app/web/db.sqlite3 may2023.sqlite3
```

