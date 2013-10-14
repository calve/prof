## Script pour envoyé un fichier sur prof
# CC0 No rights reserved

login=login
passwd=password #oui, en clair, ca craint


#On initialize la session
curl -ss "https://prof.fil.univ-lille1.fr/index.php"  -c cookie > tmp
curl -ss "https://prof.fil.univ-lille1.fr/login.php" --data "login=$login&passwd=$passwd&++O+K++=Valider" -b cookie > tmp

# On récupere la liste des ids
curl -ss "https://prof.fil.univ-lille1.fr/select_projet.php" -b cookie | grep /OPTION
read -p "Please select an option value above : " projectvalue

#On récupere la liste et l'état des TPS
curl -ss "https://prof.fil.univ-lille1.fr/main.php" --data "id_projet=$projectvalue" -b cookie | grep "echeance"
read -p "Please select an id above : " idtp

curl -ss "https://prof.fil.univ-lille1.fr/upload.php" --data "id=$idtp" -b cookie > tmp

#on upload le fichier
if [ "$1" ]; then
    curl -ss "https://prof.fil.univ-lille1.fr/upload2.php" --form "fichier1=@$1" --form "MAX_FILE_SIZE=1000000" -b cookie > tmp
else
    read -p "Give me the file : " file
    curl -ss "https://prof.fil.univ-lille1.fr/upload2.php" --form "fichier1=@$file" --form "MAX_FILE_SIZE=1000000" -b cookie > tmp
fi


cat tmp | grep "Le fichier .* est bien enregistr"

if [ $? ]; then
    echo "Erreur dans l'upload du fichier. Vérifiez ce que vous faites, et que le TP que vous essayé de rendre est bien ouvert !"
    exit 1
fi
rm tmp
exit 0

    



