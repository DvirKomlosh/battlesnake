import { CodeBattles } from "code-battles-components"
import config from "./firebase.json"

const App = () => {
  return (
    <CodeBattles
      configuration={{
        firebase: config,
        maps: ["NYC"],
        players: {
          dvir_test: "2vTkhAGBxpZ4RlEMWOWBDL5koNI3",
          itay: "lfASCvdrzuOFe4Xo3SsNxDqmWAu2",
          alon: "KbwxEBS3eiegeLraBHAcaWOYESw1",
          tommy: "ZF0t5sZ89jTs70KhTAVCWNFrajJ3",
          gal: "6pTPA6UjecWv37n7TgW8avgiTio2",
        },
      }}
      routes={{}}
    />
  )
}

export default App
