let login = "debusschere";;
let baseURL = "https://prof.fil.univ-lille1.fr/";;
let cookieFilePath = "cookie";;
  
(*
 * ocurl.ml
 *
 * Copyright (c) 2003-2008, Lars Nilsson, <lars@quantumchamaleon.com>
 *)

(**
   * Write some datas
   * Buffer.t -> string -> int
*)
let writer accum data =
  Buffer.add_string accum data;
  String.length data
    
(**
   * Show some datas as string
*)
let showContent content =
  Printf.printf "%s" (Buffer.contents content);
  flush stdout
    
let showInfo connection =
  Printf.printf "Time: %f\nURL: %s\nResponse: %d"
    (Curl.get_totaltime connection)
    (Curl.get_effectiveurl connection)
    (Curl.get_responsecode connection)
    
let getContent connection url =
  Curl.set_url connection url;
  Curl.perform connection

let init_connection () =
  Curl.global_init Curl.CURLINIT_GLOBALALL;
  
  let result = Buffer.create 16384 in
  let connection = Curl.init() in
  Curl.set_writefunction connection (writer result);
  (connection,result)
;;

    
(* Get a page
 * Get ressources specified at url using connection, putting output in result
 *)
let fetch connection url  =
  Curl.set_url connection url;
  Curl.perform connection

(* fetch cookies
* We need to get the cookies before doing anything ....
*)
let getCookies () =
  let connection = fst (init_connection ()) in
  Curl.set_cookiejar connection cookieFilePath;
  fetch connection (baseURL^"index.php");
;;

(*
* Log l'utilisateur
*)  
let log login password =
  getCookies();

  let c = (init_connection ()) in
  let connection = fst c in

  (* On spécifie le cookie *)
  Curl.set_cookiefile connection cookieFilePath;
  Curl.set_post connection true;

  (* On crée la liste de ce qu'on passera par FORM *)
  let loginOption = Curl.CURLFORM_CONTENT("login",login,Curl.CONTENTTYPE "text/html") in
  let passwdOption = Curl.CURLFORM_CONTENT("passwd",password,Curl.CONTENTTYPE "text/html") in (** TODO -- encoder l'url*)
  let validerOption = Curl.CURLFORM_CONTENT("++O+K++","Valider",Curl.CONTENTTYPE "text/html") in

  (* On donne tout a manger à Curl *)
  Curl.set_httppost connection [loginOption;passwdOption;validerOption];
  
  fetch connection (baseURL^"login.php");
  if Curl.get_responsecode connection != 302 then
    failwith "Incorrect Login/Password";
;;



let _ =
  
  begin
    try
      log "login" "password";
    with
    | Curl.CurlException (reason, code, str) ->
      Printf.printf "Error: %s\n" str
    | Failure s ->
      Printf.printf "Caught exception: %s\n" s
  end;
  Curl.global_cleanup ()



    
    
    
