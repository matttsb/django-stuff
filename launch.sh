echo "commit: $1";
git add .
git commit -m "$1-commit"
git push origin master
ssh root@sendmemusic.com ./update.sh

