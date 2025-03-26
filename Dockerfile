FROM paulgauthier/aider-full

USER root

# install some tools
RUN apt update && apt install -y git curl wget npm php-cli jq gh sudo

# add suders
RUN echo "appuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER appuser
