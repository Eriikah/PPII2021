**Architecture de la base de données**

# Tables pour les objectifs importants
## table user:

 * **user_id**(int)
 * password_hash(varchar) 
 * surname(varchar)
 * name(varchar)
 * email(varchar)
 * rôle(varchar)
 * statut(varchar)


## table proposition:

 * **prop_id**(int)
 * _poster_id_(int)
 * content(text)
 * title(varchar)
 * vote_pos(int)
 * vote_neg(int)
 * post_time(timestamp)
 * deadline(timestamp)
 * tags(varchar)(avec un max de 3 tags)

## table vote:

 * **vote_id**(int)
 * vote_on(varchar)
 * _parent_id_(int)
 * user_id(int)
 * vote_time(timestamp)


# Tables pour les fonctionnalitées annexes

## table commentaire:

 * **comment_id**(int)
 * _prop_id_(int)
 * _poster_id_(int)
 * content(text)
 * post_time(timestamp)
 * moderated([0,1,-1]) #0=pas modéré, 1=modéré accepté, -1 modéré pas accepté
 * like(int)
 * dislike(int)

## table enquête:

 * **survey_id**(int)
 * title(varchar)
 * description(text)
 * post_time(timestamp)
 * deadline(timestamp)

## table questions:

 * **question_id**(int)
 * _survey_id_(int)
 * question_nb(int)
 * content(varchar)


## table answer:

 * **answ_id**(int)
 * _question_id_(int)
 * content(text)
 * time(timestamp)


## Table annuaire:

 * **service_id**(int)
 * nom (varchar)
 * adresse (varchar)
 * telephone(varchar)
