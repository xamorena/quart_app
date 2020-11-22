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
hypercorn -w 4 quart_app.application:application
```

