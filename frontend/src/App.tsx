import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import { useState } from "react";
import { MqttClient } from "mqtt";
import trainclient from "./utils/connect_mqtt";
import Lookouts from "./components/lookouts";
import State from "./components/state";
import Gates from "./components/gates";
import { Typography } from "@mui/material";
import Mode from "./components/mode";

function App() {
  const [client] = useState<MqttClient>(trainclient);
  const [isAuto, setIsAuto] = useState<boolean>(true);

  return (
    <Container maxWidth="lg" sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Box sx={{ marginTop: "1em" }}>
            <Typography sx={{ fontWeight: "bold", fontSize: "1.75em" }}>
              01204322-Term-Project-Train-Stop
            </Typography>
          </Box>
        </Grid>
        <Mode client={client} isAuto={isAuto} setIsAuto={setIsAuto} />
        <Grid item xs={12}>
          <Box>
            <Typography sx={{ fontWeight: "bold", fontSize: "1.5em" }}>
              Lookouts
            </Typography>
          </Box>
        </Grid>
        <Lookouts client={client} />
        <Grid item xs={12}>
          <Box>
            <Typography sx={{ fontWeight: "bold", fontSize: "1.5em" }}>
              State
            </Typography>
          </Box>
        </Grid>
        <State client={client} />
        <Grid item xs={12}>
          <Box>
            <Typography sx={{ fontWeight: "bold", fontSize: "1.5em" }}>
              Gates
            </Typography>
          </Box>
        </Grid>
        <Gates client={client} isAuto={isAuto} />
      </Grid>
    </Container>
  );
}

export default App;
