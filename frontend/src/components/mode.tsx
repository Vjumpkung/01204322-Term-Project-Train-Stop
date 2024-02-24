import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Switch from "@mui/material/Switch";
import { MqttClient } from "mqtt";

export default function Mode({
  client,
  isAuto,
  setIsAuto,
}: {
  client: MqttClient;
  isAuto: boolean;
  setIsAuto: (isAuto: boolean) => void;
}) {
  client.on("message", function (topic, message) {
    if (topic === "crossing1/mode") {
      setIsAuto(message.toString() === "A");
    }
  });
  return (
    <Grid container spacing={1}>
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
    </Grid>
  );
}
