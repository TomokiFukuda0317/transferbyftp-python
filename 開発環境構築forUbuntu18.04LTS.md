sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install git
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
vi ~/.bashrc
    export PYENV_ROOT=$HOME/.pyenv
    export PATH=${PYENV_ROOT}/bin:$PATH
    eval "$(pyenv init -)"

sudo apt-get install libssl-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev

sudo apt-get install zlib1g-dev
sudo apt-get install libffi-dev

pyenv install -v 3.7.4
pyenv global 3.7.4

python --version

https://qiita.com/rh_/items/ce6e59d798204f3ee281