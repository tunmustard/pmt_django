FROM ubuntu:16.04


RUN apt-get update
RUN apt-get install --no-install-recommends -y apt-utils software-properties-common curl nano unzip openssh-server
RUN apt-get install -y python3 python3-dev python-distribute python3-pip git

# main python packages
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade numpy scipy matplotlib scikit-learn pandas seaborn plotly jupyter statsmodels
RUN pip3 install --upgrade nose tqdm pydot pydotplus watermark geopy joblib

# Jupyter configs
RUN jupyter notebook --allow-root --generate-config -y
RUN echo "c.NotebookApp.password = ''" >> ~/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py
RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension

# TensorFlow 
RUN pip3 install --upgrade tensorflow  

# Keras with TensorFlow backend
RUN pip3 install --upgrade keras

# Graphviz, visualizing trees
RUN apt-get -y install graphviz 

# boost
RUN apt-get -y install libboost-program-options-dev zlib1g-dev libboost-python-dev

RUN apt-get update

# JDK --fix-missing
RUN apt-get -y  install openjdk-8-jdk
ENV CPLUS_INCLUDE_PATH=/usr/lib/jvm/java-8-openjdk-amd64/include/linux:/usr/lib/jvm/java-1.8.0-openjdk-amd64/include

RUN apt-get -y install cmake 

# LightGBM
RUN cd /usr/local/src && git clone --recursive --depth 1 https://github.com/Microsoft/LightGBM && \
    cd LightGBM && mkdir build && cd build && cmake .. && make -j $(nproc) 

# LightGBM python wrapper
RUN cd /usr/local/src/LightGBM/python-package && python3 setup.py install 

# CatBoost
RUN pip3 install --upgrade catboost

# PyTorch
RUN pip3 install http://download.pytorch.org/whl/cpu/torch-0.4.0-cp35-cp35m-linux_x86_64.whl 
RUN pip3 install --upgrade torchvision

# Facebook Prophet
RUN pip3 install --upgrade pystan cython
RUN pip3 install --upgrade fbprophet

RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip 
#Optional packages for opencv
RUN apt-get install -y --fix-missing \
	python-dev \
	python-numpy \
	libtbb2 \
	libtbb-dev \
	libjpeg-dev \
	libpng-dev \
	libtiff-dev \
	libjasper-dev \
	libdc1394-22-dev
#Optional packages for opencv
RUN apt-get install -y --fix-missing gcc \
	g++ \
	gtk2.0 \
	libv4l-dev \
	ffmpeg \
	gstreamer1.0-plugins-base
#Optional packages for opencv -update latest version , not needed

#Clean
RUN apt-get clean && rm -rf /tmp/* /var/tmp/*

#installing dlib
#RUN cd ~ && \
#    mkdir -p dlib && \
#    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
#    cd  dlib/ && \
#    python3 setup.py install --yes USE_AVX_INSTRUCTIONS ##DISABLE AVX INSTRUCTION FOR MY UBUNTU LAPTOP


#COPY . /root/face_recognition
#RUN cd /root/face_recognition && \
#    pip3 install -r requirements.txt && \
#    python3 setup.py install
	

#RUN cd ~/opencv/build && \
#	make
#------------------------------------

#installing opencv-python
#RUN cd ~ && \
#	git clone https://github.com/opencv/opencv.git && \
#	cd ~/opencv && \
#	mkdir build && \
#	cd build && \
#	cmake -D WITH_1394=OFF ../
#	
#	#cmake ../ ### <-original line
	

#RUN cd ~/opencv/build && \
#	make && \
#	make install

###Installing Flask
RUN pip install flask	

#Installing Django
RUN pip install Django

	
COPY docker_files/entry-point.sh /

# Final setup: directories, permissions, ssh login, symlinks, etc
RUN mkdir -p /home/user && \
    mkdir -p /var/run/sshd && \
    echo 'root:12345' | chpasswd && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \
    chmod a+x /entry-point.sh

WORKDIR /home/user
EXPOSE 22 4545

ENTRYPOINT ["/entry-point.sh"]
CMD ["shell"]
