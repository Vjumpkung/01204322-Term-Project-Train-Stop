import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import { MqttClient } from "mqtt";
import { useState } from "react";

export default function Lookouts({ client }: { client: MqttClient }) {
  const [westFar, setWestFar] = useState<boolean>(false);
  const [westNear, setWestNear] = useState<boolean>(false);
  const [eastFar, setEastFar] = useState<boolean>(false);
  const [eastNear, setEastNear] = useState<boolean>(false);

  client.on("message", function (topic, message) {
    if (topic === "crossing1/lookouts/west/far") {
      setWestFar(message.toString() === "1");
    }
    if (topic === "crossing1/lookouts/west/near") {
      setWestNear(message.toString() === "1");
    }
    if (topic === "crossing1/lookouts/east/far") {
      setEastFar(message.toString() === "1");
    }
    if (topic === "crossing1/lookouts/east/near") {
      setEastNear(message.toString() === "1");
    }
  });

  return (
    <>
      <Grid item xs={12} sm={6} md={3}>
        <Card>
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
        <Card>
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
        <Card>
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
        <Card>
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
