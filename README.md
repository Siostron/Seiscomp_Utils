# Seiscomp_Utils
Bash and Python scrips around Seiscomp

Event_mail.job - Script called from Seiscomp scalert when a new event is declared
                 uses scbulletin, scxmldump and scmapcut (https://www.seiscomp.de/) 
                 to create a bulletin and an image map to be attached to an email
                 and a Telegram message.
                 
                 mail - Linux mailutils must be installed and configured
                 telegram-send - Telegram-send utils must be installed (https://github.com/rahiel/telegram-send)
