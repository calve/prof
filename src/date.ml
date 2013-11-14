(*
 * A simple date type
 *)

(*
 * Date is simply (year*month*day*hour*minute)
 *)
type t = DATE of int*int*int*int*int

let date year month day hour minute =
  DATE (year,month,day,hour,minute)

let string t = 
  match t with
  DATE (year,month,day,hour,minute) -> 
    (string_of_int day) ^ "/" ^
      (string_of_int month) ^ "/" ^
      (string_of_int year) ^ "-" ^
      (string_of_int hour) ^ ":" ^
      (string_of_int minute)
