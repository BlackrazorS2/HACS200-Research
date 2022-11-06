d1_stopped=$(sudo pm2 list | grep DATABASE_1 | grep stopped | wc -l)
d2_stopped=$(sudo pm2 list | grep DATABASE_2 | grep stopped | wc -l)
d3_stopped=$(sudo pm2 list | grep DATABASE_3 | grep stopped | wc -l)
d4_stopped=$(sudo pm2 list | grep DATABASE_4 | grep stopped | wc -l)

honeypot1_ip=$(sudo cat ./properties/DATABASE_1_properties | cut -d' ' -f1)
honeypot2_ip=$(sudo cat ./properties/DATABASE_2_properties | cut -d' ' -f1)
honeypot3_ip=$(sudo cat ./properties/DATABASE_3_properties | cut -d' ' -f1)
honeypot4_ip=$(sudo cat ./properties/DATABASE_4_properties | cut -d' ' -f1)

if [ $d1_stopped -ne 0 ]
then
  sudo ./recycler.sh DATABASE_1 $honeypot1_ip 1
fi

if [ $d2_stopped -ne 0 ]
then
  sudo ./recycler.sh DATABASE_2 $honeypot2_ip 1
fi

if [ $d3_stopped -ne 0 ]
then
  sudo ./recycler.sh DATABASE_3 $honeypot3_ip 1
fi

if [ $d4_stopped -ne 0 ]
then
  sudo ./recycler.sh DATABASE_4 $honeypot4_ip 1
fi