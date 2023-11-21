#!/bin/sh

# Use this script to install any other tool that can't easily be installed via the execution-environment.yml file.

# Install Internet Archive Downloader
IA_APPDIR="/opt/ia"
IA_GITHUB_URL="https://github.com/john-corcoran/internetarchive-downloader"

git clone $IA_GITHUB_URL $IA_APPDIR
pip3 install -r $IA_APPDIR/requirements.txt
cat > /usr/bin/ia <<EOF
#!/bin/sh
$IA_APPDIR/bin/python $IA_APPDIR/ia_downloader.py "$@"
EOF
chmod +x /usr/bin/ia