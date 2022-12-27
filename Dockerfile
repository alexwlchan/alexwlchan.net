FROM greengloves/alexwlchan.net:28

COPY ./scripts/install_pillow.sh .
RUN ./install_pillow.sh

ENTRYPOINT ["bundle", "exec", "jekyll"]
