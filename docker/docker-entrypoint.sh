#!/bin/sh

# Run the container the default way

if [ "$1" = 'sketch' ]; then
  # Set SECRET_KEY in /etc/sketch.conf if it isn't already set
  if grep -q "SECRET_KEY = '<KEY_GOES_HERE>'" /etc/sketch.conf; then
    OPENSSL_RAND=$( openssl rand -base64 32 )
    # Using the pound sign as a delimiter to avoid problems with / being output from openssl
    sed -i 's#SECRET_KEY = \x27\x3CKEY_GOES_HERE\x3E\x27#SECRET_KEY = \x27'$OPENSSL_RAND'\x27#' /etc/sketch.conf
  fi

  # Set up the Postgres connection
  if [ $POSTGRES_USER ] && [ $POSTGRES_PASSWORD ] && [ $POSTGRES_ADDRESS ] && [ $POSTGRES_PORT ]; then
    sed -i 's#postgresql://<USERNAME>:<PASSWORD>@localhost#postgresql://'$POSTGRES_USER':'$POSTGRES_PASSWORD'@'$POSTGRES_ADDRESS':'$POSTGRES_PORT'#' /etc/timesketch.conf
  else
    # Log an error since we need the above-listed environment variables
    echo "Please pass values for the POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_ADDRESS, and POSTGRES_PORT environment variables"
    exit 1
  fi

  # Set up web credentials
  if [ -z ${SKETCH_USER+x} ]; then
    SKETCH_USER="admin"
    echo "SKETCH_USER set to default: ${SKETCH_USER}";
  fi
  if [ -z ${SKETCH_PASSWORD+x} ]; then
    SKETCH_PASSWORD="$(openssl rand -base64 32)"
    echo "SKETCH_PASSWORD set randomly to: ${SKETCH_PASSWORD}";
  fi

  # Sleep to allow the other processes to start
  sleep 5
  sktctl add_user -u "$SKETCH_USER" -p "$SKETCH_PASSWORD"

  # Run the Sketch server (without SSL)
  uwsgi --ini uwsgi.ini
fi

# Run a custom command on container start
exec "$@"
