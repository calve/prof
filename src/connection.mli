(* init_connection renvoie un objet de type (Curl.t * Buffer.t) représentant une connexion a Curl et un buffer pour y écrire la page
*)
val init_connection : unit -> (Curl.t * Buffer.t)

(* log loggin password demarre une session avec l'utilisateur loggin et le mot de passe password 
 * @return "Incorrect Login/Password" si le code de réponse de la page de loginn est différent de 302, et donc que la connection n'as pas réussi
 *)
val log : (Curl.t * Buffer.t) -> string -> string -> unit

(* getUElist renvoie la liste des (id,intitulés) des unités d'enseignement trouvées
 * getUElist assume que l'utilisateur soit loggé
 * @return liste des (id,intitulés)
 *)
val get_UE_list : (Curl.t * Buffer.t) -> (int * string) list
