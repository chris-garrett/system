vim.cmd("set expandtab")
vim.cmd("set tabstop=2")
vim.cmd("set softtabstop=2")
vim.cmd("set shiftwidth=2")
vim.cmd("set nowrap")
vim.cmd("set mouse=")
vim.g.mapleader = " "
vim.g.background = "light"

vim.opt.swapfile = false

-- Navigate vim panes better
vim.keymap.set('n', '<c-k>', ':wincmd k<CR>')
vim.keymap.set('n', '<c-j>', ':wincmd j<CR>')
vim.keymap.set('n', '<c-h>', ':wincmd h<CR>')
vim.keymap.set('n', '<c-l>', ':wincmd l<CR>')

vim.keymap.set('n', '<leader>h', ':nohlsearch<CR>')
vim.wo.number = true

vim.opt.clipboard:append { 'unnamed', 'unnamedplus' }

-- Function to toggle mouse setting between `mouse=` and `mouse=a`
local function toggle_mouse()
  if vim.o.mouse == 'a' then
    --vim.o.mouse = ''
    vim.cmd("set mouse=")
    print("Mouse disabled")
  else
    --vim.o.mouse = 'a'
    vim.cmd("set mouse=a")
    print("Mouse enabled")
  end
end

-- Map <leader>m to toggle the mouse setting
vim.keymap.set('n', '<leader>m', toggle_mouse)
