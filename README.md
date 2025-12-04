# Seiscomp_Utils
Bash and Python scrips around Seiscomp

Event_mail.job

Script called from Seiscomp *scalert* when a new event is declared. It uses *scbulletin*, *scxmldump* and *scmapcut* (https://www.seiscomp.de/) to create a bulletin and an image map to be attached to an email and a Telegram messages. (Linux mailutils and telegram-send utils (https://github.com/rahiel/telegram-send) must be installed and configured.
                 -  
