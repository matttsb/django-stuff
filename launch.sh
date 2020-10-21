echo "commit: $1";
git add .
git commit -m "$1"
ssh root@sendmemusic.com ./update.sh

