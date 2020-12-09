FROM python:3.7


RUN python -m pip install --upgrade pip
ENV HOME=/var/www

COPY requirements.txt $HOME/requirements.txt
RUN pip install -r $HOME/requirements.txt

COPY  . .

