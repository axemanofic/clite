import DefaultTheme from "vitepress/theme";
import "@catppuccin/vitepress/theme/mocha/mauve.css";
import Editor from 'vitepress-python-editor'

/** @type {import('vitepress').Theme} */
export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('Editor', Editor)
  },
}
