#!/bin/sh

if  [ "$#" = "0" ]
 then
  python deck_building_card.py
elif  [ "$1" = "test" ] 
 then
  python unit_test.py
else
  echo "error input"  
 fi
