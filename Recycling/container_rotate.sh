if [ $# -ne 3 ]
then
  echo "Usage: ./container_rotate.sh (recycle existing containers (1 for yes, 0 for no)) (rotate ips (1 for yes, 0 for no)) (create new containers (1 for yes, 0 for no))"
  exit 1
fi

honeypot1_ip=$(sudo cat ./properties/DATABASE_1_properties | cut -d' ' -f1)
honeypot2_ip=$(sudo cat ./properties/DATABASE_2_properties | cut -d' ' -f1)
honeypot3_ip=$(sudo cat ./properties/DATABASE_3_properties | cut -d' ' -f1)
honeypot4_ip=$(sudo cat ./properties/DATABASE_4_properties | cut -d' ' -f1)

if [ $1 -eq 1 ]
then
  sudo ./recycler.sh DATABASE_1 $honeypot1_ip 0
  sudo ./recycler.sh DATABASE_2 $honeypot2_ip 0
  sudo ./recycler.sh DATABASE_3 $honeypot3_ip 0
  sudo ./recycler.sh DATABASE_4 $honeypot4_ip 0
fi

if [ $2 -eq 1 ]
then
  sudo ./copy_data.sh
  temp=$honeypot4_ip
  honeypot4_ip=$honeypot3_ip
  honeypot3_ip=$honeypot2_ip
  honeypot2_ip=$honeypot1_ip
  honeypot1_ip=$temp

  honeypot1_port=$(sudo cat ./properties/DATABASE_1_properties | cut -d' ' -f2)
  honeypot2_port=$(sudo cat ./properties/DATABASE_2_properties | cut -d' ' -f2)
  honeypot3_port=$(sudo cat ./properties/DATABASE_3_properties | cut -d' ' -f2)
  honeypot4_port=$(sudo cat ./properties/DATABASE_4_properties | cut -d' ' -f2)

  sudo echo "$honeypot1_ip $honeypot1_port" > ./properties/DATABASE_1_properties
  sudo echo "$honeypot2_ip $honeypot2_port" > ./properties/DATABASE_2_properties
  sudo echo "$honeypot3_ip $honeypot3_port" > ./properties/DATABASE_3_properties
  sudo echo "$honeypot4_ip $honeypot4_port" > ./properties/DATABASE_4_properties
fi

if [ $3 -eq 1 ]
then
  sudo ./recycler.sh DATABASE_1 $honeypot1_ip 1
  sudo ./recycler.sh DATABASE_2 $honeypot2_ip 1
  sudo ./recycler.sh DATABASE_3 $honeypot3_ip 1
  sudo ./recycler.sh DATABASE_4 $honeypot4_ip 1
fi