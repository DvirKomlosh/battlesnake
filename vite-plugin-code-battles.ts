import { execSync } from "child_process"
import { existsSync, readdirSync, rmSync } from "fs"
import { join } from "path"

export default function codeBattles() {
  return {
    name: "code-battles",
    buildStart: () => {
      const directory = join("public", "scripts")
      const file = "all.zip"
      const fullFile = join(directory, file)
      if (existsSync(fullFile)) {
        rmSync(fullFile)
      }
      execSync(
        `cd ${directory} && zip ${file} ` +
          readdirSync(directory, { recursive: true })
            .filter((x) => x !== "main.py")
            .join(" ")
      )
      console.log(`✨ Rebuilt ${file} for Code Battles (PyScript)`)
    },
  }
}
