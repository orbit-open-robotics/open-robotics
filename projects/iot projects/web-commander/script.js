
const BROKER = "broker.hivemq.com";
const PORT = 8884;
const TOPIC_TX_BASE = "orbit_pico/command";    // web → Pico
const TOPIC_RX_BASE = "orbit_pico/response";  // Pico → web

const clientId = "web_commander_" + Math.random().toString(16).slice(2, 8);
const client = new Paho.Client(BROKER, PORT, clientId);
let topicRx = TOPIC_RX_BASE;  // Will subscribe to specific Pico's response topic after sending command

// --- Logging ---
function log(msg) {
    const div = document.getElementById("log");
    const time = new Date().toLocaleTimeString();
    div.innerHTML += `<div>[${time}] ${msg}</div>`;
    div.scrollTop = div.scrollHeight;
}

function clearLog() {
    document.getElementById("log").innerHTML = "";
}

// --- MQTT callbacks ---
client.onConnectionLost = (res) => {
    setStatus("disconnected", "Disconnected: " + res.errorMessage);
    document.getElementById("send-btn").disabled = true;
    log("Connection lost — retrying in 5s...");
    setTimeout(connect, 5000);
};

client.onMessageArrived = (message) => {
    log("Pico says: " + message.payloadString);
};

// --- Connect ---
function connect() {
    log("Connecting to broker...");
    client.connect({
        useSSL: true,
        onSuccess: () => {
            setStatus("connected", "Connected to broker");
            document.getElementById("send-btn").disabled = false;
            client.subscribe(topicRx);
            log("Connected! Subscribed to " + topicRx);
        },
        onFailure: (err) => {
            log("Connection failed: " + err.errorMessage);
            setTimeout(connect, 5000);
        }
    });
}

function sendCommand() {
    const name = document.getElementById("name-input").value.trim();
    const command = document.getElementById("command-input").value.trim();
    if (!name || !command) { log("Name and command are required."); return; }

    // Reset client subscription to listen for this Pico's response
    if (topicRx) {
        client.unsubscribe(topicRx);
    }
    topicRx = TOPIC_RX_BASE + "/" + name;
    client.subscribe(topicRx);
    log("Subscribed to " + topicRx + " for response");

    const message = new Paho.Message(command);
    message.destinationName = TOPIC_TX_BASE + "/" + name;  // Send to specific Pico
    client.send(message);
    log(`Sent command to ${name}: "${command}"`);
    setStatus("sent", "Command sent to Pico");
}

function setStatus(type, text) {
    const el = document.getElementById("status");
    el.className = type;
    el.textContent = text;
}

// --- Start ---
connect();
