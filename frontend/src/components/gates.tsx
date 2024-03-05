import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Grid from "@mui/material/Grid";
import Switch from "@mui/material/Switch";
import Typography from "@mui/material/Typography";
import { MqttClient } from "mqtt";
import { useState } from "react";
import { CROSSINGID } from "../utils/connect_mqtt";

export default function Gates({
  client,
  isAuto,
}: {
  client: MqttClient;
  isAuto: boolean;
}) {
  const [northGates, setNorthGates] = useState<boolean>(false);
  const [southGates, setSouthGates] = useState<boolean>(false);

  client.on("message", function (topic, message) {
    if (topic === `${CROSSINGID}/gates/north`) {
      setNorthGates(message.toString() === "1");
    }
    if (topic === `${CROSSINGID}/gates/south`) {
      setSouthGates(message.toString() === "1");
    }
  });

  return (
    <>
      <Grid item xs={12}>
        <Box>
          <Typography sx={{ fontWeight: "bold", fontSize: "1.5em" }}>
            Gates
          </Typography>
        </Box>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card
          sx={
            !isAuto
              ? { backgroundColor: `${northGates ? "green" : "red"}` }
              : null
          }
        >
          <CardContent>
            <Typography sx={{ fontSize: 30 }} color="text.primary" gutterBottom>
              North Gate
            </Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              status
            </Typography>
            <Typography sx={{ fontSize: "1.5em" }}>
              {northGates ? "open" : "close"}
            </Typography>
            <Box sx={{ textAlign: "right" }}>
              {isAuto ? null : (
                <Switch
                  color="primary"
                  checked={northGates}
                  onChange={(event) => {
                    client.publish(
                      `${CROSSINGID}/gates/north`,
                      event.target.checked ? "1" : "0",
                      { retain: true }
                    );
                  }}
                  size="medium"
                />
              )}
            </Box>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card
          sx={
            !isAuto
              ? { backgroundColor: `${southGates ? "green" : "red"}` }
              : null
          }
        >
          <CardContent>
            <Typography sx={{ fontSize: 30 }} color="text.primary" gutterBottom>
              South Gate
            </Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              status
            </Typography>
            <Typography sx={{ fontSize: "1.5em" }}>
              {southGates ? "open" : "close"}
            </Typography>
            <Box sx={{ textAlign: "right" }}>
              {isAuto ? null : (
                <Switch
                  color="primary"
                  checked={southGates}
                  onChange={(event) => {
                    client.publish(
                      `${CROSSINGID}/gates/south`,
                      event.target.checked ? "1" : "0",
                      { retain: true }
                    );
                  }}
                  size="medium"
                />
              )}
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </>
  );
}
