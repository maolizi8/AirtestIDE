#!/bin/sh

./aapt a KivyIns-debug.apk  assets/private.mp3
./aapt a KivyIns-debug.apk  assets/script_registry.txt

echo "resign new apk..."
jarsigner -verbose -sigalg SHA1withDSA -digestalg SHA1 -keystore firebase_keystore -storepass 5485726 KivyIns-debug.apk firebase_key

exit 0
