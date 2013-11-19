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

(*
 * Compare two dates
 * usage : compare date1 date2
 * return 0 if two dates are equals
 * return a positive integer if date1 was before date2
 * return a negative integer else.
 * Compare actually returns the difference in minutes between two dates,
 * but it may not be suitable for it yet, since their is absolutely no
 * control on date validity
 *)
val compare : t -> t -> int
