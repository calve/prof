## Script pour envoyé un fichier sur prof
# CC0 No rights reserved

baseurl="https://prof.fil.univ-lille1.fr/"
login=debusschere

#On récupère le mot de passe
echo -n Password: 
read -s -r passwd
echo

#On initialize la session
curl -ss $baseurl"index.php"  -c cookie > tmp

curl -ss $baseurl"login.php" --data "login=$login" --data "passwd=$passwd" --data "++O+K++=Valider" -b cookie > tmp

# On récupere la liste des ids 
                                                #awk -F"VALUE=\"|\">|</OPTION>" '{ print $3 " -> " $2}'
curl -ss $baseurl"select_projet.php" -b cookie | grep "<\/OPTION>" | awk -F"VALUE=\\\"|\">|</OPTION>" '{ print $3 " -> " $2}'
read -p "Please select an option value above : " projectvalue

#On récupere la liste et l'état des TPS
curl -ss $baseurl"main.php" --data "id_projet=$projectvalue" -b cookie | grep "echeance"
read -p "Please select an id above : " idtp

curl -ss $baseurl"upload.php" --data "id=$idtp" -b cookie > tmp

#on upload le fichier
if [ "$1" ]; then
    curl -ss $baseurl"upload2.php" --form "fichier1=@$1" --form "MAX_FILE_SIZE=1000000" -b cookie > tmp
else
    read -p "Give me the file : " file
    curl -ss $baseurl"upload2.php" --form "fichier1=@$file" --form "MAX_FILE_SIZE=1000000" -b cookie > tmp
fi


cat tmp | grep "Le fichier .* est bien enregistr"

if [ $? ]; then
    echo "Erreur dans l'upload du fichier. Vérifiez ce que vous faites, et que le TP que vous essayé de rendre est bien ouvert !"
    exit 1
fi
rm tmp
exit 0

    



