import { execSync } from "child_process"
import {
  existsSync,
  readdirSync,
  readFileSync,
  writeFileSync,
  rmSync,
  cpSync,
} from "fs"
import { join } from "path"
import { chdir } from "process"
import type { Plugin } from "vite"

const refresh = () => {
  chdir(__dirname)
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

    const slashPath = file.toString().replace(/\\/g, "/")
    config.files["/scripts/" + slashPath] = "./" + slashPath
  }
  writeFileSync(file, JSON.stringify(config, null, 4))
  console.log("✨ Refreshed config.json to include all Python files")
}

const copyPythonLibrary = () => {
  chdir(__dirname)
  const directory = join("public", "scripts")
  const pythonLibraryPath = join(directory, "code_battles")

  if (existsSync(pythonLibraryPath)) {
    rmSync(pythonLibraryPath, { recursive: true, force: true })
  }
  cpSync(
    join("node_modules", "code-battles-components", "dist", "code_battles"),
    pythonLibraryPath,
    { recursive: true }
  )
  writeFileSync(join(pythonLibraryPath, ".gitignore"), "*")
  console.log("✨ Copied the current code_battles python library code")
}

const buildAPIDocumentation = () => {
  chdir(join(__dirname, "public", "scripts"))
  execSync(
    `pdoc api.py --no-show-source -t ${join(
      "..",
      "..",
      "node_modules",
      "code-battles-components",
      "dist",
      "pdoc-template"
    )} -o ..`
  )
  rmSync(join("..", "index.html"))
  rmSync(join("..", "search.js"))
  console.log("✨ Refreshed generated API documentation")
}

let copyingPythonLibrary = false

export default function CodeBattles(): Plugin {
  return {
    name: "code-battles",
    buildStart() {
      copyPythonLibrary()
      buildAPIDocumentation()
      refresh()
    },
    configureServer(server) {
      server.watcher.add([
        "public/scripts/*.py",
        "node_modules/code-battles-components/dist/code_battles/*.py",
      ])
      server.watcher.on("add", handleFileChange)
      server.watcher.on("change", handleFileChange)
      server.watcher.on("unlink", handleFileChange)

      function handleFileChange(file: string) {
        if (
          file.includes("public/scripts") &&
          file.endsWith(".py") &&
          !copyingPythonLibrary
        ) {
          refresh()
        }

        if (
          file.includes(
            "node_modules/code-battles-components/dist/code_battles"
          ) &&
          file.endsWith(".py")
        ) {
          copyingPythonLibrary = true
          copyPythonLibrary()
          copyingPythonLibrary = false
        }

        server.ws.send({ type: "full-reload" })
      }
    },
  }
}
