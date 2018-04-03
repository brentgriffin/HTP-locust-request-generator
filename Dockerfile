FROM python:3.6.5-alpine3.7

LABEL com.dotcms.contact "griffin.brent@gmail.com"
LABEL com.dotcms.vendor "https://hightechprofessional.com/"
LABEL com.dotcms.description "dotCMS Base CMS"

ENV HOST http://localhost
ENV PORT 8080
ENV CLIENT_THREADS 10

WORKDIR /script

RUN pip install bs4 && pip install requests

COPY createScript.py createScript.py
COPY sharedfuncs.py sharedfuncs.py

#CMD python3 /script/createScript.py ${HOST}:${PORT} ${CLIENT_THREADS}
CMD python3 /script/createScript.py ${HOST} ${CLIENT_THREADS}
