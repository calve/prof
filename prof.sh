## Script pour envoyé un fichier sur prof
# CC0 No rights reserved

# remplacez login par votre nom d'utilisateur
# usage : ./prof.sh [archive.tar.gz]

baseurl="https://prof.fil.univ-lille1.fr/"
login=login

#On récupère le mot de passe
echo -n Password: 
read -s -r passwd
echo

#On initialize la session
curl -ss $baseurl"index.php"  -c cookie > tmp

curl -ss $baseurl"login.php" --data "login=$login" --data-urlencode "passwd=$passwd" --data "++O+K++=Valider" -b cookie > tmp

# On récupere la liste des ids 
curl -ss $baseurl"select_projet.php" -b cookie | grep "<\/OPTION>" | awk -F"VALUE=\\\"|\">|</OPTION>" '{ print $3 " -> " $2}'
read -p "Please type one of the numbers above : " projectvalue

#On récupere la liste et l'état des TPS
curl -ss $baseurl"main.php" --data "id_projet=$projectvalue" -b cookie | grep echeance | colrm 1 46 | sed "s/')\">\|<\/a><\/td>/ /g"
read -p "Please type on of the numbers above : " idtp

curl -ss $baseurl"upload.php" --data "id=$idtp" -b cookie > tmp

#on upload le fichier
if [ "$1" ]; then
    curl -ss $baseurl"upload2.php" --form "fichier1=@$1" --form "MAX_FILE_SIZE=1000000" -b cookie > tmp
else
    read -p "Give me the file : " file
    curl -ss $baseurl"upload2.php" --form "fichier1=@$file" --form "MAX_FILE_SIZE=1000000" -b cookie > tmp
fi

#Je n'arrive pas a récupéré le é de enregistré, la page tmp semble avoir un encodage bizarre
cat tmp | grep -o "Le fichier .* est bien enregistr"


if [ $? -ne "0" ]; then #Si la derniere commande n'a pas réussie ...
    rm tmp cookie
    echo "Erreur dans l'upload du fichier. Vérifiez ce que vous faites, et que le TP que vous essayé de rendre est bien ouvert !"
    exit 1
fi

rm tmp cookie
exit 0

    



