return {
  -- adds a nice footer with various states
  "nvim-lualine/lualine.nvim",
  config = function()
    require("lualine").setup({
      options = {
        theme = "catppuccin-mocha",
        sections = {
          lualine_a = { {
            "filename",
            path = 2,
          } },
        },
      },
    })
  end,
}
