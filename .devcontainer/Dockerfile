# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.233.0/containers/codespaces-linux/.devcontainer/base.Dockerfile

FROM mcr.microsoft.com/vscode/devcontainers/universal:linux

# ** [Optional] Uncomment this section to install additional packages. **
# USER root
#
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

USER codespace

# [Required] Poetry
RUN curl -sSL https://install.python-poetry.org | python - -y
RUN poetry config virtualenvs.in-project true

# [Required] Gitmoji CLI
# Deprecated: Maybe removed once nonemoji is done
RUN yarn global add gitmoji-cli
ENV PATH="$PATH:/home/codespace/.yarn/bin"
