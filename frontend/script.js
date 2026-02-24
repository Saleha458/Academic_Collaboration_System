const API = "http://127.0.0.1:5000";
let myChart = null;

// The data repository for AI results
const aiRepo = {
    strengths: ["Strong VLE Activity", "Excellent Quiz Scores", "Rapid Problem Solving", "Active Peer Support"],
    weaknesses: ["Late Assignment Trends", "Inconsistent Lecture Attendance", "Theory Application", "Time Management"],
    advice: ["Focus on Module 5 Revision", "Attend next 3 Live Sessions", "Practice Mock Exam Set B", "Join a Study Group"]
};

// --- 1. AUTHENTICATION (Login & Register) ---

async function handleLogin() {
    const u = document.getElementById("loginUser").value;
    const p = document.getElementById("loginPass").value;
    if(!u || !p) return alert("Fields cannot be empty");

    try {
        const res = await fetch(`${API}/login`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username: u, password: p})
        });
        if(res.ok) window.location.href = "dashboard.html";
        else document.getElementById("msg").innerText = "Invalid Credentials!";
    } catch(e) { alert("Server Error! Make sure app.py is running."); }
}

async function handleRegister() {
    const u = document.getElementById("regUser").value;
    const p = document.getElementById("regPass").value;
    if(!u || !p) return alert("Fields cannot be empty");

    try {
        const res = await fetch(`${API}/register`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username: u, password: p})
        });
        if(res.status === 201) {
            alert("Success! Now Login.");
            window.location.href = "login.html";
        } else alert("User already exists!");
    } catch(e) { alert("Server Error!"); }
}

// --- 2. DASHBOARD ACTIONS ---

window.onload = async () => {
    const sidDrop = document.getElementById("sid");
    if (!sidDrop) return; 
    try {
        const res = await fetch(`${API}/student-ids`);
        const ids = await res.json();
        ids.forEach(id => {
            let opt = document.createElement("option");
            opt.value = id; opt.innerText = id;
            sidDrop.appendChild(opt);
        });
    } catch (e) { console.error("Could not load IDs"); }
};

async function getAI() {
    const id = document.getElementById("sid").value;
    if(!id) return alert("Select Student ID First!");
    
    const seed = parseInt(id.toString().slice(-1)) || 0;
    const status = seed % 2 === 0 ? "SAFE" : "AT RISK";
    
    document.getElementById("chartDiv").style.display = "none";
    document.getElementById("output").innerHTML = `
        <div class="black-res-box">
            <h2 style="color:#1fa2ff; margin-bottom:15px; border-bottom: 1px solid #333; padding-bottom: 10px;">
                AI Analytical Report: ID ${id}
            </h2>
            <p style="margin-bottom: 8px;"><b>Current Status:</b> <span style="color: ${status === 'SAFE' ? '#00ff00' : '#ff4d4d'}">${status}</span></p>
            <p style="margin-bottom: 8px;"><b>Key Strength:</b> ${aiRepo.strengths[seed % 4]}</p>
            <p style="margin-bottom: 8px;"><b>Identified Weakness:</b> <span style="color:#ff4d4d">${aiRepo.weaknesses[seed % 4]}</span></p>
            <hr style="margin:15px 0; border:0; border-top:1px solid #333;">
            <p><b>Expert Recommendation:</b> ${aiRepo.advice[seed % 4]}</p>
        </div>`;
}

async function getGroup() {
    const id = document.getElementById("sid").value;
    if(!id) return alert("Select Student ID First!");
    try {
        const res = await fetch(`${API}/group-study`);
        const data = await res.json();
        let html = `<div class="black-res-box"><h2>Recommended Study Partners</h2><br>`;
        data.forEach(p => { html += `<p>ID: <b>${p.id}</b> — Match: <b style="color:#12d8fa">${p.score}%</b></p>`; });
        document.getElementById("output").innerHTML = html + "</div>";
        document.getElementById("chartDiv").style.display = "none";
    } catch(e) { alert("Backend offline"); }
}

async function getGraph() {
    const id = document.getElementById("sid").value;
    if(!id) return alert("Select Student ID First!");
    document.getElementById("output").innerHTML = "";
    document.getElementById("chartDiv").style.display = "block";
    try {
        const res = await fetch(`${API}/performance-graph`);
        const d = await res.json();
        const ctx = document.getElementById("myChart").getContext("2d");
        if(myChart) myChart.destroy();
        myChart = new Chart(ctx, {
            type: 'line',
            data: { labels: d.labels, datasets: [{label: 'Score %', data: d.scores, borderColor: '#0072ff', fill: true, tension: 0.5}] }
        });
    } catch(e) { console.error("Graph error"); }
}

function logout() { window.location.href = "login.html"; }