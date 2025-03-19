create table if not exists battle (
    id serial primary key,
    created_at timestamp not null default now(),
    end_date timestamp null,
    pokemon_1 varchar(150) not null,
    pokemon_2 varchar(150) not null,
    winner varchar(150) null,
    initial_hp_1 int not null,
    initial_hp_2 int not null
);

create table if not exists attack(
    id serial primary key,
    battle_id int not null,
    pokemon_1_hp int not null,
    pokemon_2_hp int not null,
    attacker varchar(150) not null,
    attack_damage int not null,
    defense_damage int not null,
    attack_move varchar(150) not null,
    defense_move varchar(150) not null,
    created_at timestamp not null default now()
);