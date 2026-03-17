
const client = new Paho.Client("broker.hivemq.com", 8884, "webclient_" + Math.random());

client.connect({
    useSSL: true,
    onSuccess: () => document.getElementById("status").textContent = "Connected"
});

function send() {
    const text = document.getElementById("msg").value;
    const message = new Paho.Message(text);
    message.destinationName = "mypico/inbox";
    client.send(message);
}
