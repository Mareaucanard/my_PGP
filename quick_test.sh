source gen_keys.sh
cat message.txt | ./mypgp -pgp -c $PB | ./mypgp -pgp -d $PV
echo "cat message.txt | ./mypgp -pgp -c $PB | ./mypgp -pgp -d $PV" > je2