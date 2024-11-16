(*zadatak 1 a*)
Require Import Bool.

Notation " ! b " := (negb b) (at level 0).

Goal forall x y : bool,
  (x && !y) || (!x && !y) || (!x && y) = !x || !y.
Proof.
  destruct x, y; reflexivity.
Qed.

(*zadatak 1 b*)
Goal forall x y z : bool,
  (!(!x && y && z)) && (!(x && y && !z)) && (x && !y && z) = x && !y && z.
Proof.
  destruct x, y, z; reflexivity.
Qed.