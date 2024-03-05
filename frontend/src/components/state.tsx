import { Box } from "@mui/material";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import { MqttClient } from "mqtt";
import { useState } from "react";
import { CROSSINGID } from "../utils/connect_mqtt";

export default function State({ client }: { client: MqttClient }) {
  const [state, setState] = useState<string>("0");

  client.on("message", function (topic, message) {
    if (topic === `${CROSSINGID}/state`) {
      setState(message.toString());
    }
  });

  return (
    <>
      <Grid item xs={12}>
        <Box>
          <Typography sx={{ fontWeight: "bold", fontSize: "1.5em" }}>
            State
          </Typography>
        </Box>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card>
          <CardContent>
            <Typography sx={{ fontSize: 30 }} color="text.primary" gutterBottom>
              State
            </Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              value
            </Typography>
            <Typography sx={{ fontSize: "1.5em" }}>{state}</Typography>
          </CardContent>
        </Card>
      </Grid>
    </>
  );
}
