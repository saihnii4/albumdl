#!/bin/sh

if [[ !(-v CLIENT_ID) || !(-v CLIENT_SECRET) ]]; then
	if [ -e .env ]; then
		source .env # wth
	else
		echo -e "\033[1mCLIENT_ID or CLIENT_SECRET missing, please set them\033[0m"
		exit 1
	fi
fi

python "$(dirname $0)/query.py" $1 | xargs gum choose | python "$(dirname $0)/dl.py"

