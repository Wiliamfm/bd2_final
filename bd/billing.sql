create table bill_state(
  id serial primary key,
  state varchar(20) unique not null
);

create table general_bill(
  id serial primary key,
  create_date timestamp not null,
  address varchar(100) not null,
  total decimal not null
);

create table bill(
  id serial primary key,
  general_bill integer references general_bill (id),
  client_id integer not null,
  product_id integer not null,
  bill_state integer references bill_state (id) on delete set null
);