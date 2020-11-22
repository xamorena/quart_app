# Quart Application "quart_app"

Web Application based on Quart

# Usage:

```
export QUART_APP=quart_app.application:application
quart init_db
quart run
```

With hypercorn:

```
hypercorn -b 0.0.0.0:5000 -w 1 quart_app.application:application
```
