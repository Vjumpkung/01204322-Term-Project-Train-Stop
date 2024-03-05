import mqtt from "mqtt";

const MQTT_BROKER = import.meta.env.VITE_MQTT_BROKER;
const PORT = import.meta.env.VITE_PORT;
const USERNAME = import.meta.env.VITE_USERNAME;
const PASS = import.meta.env.VITE_PASS;
export const CROSSINGID = import.meta.env.VITE_CROSSINGID;
import { toast, Bounce } from "react-toastify";

const trainclient = mqtt.connect(`wss://${MQTT_BROKER}:${PORT}`, {
  username: USERNAME,
  password: PASS,
  keepalive: 60000,
  clientId: CROSSINGID + "_frontend" + Math.random().toString(16),
});

trainclient.on("connect", () => {
  console.log(`Connected to ${MQTT_BROKER}:${PORT}`);
  toast.success(`🚀 MQTT Broker Connected`, {
    position: "bottom-right",
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
    theme: "colored",
    transition: Bounce,
  });
});

trainclient.stream.on("error", (error) => {
  console.log(`Error: ${error}`);
  toast.error(`🚨 ${error}`, {
    position: "bottom-right",
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
    theme: "light",
    transition: Bounce,
  });
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
