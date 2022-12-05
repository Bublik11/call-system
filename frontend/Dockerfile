# для раздачи статических файлов используем nginx
FROM nginx:mainline

LABEL maintainer="IVAN BUBLIK <https://github.com/Bublik11>"
# удаляем дефолтную страницу nginx
RUN rm -rf /usr/share/nginx/html/*
# копируем файлы
COPY . /usr/share/nginx/html
# выполняем настройку запуска
CMD ["nginx", "-g", "daemon off;"]