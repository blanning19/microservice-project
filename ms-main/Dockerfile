FROM python:3.11

# set a directory for the app
WORKDIR /usr/src/main

# copy all the files to the container
COPY . .

# install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 6000

# run the command
# CMD ["python3", "./app.py"]

# --- Enable SSH (minimal) ---
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssh-server && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/run/sshd

# Create a simple dev user (change name if you want)
ARG DEV_USER=dev
RUN useradd -m -s /bin/bash ${DEV_USER} && echo "${DEV_USER}:${DEV_USER}" | chpasswd

# Allow password login (quick + simple). For better security, switch to keys later.
RUN sed -ri 's/^#?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -ri 's/^#?PubkeyAuthentication .*/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    sed -ri 's/^#?PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config

# Wrapper to start sshd + your original app command
# (No need to change your code—just set APP_CMD in compose.)
COPY docker/start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

EXPOSE 22
CMD ["/usr/local/bin/start.sh"]