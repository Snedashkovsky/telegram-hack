FROM python:3.6

ADD ./requirements.txt ./
RUN pip install -r ./requirements.txt

ADD ./blockchains ./blockchains
ADD ./bot ./bot
ADD ./commands ./commands
ADD ./demo ./demo
ADD ./fluence ./fluence
ADD ./rating ./rating
ADD ./config.py ./
ADD ./start.py ./

ENV BOT_TOKEN "765705629:AAH9YsCDdYHWsEWiSlKWPFwFHOijynwOU5A"
ENV MAPS_API_KEY "0d28c99c928f4c1da4433bd10bf94838"
ENV STEEMIT_KEY "5K5DA2kmJqLew5fDcwBaV44BKUGHiHCnefDzVFJvvQ6M9XNGnF2"

CMD python ./start.py --process_name demo && python ./start.py --process_name bot