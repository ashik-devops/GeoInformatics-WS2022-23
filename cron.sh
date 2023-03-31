# nohup sh cron.sh &

cd /Users/ashikmahmud/MyDocuments/Personal/GEO2023EX/Final
while true; do
 python periodicScrapper.py && python insertData.py
 sleep 1000
done 
