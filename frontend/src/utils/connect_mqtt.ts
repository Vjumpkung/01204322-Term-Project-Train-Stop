import mqtt from "mqtt";

const MQTT_BROKER = import.meta.env.VITE_MQTT_BROKER;
const PORT = import.meta.env.VITE_PORT;
const USERNAME = import.meta.env.VITE_USERNAME;
const PASS = import.meta.env.VITE_PASS;
const CROSSINGID = import.meta.env.VITE_CROSSINGID;

const trainclient = mqtt.connect(`mqtt://${MQTT_BROKER}:${PORT}`, {
  username: USERNAME,
  password: PASS,
  keepalive: 60000,
  clientId: CROSSINGID,
});

trainclient.on("connect", () => {
  console.log(`Connected to ${MQTT_BROKER}:${PORT}`);
});

trainclient.subscribe(`${CROSSINGID}/lookouts/west/far`);
trainclient.subscribe(`${CROSSINGID}/lookouts/west/near`);
trainclient.subscribe(`${CROSSINGID}/lookouts/east/far`);
trainclient.subscribe(`${CROSSINGID}/lookouts/east/near`);
trainclient.subscribe(`${CROSSINGID}/state`);
trainclient.subscribe(`${CROSSINGID}/gates/north`);
trainclient.subscribe(`${CROSSINGID}/gates/south`);
trainclient.subscribe(`${CROSSINGID}/mode`);

export default trainclient;
