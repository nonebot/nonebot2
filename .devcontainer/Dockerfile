# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/main/containers/codespaces-linux/
FROM mcr.microsoft.com/vscode/devcontainers/universal:linux

# [Required] Poetry
RUN su vscode -c "curl -sSL https://install.python-poetry.org | python3 - -y"

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && yarn global add gitmoji-cli" 2>&1
