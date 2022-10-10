if [ $# -ne 3 ]
then
  echo "Usage: ./container_rotate.sh (recycle existing containers (1 for yes, 0 for no)) (rotate ips (1 for yes, 0 for no)) (create new containers (1 for yes, 0 for no))"
  exit 1
fi

honeypot1_ip=$(cat ./properties/honeypot1_properties | cut -d' ' -f1)
honeypot2_ip=$(cat ./properties/honeypot2_properties | cut -d' ' -f1)
honeypot3_ip=$(cat ./properties/honeypot3_properties | cut -d' ' -f1)
honeypot4_ip=$(cat ./properties/honeypot4_properties | cut -d' ' -f1)

if [ $1 -eq 1 ]
then
  ./recycler.sh honeypot1 $honeypot1_ip 0
  ./recycler.sh honeypot2 $honeypot2_ip 0
  ./recycler.sh honeypot3 $honeypot3_ip 0
  ./recycler.sh honeypot4 $honeypot4_ip 0
fi

if [ $2 -eq 1 ]
then
  
 ./copy_data.sh 
  temp=$honeypot4_ip
  honeypot4_ip=$honeypot3_ip
  honeypot3_ip=$honeypot2_ip
  honeypot2_ip=$honeypot1_ip
  honeypot1_ip=$temp

  honeypot1_port=$(cat ./properties/honeypot1_properties | cut -d' ' -f2)
  honeypot2_port=$(cat ./properties/honeypot2_properties | cut -d' ' -f2)
  honeypot3_port=$(cat ./properties/honeypot3_properties | cut -d' ' -f2)
  honeypot4_port=$(cat ./properties/honeypot4_properties | cut -d' ' -f2)

  echo "$honeypot1_ip $honeypot1_port" > ./properties/honeypot1_properties
  echo "$honeypot2_ip $honeypot2_port" > ./properties/honeypot2_properties
  echo "$honeypot3_ip $honeypot3_port" > ./properties/honeypot3_properties
  echo "$honeypot4_ip $honeypot4_port" > ./properties/honeypot4_properties
fi

if [ $3 -eq 1 ]
then
  ./recycler.sh honeypot1 $honeypot1_ip 1
  ./recycler.sh honeypot2 $honeypot2_ip 1
  ./recycler.sh honeypot3 $honeypot3_ip 1
  ./recycler.sh honeypot4 $honeypot4_ip 1
fi
