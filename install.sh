#!/bin/sh

DIR=$(dirname $(readlink -f $0))
CELLARET_PATH=/opt/Cellaret
APPLICATIONS_PATH=/usr/share/applications
PKGS='python python-wxtools python-markdown'

ABOUT() {
	clear
	cat <<'EOF'

Cellaret is a software program 
that browse and edit Markdown text.

Copyright 2014 Roman Verin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

EOF
}

HELP_INSTALL() {
	clear
	cat <<'EOF'
------------------------------------------------------------
Install help
------------------------------------------------------------

This install.sh file were tested only in Ubuntu 12.04.

EOF
}

SHOW_MENU() {
	clear
	cat <<'EOF'

=============== Install Cellaret 0.1.1 ================

Choose:

[1] Help
[2] Checking dependencies
[3] Install Cellaret

[q] Quit

EOF
}

CHECK_PACKAGES() {
	for pkg in $PKGS
	do
		dpkg-query -W -f='${Package} ${Status} ${Version}\n' $pkg
	done
}

SHOW_MENU
read Choose
case $Choose in
	1)
		HELP_INSTALL
		read -p '[q] Exit ' answer
		case $answer in
			q)
				echo ''
				echo 'Exiting...'
				busybox sleep 1
				;;
		esac
		;;

	2)
		clear
		echo ''
		echo 'Checking dependencies...'
		echo ''
		CHECK_PACKAGES
		echo ''
		busybox sleep 1
		;;

	3)
		clear
		echo ''
		if test -d $CELLARET_PATH; then
			read -p 'Cellaret already installed. Update it? (Yes/No)? ' answer
			case $answer in
				y|Y|Yes|yes|YES)
					echo 'Yes'
					echo ''
					sudo rm -rf $CELLARET_PATH
					sudo mkdir $CELLARET_PATH
					sudo cp -rf $DIR/application $CELLARET_PATH/application
					sudo cp -rf $DIR/translations $CELLARET_PATH/translations
					sudo cp $DIR/cellaret.py $CELLARET_PATH/cellaret
					sudo chmod 0755 $CELLARET_PATH/cellaret
					sudo cp $DIR/images/cellaret-32.png $CELLARET_PATH/cellaret.png
					sudo cp $DIR/LICENSE $CELLARET_PATH/LICENSE
#					sudo cp $DIR/cellaret.desktop $APPLICATIONS_PATH/cellaret.desktop
					echo ''
					echo 'Cellaret updated.'
					busybox sleep 1
					;;
				*)
					echo 'No'
					echo ''
					echo 'Exiting...'
					busybox sleep 1
#					exit
					;;
			esac
		else
			sudo mkdir $CELLARET_PATH
			sudo cp -rf $DIR/application $CELLARET_PATH/application
			sudo cp -rf $DIR/translations $CELLARET_PATH/translations
			sudo cp $DIR/cellaret.py $CELLARET_PATH/cellaret
			sudo chmod 0755 $CELLARET_PATH/cellaret
			sudo cp $DIR/images/cellaret-32.png $CELLARET_PATH/cellaret.png
			sudo cp $DIR/LICENSE $CELLARET_PATH/LICENSE
			if test -x /usr/bin/desktop-file-install; then
				sudo desktop-file-install --rebuild-mime-info-cache $DIR/cellaret.desktop
			else
				sudo cp $DIR/cellaret.desktop $APPLICATIONS_PATH/cellaret.desktop
			fi
			if test -x /usr/bin/update-menus; then
				update-menus
			fi
			echo ''
			echo 'Cellaret installed.'
			busybox sleep 1
		fi
		echo ''
		;;

	*)
		echo 'Exiting...'
		busybox sleep 1
#		exit
		;;
esac
