## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

#### Notes sur l'éxecution de l'application en local :
L'application nécéssite les variables d'environnement suivantes:

- SECRET_KEY=[djando_secret_key]
- DEBUG=(true ou false)
- SENTRY_DSN=[sentry_dsn] (Client Keys DSN dans les paramètres du projet Sentry)

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`


# Déploiement

Le déploiement en production nécéssite les outils suivants :

- GitHub
- Docker et DockerHub
- CircleCi
- Heroku
- Sentry

La création d'un compte sera nécessaire pour chacun de ces outils.



### Fonctionnement global du pipeline

- Le projet est configuré pour que les modifications faites sur la branche master déclenchent la mise en production de l'application si aucune erreur de linting n'est détectée et que tous les tests unitaires ont réussi.
- Lors d'un push sur la branche master, un build sera lancé dans CircleCi. Il se fera à travers 3 étapes :
  - d'abord les tests unitaires et le linting,
  - puis la création d'une image Docker et son envoi sur le registry DockerHub,
  - et enfin le déploiement de cette image sur Heroku.
- Chacune de ces étapes dépend du succès de la précédente.
- Seule la branche master est concernée. Les autres branches ne déclenchent que l'étape 1 (tests et linting).


## Configuration CircleCi

Lien vers le projet : https://app.circleci.com/pipelines/github/CedPi/Python-OC-Lettings-FR

Les variables d'environnement nécessaires au bon fonctionnement du projet se trouvent dans la section
Projects > Project Settings > Environment Variables

- DOCKER_PWD :	mot de passe Docker
- DOCKER_USR :	login Docker
- HEROKU_API_KEY :	API key Heroku (dans Heroku, aller dans Account Settings)
- HEROKU_APP_NAME : nom de l'application créée dans Heroku
- SECRET_KEY :	secret key de Django
- SENTRY_DSN :	DSN du projet Sentry (dans Sentry, paramètres du projet, Client Keys DSN)


## Docker

Il est nécéssaire d'installer Docker sur son poste pour pouvoir tester l'application conteneurisée localement.

Lancer une image dans un conteneur :
Exécuter la commande "docker run" avec les paramètres suivants:
- "-e" pour injecter une variable
	- variables nécéssaires:
		- PORT
		- DEBUG
		- SECRET_KEY
		- SENTRY_DSN
- "-p" pour la publication du port
- puis le nom/tag de l'image

Exemple:
```bash
docker run -e "PORT=8765" -e "DEBUG=1" -e "SECRET_KEY=my_secret_key" -e "SENTRY_DSN=my_sentry_dsn" -p 8007:8765 cedpi/oc-lettings:944324976d86689b6e63d915eba87787e14f4626
```

Note: les images sont automatiquement taguées avec le “hash”  de commit CircleCI


## Heroku

Lien vers l'application : https://oc-lettings-117.herokuapp.com/

Avant un déploiement:

- s'assurer que l'url de l'application Heroku est bien définie dans la variable "PRODUCTION_APP" (qui est ensuite utilisée dans ALLOWED_HOSTS), dans oc_lettings_site/settings.py
- s'assurer que l'application est créée avec le bon nom (oc-lettings-117), sinon la créer (Dans Heroku : Dashboard > New > Create new app, puis saisir le nom et enregistrer.

Les variables d'environnement sont accessibles dans Dashboard > oc-lettings-117 > Settings > Reveal Config Vars. Il est inutile de les modifier ici car elles sont définies via le fichier de configuration de CircleCi.


## Sentry

Sentry est utilisé pour monitorer les erreurs de l'application.
- Si besoin de recréer un projet, sélectionner Django comme type de projet, puis suivre les indications pour l'intégrer à l'application (nécessite des modifications dans le settings.py - copiez et collez le code fourni par la doc Sentry).
- Pour rappel, le DSN de Sentry peut se retrouver dans les paramètres du projet, puis dans Client Key DSN.
- Une route a été ajoutée dans l'application afin de vérifier si Sentry est correctement configuré.
- En se rendant sur https://oc-lettings-117.herokuapp.com/sentry-debug/, une erreur sera logguée dans Sentry
