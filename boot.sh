adduser --disabled-password --gecos '' r
cd /app/
mod_wsgi-express setup-server wsgi.py --port=80 --user r --group r --server-root=/etc/app
chmod a+x /etc/app/handler.wsgi
/etc/app/apachectl start
tail -f /etc/app/error_log
