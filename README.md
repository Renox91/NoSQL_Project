# NoSQLProject

## Lancement du projet

```bash
git clone https://github.com/SamirPS/DockerProject.git
cd NoSQL_Project
docker-compose up --build
```

## Structure du projet

Ce projet utilise le langage Python3 avec le framework Flask.

3 Base de données NoSQL sont utilisés :

- **mongodb** : Sert à stocker les comptes utilisateurs
- **postgresql** : Sert à stocker les scores des différents utilisateurs sur les différents jeux
- **redis** : Simple usage pour savoir le nombre de fois que le site à été visité 


## Persistances des volumes

Connecting to the **postgresql** database :
```bash
docker exec -it db bash
root@05b3a3471f6f:/#  psql -U postgres
```
Connecting to the **redis** database :
```bash
docker exec -it redis redis-cli
```

Connecting to the **MongoDB** database :
```bash
docker exec -it mongodb mongo
```


