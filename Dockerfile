FROM miaos_server_env:v0.1

ADD miaos-core/ /root/miaos-core/
ADD miaos-interface/ /root/miaos-interface/

WORKDIR /root/

ENTRYPOINT [ "/usr/local/bin/python" ]
CMD [ "procman.py" ]