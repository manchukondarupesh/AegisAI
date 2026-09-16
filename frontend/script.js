async function askAgent() {

    const question = document.getElementById("question").value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    const responseBox = document.getElementById("response");

    responseBox.innerHTML = "Thinking...";

    try {

        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error("Server returned " + response.status);
        }

        const data = await response.json();

        console.log("AegisAI Backend Response:", data);

        let answerText;

 if (Array.isArray(data.answer)) {

    if (data.answer.length === 0) {
        answerText = "No matching records found.";
    } else {
        answerText = data.answer
            .map(row => row.join(" | "))
            .join("\n");
    }

} else {

    answerText = String(data.answer);

}

        responseBox.innerHTML = `
            <strong>Agent:</strong> ${data.agent}<br><br>

            <strong>Answer:</strong>
            <pre>${answerText}</pre>
        `;

    } catch (error) {

        console.error("AegisAI Error:", error);

        responseBox.innerHTML = `
            <strong>Error:</strong><br>
            Unable to connect to AegisAI backend.
        `;
    }
}


async function loadDashboard() {

    try {

        const response = await fetch("http://127.0.0.1:8000/dashboard");

        const data = await response.json();
        const droneResponse = await fetch(
    "http://127.0.0.1:8000/drones"
);
const missionResponse = await fetch(
    "http://127.0.0.1:8000/missions"
);

const missionData = await missionResponse.json();

const missionTableBody =
    document.getElementById("mission-table-body");

missionTableBody.innerHTML = "";

missionData.missions.forEach(mission => {

    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${mission[0]}</td>
        <td>${mission[1]}</td>
        <td>${mission[2]}</td>
        <td>${mission[3]}</td>
        <td>${mission[4]}</td>
    `;

    missionTableBody.appendChild(row);
});

const droneData = await droneResponse.json();

const tableBody = document.getElementById("drone-table-body");

tableBody.innerHTML = "";

droneData.drones.forEach(drone => {

    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${drone[0]}</td>
        <td>${drone[1]}</td>
        <td>${drone[2]}</td>
        <td>${drone[3]}%</td>
        <td>${drone[4]}°C</td>
        <td>${drone[5]}</td>
    `;

    tableBody.appendChild(row);
});
// Load telemetry data

const telemetryResponse = await fetch(
    "http://127.0.0.1:8000/telemetry"
);

const telemetryData = await telemetryResponse.json();

const telemetryTableBody =
    document.getElementById("telemetry-table-body");

telemetryTableBody.innerHTML = "";

telemetryData.telemetry.forEach(telemetry => {

    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${telemetry[0]}</td>
        <td>${telemetry[1]}</td>
        <td>${telemetry[2]}</td>
        <td>${telemetry[3]}%</td>
        <td>${telemetry[4]}°C</td>
        <td>${telemetry[5]}%</td>
    `;

    telemetryTableBody.appendChild(row);
});
const alertList = document.getElementById("alert-list");

alertList.innerHTML = "";

if (data.high_alerts.length === 0) {

    alertList.innerHTML = "<p>No high-severity alerts.</p>";

} else {

    data.high_alerts.forEach(alert => {

        const alertItem = document.createElement("div");

        alertItem.className = "alert-item";

        alertItem.innerHTML = `
            <strong>⚠️ ${alert[1]} — ${alert[2]}</strong>
            <p>Drone: ${alert[0]}</p>
            <p>${alert[3]}</p>
        `;

        alertList.appendChild(alertItem);
    });
}

        document.getElementById("drone-status").innerText =
            data.total_drones + " drones monitored";

        if (data.low_battery.length > 0) {

            const drone = data.low_battery[0];

            document.getElementById("battery-status").innerText =
                drone[0] + ": " + drone[1] + "% ⚠️";

        } else {

            document.getElementById("battery-status").innerText =
                "All batteries normal";
        }


        if (data.high_temperature.length > 0) {

            const drone = data.high_temperature[0];

            document.getElementById("temperature-status").innerText =
                drone[0] + ": " + drone[1] + "°C ⚠️";

        } else {

            document.getElementById("temperature-status").innerText =
                "All temperatures normal";
        }


        document.getElementById("alert-status").innerText =
            data.high_alerts.length + " HIGH severity alerts";

    } catch (error) {

        console.error("Dashboard error:", error);

        document.getElementById("drone-status").innerText =
            "Unable to load data";
    }
}


loadDashboard();