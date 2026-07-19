# 1. Navigate to your mobile folder
cd mobile 

# 2. Install buildozer and its dependencies
pip install buildozer
sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libssl-dev cmake

# 3. Initialize buildozer (this creates the buildozer.spec file)
buildozer init

buildozer -v android debug

#or
#buildozer android clean
#buildozer -v android debug deploy run logcat