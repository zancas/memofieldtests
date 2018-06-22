FROM       ubuntu:18.04
RUN        apt-get update && apt-get install -y build-essential pkg-config \
           libc6-dev m4 g++-multilib autoconf libtool ncurses-dev unzip git \
           python python-zmq zlib1g-dev wget curl bsdmainutils automake
RUN        useradd --home-dir /home/zcasher zcasher
RUN        mkdir -p /home/zcasher && chown zcasher:zcasher /home/zcasher
USER       zcasher
RUN        mkdir -p /home/zcasher/.zcash && \
           echo "addnode=testnet.z.cash" > /home/zcasher/.zcash/zcash.conf && \
           echo "testnet=1" >> /home/zcasher/.zcash/zcash.conf
RUN        cd /home/zcasher && \
           git clone -b v1.1.0 https://github.com/zcash/zcash.git
RUN        cd /home/zcasher/zcash && \
           ./zcutil/fetch-params.sh --testnet && \
           ./zcutil/build.sh -j$(nproc)
