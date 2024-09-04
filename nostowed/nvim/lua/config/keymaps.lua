-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
--
--
local map = vim.keymap.set
---- Move to window using the <ctrl> arrow keys
map("n", "<C-Up>", "<C-w>h", { desc = "Go to left window", remap = true })
map("n", "<C-Down>", "<C-w>j", { desc = "Go to lower window", remap = true })
map("n", "<C-Left>", "<C-w>k", { desc = "Go to upper window", remap = true })
map("n", "<C-Right>", "<C-w>l", { desc = "Go to right window", remap = true })

-- Resize window using <ctrl> hjkl keys
map("n", "<C-h>", "<cmd>resize +2<cr>", { desc = "Increase window height" })
map("n", "<C-j>", "<cmd>resize -2<cr>", { desc = "Decrease window height" })
map("n", "<C-k>", "<cmd>vertical resize -2<cr>", { desc = "Decrease window width" })
map("n", "<C-l>", "<cmd>vertical resize +2<cr>", { desc = "Increase window width" })

map("n", "<C-d>", "<C-d>zz", { desc = "C-d and center" })

local function retain(m, k, v)
  vim.keymap.set(m, k, v, { silent = true })
end

retain("x", "p", "P")

vim.api.nvim_set_keymap("n", "x", '"_x', { noremap = true })
