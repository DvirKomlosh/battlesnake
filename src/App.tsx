import { CodeBattles } from "code-battles-components"
import config from "./firebase.json"

const App = () => {
  return (
    <CodeBattles
      configuration={{
        firebase: config,
        maps: ["NYC"],
        players: {
          hufflepuff: "iDG5e1exULVbW548MLdzVPoK35B2",
          ravenclaw: "pDFLAWny18RZyV3wdm17QDyLJ9N2",
          slytherin: "vhCOsaiWqCN6R3Rn00CJb6sHhnW2",
          gryffindor: "08rJmicETybFUuBeCKx7iJtOgvo2",
        },
      }}
      routes={{}}
    />
  )
}

export default App
