import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Switch from "@mui/material/Switch";
import Grid from "@mui/material/Grid";
import { useState } from "react";
import { MqttClient } from "mqtt";
import trainclient from "./utils/connect_mqtt";
import Lookouts from "./components/lookouts";
import State from "./components/state";
import Gates from "./components/gates";
import { Typography } from "@mui/material";

function App() {
  const [client] = useState<MqttClient>(trainclient);
  const [isAuto, setIsAuto] = useState<boolean>(true);

  client.on("message", function (topic, message) {
    if (topic === "crossing1/mode") {
      setIsAuto(message.toString() === "A");
    }
  });

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
        <Grid item xs={12}>
          <Box sx={{ marginTop: "1em" }}>
            <Typography sx={{ fontWeight: "bold", fontSize: "1.5em" }}>
              Mode
            </Typography>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Box>
            <Switch
              checked={isAuto}
              onChange={(event) => {
                client.publish(
                  "crossing1/mode",
                  event.target.checked ? "A" : "M"
                );
              }}
              size="medium"
            />
            <span style={{ fontWeight: "bold" }}>
              {isAuto ? "Auto" : "Manual"}
            </span>
          </Box>
        </Grid>
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
