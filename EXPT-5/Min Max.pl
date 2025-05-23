:- initialization(main).

min(X, Y, X) :- X =< Y.
min(X, Y, Y) :- X > Y.

max(X, Y, X) :- X >= Y.
max(X, Y, Y) :- X < Y.

main :-
    min(3, 5, Min),
    write('Minimum of 3 and 5 is: '),
    write(Min), nl,

    max(3, 5, Max),
    write('Maximum of 3 and 5 is: '),
    write(Max), nl.
