import { CodeBattles } from "code-battles-components"
import "code-battles-components/styles.css"
import config from "./firebase.json"

const App = () => {
  return (
    <CodeBattles
      configuration={{
        firebase: config,
        maps: ["NYC"],
        runningCountOptions: [10, 100, 1000],
      }}
      routes={{}}
    />
  )
}

export default App
