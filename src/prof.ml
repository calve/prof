let rec print_ue_list list =
  match list with
  | [] -> ()
  | h::_ -> ( 
    Printf.printf "%d : %s\n" (fst h )(snd h);
    print_ue_list (List.tl list);
  )

let ask_password s =
  print_string s;
  flush stdout;

  (* On demande au shell de ne pas répéter les charactères entrés par l'utilisateur *)
  let exit_code = Sys.command "stty -echo" in
  if (exit_code <> 0) then
    failwith "Ask_password error with stty";

  let tmp = input_line stdin in

  (* On réactive l'echo *)
  let exit_code = Sys.command "stty echo" in
  if (exit_code <> 0) then
    failwith "Ask_password error with stty"
  else
    tmp



let ask s = 
  print_string s;
  flush stdout;
  input_line stdin
    
let _ =
  
  begin
    try
      let login = ask "login ? " in
      let password = ask_password "password (hidden input) ? " in
      let c = Connection.init_connection () in
      Connection.log c login password;
      let ue_list = Connection.get_UE_list c in
      print_ue_list ue_list;
    with
    | Curl.CurlException (reason, code, str) ->
      Printf.printf "Error: %s\n" str
    | Failure s ->
      Printf.printf "Caught exception: %s\n" s
  end;
  Curl.global_cleanup ()
