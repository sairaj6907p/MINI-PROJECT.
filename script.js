let faq = {
  "What is DBMS?":["DBMS stands for Database Management System.","It manages data efficiently."],
  "What is OOP?":["OOP means Object-Oriented Programming.","It uses classes and objects."],
  "Derivative of x^2?":["Derivative of x² is 2x.","Basic calculus rule."],
  "What is SQL?":["SQL is Structured Query Language.","Used to query/manage DB."],
  "What is OS?":["OS is Operating System.","Manages hardware/software."],
  "What is Compiler?":["Compiler converts code to machine language.","Helps run programs."],
  "What is AI?":["AI is Artificial Intelligence.","Machines mimic human intelligence."],
  "How to prepare for exams?":["Make a timetable.","Revise daily & solve past papers."]
};
let answerIndex = {};

async function login(){
    let user = document.getElementById("username").value.trim();
    let pass = document.getElementById("password").value.trim();
    let role = document.getElementById("roleSelect").value;
    if(!user || !pass || !role){document.getElementById("loginError").innerText="All fields required."; return;}

    // Simple authentication via backend
    try{
        const res = await fetch("http://127.0.0.1:5000/login",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({username:user,password:pass,role:role})
        });
        const data = await res.json();
        if(data.status==="success"){
            document.getElementById("loginSection").classList.add("hidden");
            document.getElementById("dashboardSection").classList.remove("hidden");
            document.getElementById("welcomeMessage").innerText=`Welcome ${role==="1st"?"1st Year Student":"Mentor"} ${user}`;
        } else {
            document.getElementById("loginError").innerText=data.message;
        }
    } catch(err){document.getElementById("loginError").innerText="Server error.";}
}

function logout(){
    document.querySelectorAll("section,.modal").forEach(sec=>sec.classList.add("hidden"));
    document.getElementById("loginSection").classList.remove("hidden");
}

// Knowledge Hub
function openKnowledge(){document.getElementById("knowledgeHub").classList.remove("hidden");}
function closeKnowledge(){document.getElementById("knowledgeHub").classList.add("hidden");}

// Chatbot
function openChatbot(){document.getElementById("chatbotModal").classList.remove("hidden");}
function closeChatbot(){document.getElementById("chatbotModal").classList.add("hidden");}
function nextAnswer(question){if(!answerIndex[question])answerIndex[question]=0;let idx=answerIndex[question];if(idx>=faq[question].length){answerIndex[question]=0;return;}let botBox=document.getElementById("botBox");botBox.innerHTML+=`<b>Bot:</b> ${faq[question][idx]}<br>`;botBox.scrollTop=botBox.scrollHeight;answerIndex[question]++;}
async function askBot(){let input=document.getElementById("botInput");let query=input.value.trim();if(!query)return;let botBox=document.getElementById("botBox");botBox.innerHTML+=`<b>You:</b> ${query}<br>`;try{const res=await fetch("http://127.0.0.1:5000/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:query})});const data=await res.json();botBox.innerHTML+=`<b>Bot:</b> ${data.reply}<br>`;}catch(err){botBox.innerHTML+=`<b>Bot:</b> Error connecting to server.<br>`;}botBox.scrollTop=botBox.scrollHeight;}
