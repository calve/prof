(* init_connection renvoie un objet de type (Curl.t * Buffer.t) représentant une connexion a Curl et un buffer pour y écrire la page
*)
val init_connection : unit -> (Curl.t * Buffer.t)

(* log loggin password demarre une session avec l'utilisateur loggin et le mot de passe password 
 * @return "Incorrect Login/Password" si le code de réponse de la page de loginn est différent de 302, et donc que la connection n'as pas réussi
 *)
val log : (Curl.t * Buffer.t) -> string -> string -> unit

(* get_UE_list renvoie la liste des (id,intitulés) des unités d'enseignement trouvées
 * get_UE_list assume que l'utilisateur soit loggé
 * failwith "get_UE_list failed" ssi la page renvoyée ne contient pas une liste d'UE, c'est a dire pas de "VALUE.*OPTION"
 * @return liste des (id,intitulés)
 *)
val get_UE_list : (Curl.t * Buffer.t) -> (int * string) list

(* get_TP_list renvoie la liste des (id,intitulés,etat) des TPs d'une unité d'enseignements
 * get_TP_list assume que l'utilisateur soit loggé
 * @param connection
 * @param id de l'UE visée
 * failwith "get_TP_list failed" ssi la page renvoyée ne contient pas une liste de TP, c'est a dire pas de "echeance.*"
 * @return liste des (id,intitulés,etat). Un etat est vrai si le TP est ouvert au rendu
 *)
val get_TP_list : (Curl.t * Buffer.t) -> int -> (int * string * bool) list

(* upload connection tp_id file
 * Dépose le fichier file sur le tp tp_id en utilisant la connection connection * upload assume que l'utilisateur soit loggé
 * failwith "upload error" ssi la page renvoyée ne contient pas "La fichier .* a bien été envoyé"
 *)
val upload : (Curl.t * Buffer.t) -> int -> string -> unit

(* delete connection tp_id
 * Supprime le fichier associé au tp tp_id sur le serveur de prof
 * failwith "delete error" ssi la page renvoyée ne contient pas "Fichier supprimé"
 *)
val delete : (Curl.t * Buffer.t) -> int -> unit

