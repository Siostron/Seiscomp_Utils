# Seiscomp_Utils
Bash and Python scrips around Seiscomp

- Event_mail.job :

Bash script called from Seiscomp *scalert* when a new event is declared. It uses *scbulletin*, *scxmldump* and *scmapcut* (https://www.seiscomp.de/) to create a bulletin and an image map to be attached to an email and a Telegram messages. Linux mailutils and telegram-send utils (https://github.com/rahiel/telegram-send) must be installed and configured.


- check_seedlink_problems.job :

Bash script to look for seedlink problems in a network of seismic stations received by a Seiscomp Server. It sends an alert by email and Telegram if a configurable Time delay is overpassed by one or more stations. Another message is sent if the problem is solved in one or more stations. *slinktool* (https://github.com/EarthScope/slinktool), Linux mailutils and telegram-send utils (https://github.com/rahiel/telegram-send) must be installed and configured. It is advisable to run this script on a different computer than the Seiscomp server.

Ex:  ./check_seedlink_problems.job CA >& ./Trash/seedlink_check_CA.log &

- check_seedlink_problems_station.job :

Bash script to look for seedlink problems in single station of a seismic network received in a Seiscomp Server. It sends an alert by email and Telegram if a configurable Time delay is overpassed. Another alert is sent if the problem is solved. *slinktool* (https://github.com/EarthScope/slinktool), Linux mailutils and telegram-send utils (https://github.com/rahiel/telegram-send) must be installed and configured. It is advisable to run this script on a different computer than the Seiscomp server.

Ex: ./check_seedlink_problems_station.job CA ICJA >& ./Trash/seedlink_check_CA_ICJA.log &
