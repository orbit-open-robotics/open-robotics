const BROKER = "broker.hivemq.com";
const PORT = 8884;               // WSS port
const TOPIC_RX_BASE = "orbit_pico/value/";  // Pico → laptop

const clientId = "webclient_" + Math.random().toString(16).slice(2, 8);
const client = new Paho.Client(BROKER, PORT, clientId);

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
    document.getElementById("value").textContent = message.payloadString;
};

// --- Connect ---
function connect() {
    log("Connecting to broker...");
    client.connect({
        useSSL: true,
        onSuccess: () => {
            setStatus("connected", "Connected to broker");
            log("Connected! Subscribed to " + topicRx);
        },
        onFailure: (err) => {
            log("Connection failed: " + err.errorMessage);
            setTimeout(connect, 5000);
        }
    });
}

function setStatus(type, text) {
    const el = document.getElementById("status");
    el.className = type;
    el.textContent = text;
}

function updateTopic() {
    if (topicRx) {
        client.unsubscribe(TOPIC_RX_BASE + topicRx);
    }
    const topicInput = document.getElementById("topic-input");
    topicRx = topicInput.value.trim();
    localStorage.setItem("topicRx", topicRx);
    client.subscribe(TOPIC_RX_BASE + topicRx);
}


// Load saved topic from localStorage
let topicRx = localStorage.getItem("topicRx");
if (topicRx) {
    document.getElementById("topic-input").value = topicRx;
    client.subscribe(TOPIC_RX_BASE + topicRx);
}

// --- Start ---
connect();