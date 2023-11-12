export K1="2f08ddd3"
export K2="1e8a1e0b"

I=0
X=$(./mypgp -rsa -g $K1 $K2)
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
