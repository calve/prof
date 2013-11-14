type t

(*
 * Make a new date using year month day hour minute
 * Absolutely no control is made at all at the moment
 * date year month day hour minute
 *)
val date : int -> int -> int -> int -> int -> t


(*
 * Return a string representing the date
 *)
val string : t -> string
