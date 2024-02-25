import { Box } from "@mui/material";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import { MqttClient } from "mqtt";
import { useState } from "react";
import { CROSSINGID } from "../utils/connect_mqtt";

export default function Lookouts({ client }: { client: MqttClient }) {
  const [westFar, setWestFar] = useState<boolean>(false);
  const [westNear, setWestNear] = useState<boolean>(false);
  const [eastFar, setEastFar] = useState<boolean>(false);
  const [eastNear, setEastNear] = useState<boolean>(false);

  client.on("message", function (topic, message) {
    if (topic === `${CROSSINGID}/lookouts/west/far`) {
      setWestFar(message.toString() === "1");
    }
    if (topic === `${CROSSINGID}/lookouts/west/near`) {
      setWestNear(message.toString() === "1");
    }
    if (topic === `${CROSSINGID}/lookouts/east/far`) {
      setEastFar(message.toString() === "1");
    }
    if (topic === `${CROSSINGID}/lookouts/east/near`) {
      setEastNear(message.toString() === "1");
    }
  });

  return (
    <>
      <Grid item xs={12}>
        <Box>
          <Typography sx={{ fontWeight: "bold", fontSize: "1.5em" }}>
            Lookouts
          </Typography>
        </Box>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card sx={{ backgroundColor: westFar ? "green" : null }}>
          <CardContent>
            <Typography sx={{ fontSize: 30 }} color="text.primary" gutterBottom>
              West Far
            </Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              status
            </Typography>
            <Typography sx={{ fontSize: "1.5em" }}>
              {westFar ? "detected" : "not detected"}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card sx={{ backgroundColor: westNear ? "green" : null }}>
          <CardContent>
            <Typography sx={{ fontSize: 30 }} color="text.primary" gutterBottom>
              West Near
            </Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              status
            </Typography>
            <Typography sx={{ fontSize: "1.5em" }}>
              {westNear ? "detected" : "not detected"}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card sx={{ backgroundColor: eastFar ? "green" : null }}>
          <CardContent>
            <Typography sx={{ fontSize: 30 }} color="text.primary" gutterBottom>
              East Far
            </Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              status
            </Typography>
            <Typography sx={{ fontSize: "1.5em" }}>
              {eastFar ? "detected" : "not detected"}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card sx={{ backgroundColor: eastNear ? "green" : null }}>
          <CardContent>
            <Typography sx={{ fontSize: 30 }} color="text.primary" gutterBottom>
              East Near
            </Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              status
            </Typography>
            <Typography sx={{ fontSize: "1.5em" }}>
              {eastNear ? "detected" : "not detected"}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
    </>
  );
}
