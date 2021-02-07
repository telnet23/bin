#!/bin/bash

set -x

# GNU utilities
brew install coreutils findutils inetutils moreutils gawk gnu-tar

# Additional utilities
# Some are already installed on macOS, but we want the latest versions
brew install curl wget tree rename ripgrep rsync ncdu p7zip git zsh zsh-syntax-highlighting
brew install --cask dosbox electrum google-chrome mactex qgis tor-browser vmware-fusion

# Programming
brew install perl cpanminus python pyenv-virtualenv swi-prolog gnu-apl
brew install --cask macvim
pip install pygments  # Required by LaTeX package "minted"

# Audiovisual
brew install ffmpeg imagemagick exiftool
brew install --cask audacity gimp vlc

VIM=~/.vim/pack/git-plugins/start
mkdir -p "$VIM"

cpanm Perl::Critic
brew install flake8 pylint shellcheck
(cd "$VIM" && git clone --depth 1 git@github.com:dense-analysis/ale.git)

brew install cmake
(cd "$VIM" && git clone --depth 1 git@github.com:ycm-core/YouCompleteMe.git)
(cd "$VIM/YouCompleteMe" && python install.py --clangd-completer)

(cd "$VIM" && git clone --depth 1 git@github.com:altercation/vim-colors-solarized.git)
(cd "$VIM" && git clone --depth 1 git@github.com:mhinz/vim-signify.git)

defaults write com.apple.dock ResetLaunchPad true
defaults write com.apple.finder CreateDesktop false
defaults write com.apple.desktopservices DSDontWriteNetworkStores true

killall Dock
killall Finder
