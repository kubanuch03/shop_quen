server {
    listen 195.38.164.47:85;
    server_name queen-shops.com www.queen-shops.com;

    root /var/www/queen/dist;
    index index.html;
        access_log  /var/log/nginx/access_queen.log;
        error_log  /var/log/nginx/error_queen.log;

    location / {
        try_files $uri /index.html;
    }
    #location / {
    #    proxy_pass http://195.38.164.47:85;
    #    proxy_set_header Host $host;
    #    proxy_set_header X-Real-IP $remote_addr;
    #    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    #    proxy_set_header X-Forwarded-Proto $scheme;
    #    proxy_buffering off;

    #}
}
