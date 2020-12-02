# NoSQLProject

## Lancement du projet

```bash
git clone https://github.com/Renox91/NoSQL_Project
cd NoSQL_Project
docker-compose up --build
```

## Structure du projet

Ce projet utilise le langage Python3 avec le framework Flask.

3 Base de données NoSQL sont utilisés :

- **mongodb** : Sert à stocker les comptes utilisateurs

- **postgresql** : Sert à stocker les scores des différents utilisateurs sur les différents jeux

```sql
id serial NOT NULL,
game text NOT NULL,
username text NOT NULL,
score integer NOT NULL,
date_score date NOT NULL
```

- **redis** : Simple usage pour savoir le nombre de fois que le site à été visité 

## Persistances des volumes

Pour se connecter aux différentes base de données :

### mongodb
```bash
docker exec -it mongodb mongo 
```

### postgresql
```bash
docker exec -it postgre bash
psql -U postgre
```

### redis
```bash
docker exec -it redis redis-cli
```