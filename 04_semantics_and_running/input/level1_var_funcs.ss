scalar ss = 3.0

subroutine Fu[] is
  print_scalar !In Func! 0.0
end

sheet DATA = {
  1.0, 2.0, 3.0, 0.0 ... Last column is for storing the sum of previous values ...
  2.0, 4.0, 8.0, 0.0
  3.0, 6.0, 9.0, 0.0
}

range _aa

... These should fail
scalar ss = 4.0

function Fu[] return scalar is
  return 0.0
end ...

... These should work (after removing double definitions) ...
Fu[]
ss := 4.0
print_scalar ss
Fu[]

_aa := range DATA'A1..DATA'A2

... These should give an error (remove the other line to test just one of these) ...
... print_scalar tt ... ... Undefined variable ...
... Gu[] ... ... Undefined subroutine ...
