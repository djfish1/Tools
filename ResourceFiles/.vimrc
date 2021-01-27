syntax on
filetype on
filetype plugin on
filetype indent on
set smarttab
set expandtab
set cindent
set autoindent
set tabstop=2
set shiftwidth=2
set softtabstop=2

set smartcase
set hlsearch
set history=50

set showcmd
set laststatus=2
set statusline=%<%t\ %m%r%=l:%l/%L\ c:%c

set textwidth=0
set nowrap

set tags=./tags,./../tags,./../../tags,./../../../tags,./../../../../tags,./../../../../../tags,./../../../../../../tags

" Always pull up the menu to select the actual tag you want.
nmap  g

set diffopt+=vertical
autocmd FileType python setlocal expandtab shiftwidth=2 softtabstop=2 tabstop=2
