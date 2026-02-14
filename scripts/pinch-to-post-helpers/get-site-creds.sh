#!/bin/bash

# Get site credentials for pinch-to-post
# Returns: URL username password

SITE="$1"

case $SITE in
  crashcasino)
    echo "https://crashcasino.io/wp-json peter 3vRhtTs2khfdLtTiDFqkdeXI"
    ;;
  crashgame)
    echo "https://crashgamegambling.com/wp-json peter MioX SygN Xaz6 pK9o RUiK tBMF"
    ;;
  freecrash)
    echo "https://freecrashgames.com/wp-json peter F8Mg yZXM qJy4 jQvp BMeZ FoMG"
    ;;
  cryptocrash)
    echo "https://cryptocrashgambling.com/wp-json peter R3kQ 6vRA UwYd x7Cn KEtT Pk83"
    ;;
  hobbysalon)
    echo "https://www.hobbysalon.be/wp-json kris BAvt knyO ystE qYXk YQUo v9mu"
    ;;
  *)
    echo ""
    exit 1
    ;;
esac
