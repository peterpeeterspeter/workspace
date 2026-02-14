#!/bin/bash

# Site credentials helper
# Source this to get site WordPress API credentials

get_site_creds() {
  local site=$1
  case $site in
    hobbysalon)
      echo "https://www.hobbysalon.be/wp-json kris BAvt knyO ystE qYXk YQUo v9mu"
      ;;
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
    *)
      echo ""
      return 1
      ;;
  esac
}
