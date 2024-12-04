# Check for and Install homebrew if missing
which -s brew
if [[ $? != 0 ]] ; then
    # Install Homebrew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    brew update
fi

# Install redis and configure it as a service (auto-start on boot)
brew install redis
brew services start redis

# Install python and initialize a virtual environment
brew install python
python3 -m venv ./venv
source ./venv/bin/activate

# Install and upgrade pip
python3 -m ensurepip --upgrade pip
python3 -m pip install --upgrade pip

#Install python dependencies
python3 -m pip install flask
python3 -m pip install flask_bootstrap
python3 -m pip install turbo_flask
python3 -m pip install gunicorn
python3 -m pip install "redis[hiredis]"