import react from "@vitejs/plugin-react-swc"
import { join } from "path"
import { defineConfig, searchForWorkspaceRoot } from "vite"
import CodeBattles from "vite-plugin-code-battles"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), CodeBattles()],
  resolve: {
    dedupe: ["react", "react-dom"],
  },
  server: {
    fs: {
      allow: [
        searchForWorkspaceRoot(process.cwd()),
        searchForWorkspaceRoot(join(process.cwd(), "..", "code-battles")),
      ],
    },
  },
})
