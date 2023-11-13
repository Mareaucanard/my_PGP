I=0
X=$(time ./mypgp -pgp -genkey)
echo "$X"
for word in $X;
do
    I=$(bc <<< "$I + 1")
    if [ $I -eq 3 ];
    then
        export PB=$word
    fi
    if [ $I -eq 6 ];
    then
        export PV=$word
    fi
done
