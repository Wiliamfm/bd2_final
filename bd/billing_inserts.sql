insert into bill_state
values (1, 'nueva');

insert into bill_state
values (2, 'en preparacion');

insert into bill_state
values (3, 'enviada');

insert into general_bill
values (1, now(), 'address example', 10000);

insert into bill
values(1, 1, 1, 1, 1);

insert into bill
values(2, 1, 1, 2, 1);

insert into bill
values(3, 1, 1, 3, 1);

insert into general_bill
values (2, now(), 'address example', 20000);

insert into bill
values(4, 2, 1, 2, 1);

insert into bill
values(5, 2, 1, 2, 1);