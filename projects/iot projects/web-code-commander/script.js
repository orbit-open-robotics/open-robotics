const BROKER = "broker.hivemq.com";
const PORT = 8884;               // WSS port
const TOPIC_TX_BASE = "orbit_pico/code";    // laptop → Pico
const TOPIC_RX_BASE = "orbit_pico/response";  // Pico → laptop

const clientId = "webclient_" + Math.random().toString(16).slice(2, 8);
const client = new Paho.Client(BROKER, PORT, clientId);
let topicRx = TOPIC_RX_BASE

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

// --- Send code ---
function sendCode() {
    const name = document.getElementById("name-input").value.trim();
    const code = document.getElementById("code").value.trim();
    if (!code) { log("Nothing to send."); return; }

    // Save name to localStorage for next time
    localStorage.setItem("picoName", name);

     // Reset client subscription to listen for this Pico's response
    if (topicRx) {
        client.unsubscribe(topicRx);
    }
    topicRx = TOPIC_RX_BASE + "/" + name;
    client.subscribe(topicRx);
    log("Subscribed to " + topicRx + " for response");

    // Warn if payload might be too large for umqtt.simple
    if (code.length > 2000) {
        log("Warning: payload is large (" + code.length + " bytes) — Pico may struggle to receive it.");
    }

    const message = new Paho.Message(code);
    message.destinationName = TOPIC_TX_BASE + "/" + name;
    client.send(message);
    log("Sent " + code.length + " bytes to + ${name}");
}

function setStatus(type, text) {
    const el = document.getElementById("status");
    el.className = type;
    el.textContent = text;
}

// Load saved Pico name from localStorage
const picoName = localStorage.getItem("picoName");
if (picoName) {
    document.getElementById("name-input").value = picoName;
}

// --- Start ---
connect();