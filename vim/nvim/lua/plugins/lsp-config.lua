return {
  -- package manager for lsps, daps, linters and formatters
  {
    "williamboman/mason.nvim",
    lazy = false,
    config = function()
      require("mason").setup()
    end,
  },
  -- reduces boilerplate. you dont have to do this for each lsp:
  -- require("lspconfig")[server].setup({})
  {
    "williamboman/mason-lspconfig.nvim",
    lazy = false,
    opts = {
      auto_install = true,
    },
  },
  {
    "neovim/nvim-lspconfig",
    lazy = false,
    dependencies = {
      "hrsh7th/cmp-nvim-lsp",
      "williamboman/mason-lspconfig",
      { "antosha417/nvim-lsp-file-operations", config = true },
    },
    config = function()
      require("mason-lspconfig").setup({
        automatic_installation = true,
      })

      local capabilities = require("cmp_nvim_lsp").default_capabilities()

      local lspconfig = require("lspconfig")
      lspconfig.ts_ls.setup({
        root_dir = lspconfig.util.root_pattern("package.json"),
        capabilities = capabilities,
      })
      lspconfig.html.setup({
        capabilities = capabilities,
      })
      lspconfig.lua_ls.setup({
        capabilities = capabilities,
      })
      lspconfig.pylsp.setup({
        capabilities = capabilities,
      })
      --lspconfig.denols.setup({
      --  capabilities = capabilities,
      --})

     -- show get popup
      vim.keymap.set("n", "K", vim.lsp.buf.hover, {})
      -- show get definition
      vim.keymap.set("n", "<leader>gd", vim.lsp.buf.definition, {})
      -- show get references
      vim.keymap.set("n", "<leader>gr", vim.lsp.buf.references, {})
      -- show code actions
      vim.keymap.set("n", "<leader>ca", vim.lsp.buf.code_action, {})
      -- show code error popup
      vim.keymap.set("n", "<leader>ce", vim.diagnostic.open_float, {})
      -- rename symbol
      vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, {})
    end,
  },
}
