cat > /etc/apache2/mods-available/mpm_prefork.conf << EOF
# prefork MPM
# StartServers: number of server processes to start
# MinSpareServers: minimum number of server processes which are kept spare
# MaxSpareServers: maximum number of server processes which are kept spare
# MaxRequestWorkers: maximum number of server processes allowed to start
# MaxConnectionsPerChild: maximum number of requests a server process serves

<IfModule mpm_prefork_module>
        StartServers                     10
        MinSpareServers           10
        MaxSpareServers          20
        MaxRequestWorkers         1500
        MaxConnectionsPerChild   10000
</IfModule>
EOF

adduser --disabled-password --gecos '' r
cd /app/
mod_wsgi-express setup-server wsgi.py --port=80 --user r --group r --server-root=/etc/app --socket-timeout=600 --limit-request-body=524288000
chmod a+x /etc/app/handler.wsgi
/etc/app/apachectl start
tail -f /etc/app/error_log
