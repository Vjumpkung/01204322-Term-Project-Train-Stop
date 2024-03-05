import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import { MqttClient } from "mqtt";
import { useState } from "react";
import Gates from "./components/gates";
import Lookouts from "./components/lookouts";
import Mode from "./components/mode";
import State from "./components/state";
import trainclient from "./utils/connect_mqtt";

function App() {
  const [client] = useState<MqttClient>(trainclient);
  const [isAuto, setIsAuto] = useState<boolean>(true);

  return (
    <Container maxWidth="lg" sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Mode client={client} isAuto={isAuto} setIsAuto={setIsAuto} />
        <Lookouts client={client} />
        <State client={client} />
        <Gates client={client} isAuto={isAuto} />
      </Grid>
    </Container>
  );
}

export default App;
