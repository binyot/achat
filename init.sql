create table if not exists users (
                id integer primary key,
                username varchar(16) unique,
                created_at real
);

create table if not exists chats (
                id integer primary key,
                name varchar(32) unique,
                created_at real
);

create table if not exists user_chat (
                id integer primary key,
                user_id integer,
                chat_id integer,
                foreign key(user_id) references users(id),
                foreign key(chat_id) references chats(id),
                unique(user_id, chat_id)
);

create table if not exists messages (
                id integer primary key,
                author integer,
                chat integer,
                text text,
                created_at real,
                foreign key(chat) references chats(id),
                foreign key(author) references users(id)
);
