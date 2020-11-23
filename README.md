# Quart Application "quart_app"

Web Application based on Quart

## Usage:

```
export QUART_APP=quart_app.application:application
quart init_db
quart run
```

With hypercorn:

```
hypercorn -b 0.0.0.0:5000 -w 1 quart_app.application:application
```

## TODOs

- Add: Create authentication and registration methods
- Add: Update database schemas
- Add: Insert private/public board management
- Fix: Group painter events by user_id
- Fix: Upload dossier
- Fix: workspace/canvas definition
- Fix: horizontal collapse

## Schemas

### Permission:

- id
- access
- action

### Role:

 - id
 - name
 - permissions

### UserRole:

 - role_id
 - user_id

### User:

- id
- name
- email
- title
- firstname
- lastname
- photo_url
- company
- profile
- roles
- boards

### Board:

- id
- name
- owner
- secured
- messages
- dossiers
- painters

### Message:

- id
- from
- text

### Dossier:

- id
- owner
- files

### Painter:

- id
- author
- graphs

### Post:

- id
- user_id
- subject
- created
- authors
- comment
