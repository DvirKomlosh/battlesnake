import { execSync } from "child_process"
import { existsSync, readdirSync, readFileSync, writeFileSync } from "fs"
import { join } from "path"

export default function codeBattles() {
  return {
    name: "code-battles",
    buildStart: () => {
      const directory = join("public", "scripts")
      const file = join("public", "config.json")
      let config: any = {}
      if (existsSync(file)) {
        config = JSON.parse(readFileSync(file).toString())
      }
      config.files = {}
      const files = readdirSync(directory, { recursive: true })
      for (const file of files) {
        if (file.includes("__pycache__") || !file.toString().endsWith(".py")) {
          continue
        }

        config.files["/scripts/" + file] = "./" + file
      }
      writeFileSync(file, JSON.stringify(config, null, 4))
      console.log(`✨ Refreshed config.json to include all Python files`)
    },
  }
}
