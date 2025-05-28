FROM python:3.8  
ENV PYTHONBUFFERED=1 
WORKDIR /app 


COPY requirments.txt /app/requirments.txt  
    
RUN pip install -r requirments.txt 

COPY . /app
#RUN python manage.py makemigrations Domain
RUN python manage.py migrate --run-syncdb 

EXPOSE 8000

CMD python3 manage.py runserver 0.0.0.0:8000