import { CodeBattles } from "code-battles"
import "code-battles/styles.css"
import config from "./firebase.json"

const App = () => {
  return (
    <CodeBattles
      configuration={{
        firebase: config,
        parameters: { map: ["NYC"] },
        parameterIcons: { map: "fa-solid fa-globe-americas" },
        runningCountOptions: [10, 100, 1000],
      }}
      routes={{}}
    />
  )
}

export default App
