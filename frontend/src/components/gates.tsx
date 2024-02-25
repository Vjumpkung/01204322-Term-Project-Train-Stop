import { MqttClient } from "mqtt";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import { Fragment, useState } from "react";
import Switch from "@mui/material/Switch";
import Box from "@mui/material/Box";

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
    if (topic === "crossing1/gates/north") {
      setNorthGates(message.toString() === "1");
    }
    if (topic === "crossing1/gates/south") {
      setSouthGates(message.toString() === "1");
    }
  });

  return (
    <Fragment>
      <Grid item xs={12}>
        <Box>
          <Typography sx={{ fontWeight: "bold", fontSize: "1.5em" }}>
            Gates
          </Typography>
        </Box>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card>
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
                  color="secondary"
                  checked={northGates}
                  onChange={(event) => {
                    client.publish(
                      "crossing1/gates/north",
                      event.target.checked ? "1" : "0"
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
        <Card>
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
                  color="secondary"
                  checked={southGates}
                  onChange={(event) => {
                    client.publish(
                      "crossing1/gates/south",
                      event.target.checked ? "1" : "0"
                    );
                  }}
                  size="medium"
                />
              )}
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </Fragment>
  );
}
