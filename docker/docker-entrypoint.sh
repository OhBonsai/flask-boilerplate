#!/bin/sh

# Run the container the default way

if [ "$1" = 'sketch' ]; then
  # Set SECRET_KEY in /etc/sketch.conf if it isn't already set
  if grep -q "SECRET_KEY = '<KEY_GOES_HERE>'" /etc/sketch.conf; then
    OPENSSL_RAND=$( openssl rand -base64 16 )
    # Using the pound sign as a delimiter to avoid problems with / being output from openssl
    sed -i 's#SECRET_KEY = \x27\x3CKEY_GOES_HERE\x3E\x27#SECRET_KEY = "'$OPENSSL_RAND'"#' /etc/sketch.conf
  fi

  # Set up the Postgres connection
  if [ $POSTGRES_USER ] && [ $POSTGRES_PASSWORD ] && [ $POSTGRES_ADDRESS ] && [ $POSTGRES_PORT ]; then
    sed -i 's#postgresql://<USERNAME>:<PASSWORD>@localhost#postgresql://'$POSTGRES_USER':'$POSTGRES_PASSWORD'@'$POSTGRES_ADDRESS':'$POSTGRES_PORT'#' /etc/sketch.conf
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
    SKETCH_PASSWORD="$(openssl rand -base64 16)"
    echo "SKETCH_PASSWORD set randomly to: ${SKETCH_PASSWORD}";
  fi

  # Migrate db
  sktctl migrate init
  sktctl migrate migrate
  sktctl migrate upgrade

  # Sleep to allow the other processes to start
  sleep 5
  sktctl add_user --username "$SKETCH_USER" --password "$SKETCH_PASSWORD"
fi

# Run the Sketch server (without SSL)
exec uwsgi --ini uwsgi.ini
