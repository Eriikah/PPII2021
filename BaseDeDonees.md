Architecture de la base de données

table user:
user_id(int)
password_hash(varchar) 
name(varchar)
email(varchar)
rôle(varchar)
statut(varchar)
mod_status(int)

table proposition:
prop_id(int)
#poster_id(int)
content(text)
title(varchar<128)
vote_pos(int)
vote_neg(int)
post_time(timestamp)
deadline(timestamp)
tags(varchar)(avec un max de 3 tags)

table vote:
vote_id(int)
vote_on(varchar)
#parent_id(int)
user_id(int)
vote_time(timestamp)

table commentaire:
comment_id(int)
#prop_id(int)
#poster_id(int)
content(text)
post_time(timestamp)
moderated([0,1,-1]) #0=pas modéré, 1=modéré accepté, -1 modéré pas accepté
like(int)
dislike(int)


table enquête:
survey_id(int)
title(varchar)
description(text)
post_time(timestamp)
deadline(timestamp)

table questions:
question_id(int)
#survey_id(int)
question_nb(int)
content(varchar)

table answer:
answ_id(int)
#question_id(int)
content(text)
time(timestamp)

Table annuaire
service_id(int)
nom (varchar)
adresse (varchar)
telephone(varchar)

