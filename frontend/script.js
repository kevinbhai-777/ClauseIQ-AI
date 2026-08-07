// ============================================
// CLAUSEIQ
// Frontend JavaScript
// ============================================


// ===============================
// Elements
// ===============================

// API URL - tries multiple common ports if default fails
const API_BASE_URL = (() => {
    // Try current origin first
    if (window.location.origin && window.location.origin !== "null") {
        return window.location.origin;
    }
    // Fallback to localhost:8000 (default backend port)
    return "http://127.0.0.1:8000";
})();

console.log("API Base URL:", API_BASE_URL);

const fileInput = document.getElementById("fileInput");

const fileName = document.getElementById("fileName");

const analyzeBtn = document.getElementById("analyzeBtn");

const loading = document.getElementById("loading");


const summary = document.getElementById("summary");

const risks = document.getElementById("risks");

const obligations = document.getElementById("obligations");

const recommendations = document.getElementById("recommendations");


const askBtn = document.getElementById("askBtn");

const question = document.getElementById("question");

const answer = document.getElementById("answer");



// ============================================
// Display Selected Filename
// ============================================


fileInput.addEventListener("change", () => {


    if(fileInput.files.length > 0){


        fileName.innerHTML =
            "📄 " + fileInput.files[0].name;


    }
    else{


        fileName.innerHTML =
            "No file selected";


    }


});



// ============================================
// Analyze Contract
// ============================================


analyzeBtn.addEventListener("click", async () => {



    if(fileInput.files.length === 0){


        alert("Please upload a PDF contract.");


        return;


    }



    loading.style.display = "block";


    analyzeBtn.disabled = true;


    analyzeBtn.innerHTML =
        "Analyzing...";



    const formData = new FormData();



    formData.append(
        "file",
        fileInput.files[0]
    );



    try{


        const response = await fetch(

            `${API_BASE_URL}/analyze`,

            {

                method:"POST",

                body:formData

            }

        );



        const data = await response.json();


        if(!response.ok || data.error){

            throw new Error(data.error || "Server Error");

        }



        parseAnalysis(data.analysis);



    }



    catch(error){



        const errorMsg = error.message || "Unable to connect to backend.";

        summary.innerHTML =
            `❌ ${errorMsg}`;



        risks.innerHTML = "-";

        obligations.innerHTML = "-";

        recommendations.innerHTML = "-";



        console.error(error);



    }



    loading.style.display = "none";



    analyzeBtn.disabled = false;



    analyzeBtn.innerHTML =

        '<i class="fa-solid fa-magnifying-glass"></i> Analyze Contract';



});



// ============================================
// Parse Gemini Response
// ============================================


function parseAnalysis(text){



    summary.innerHTML = "";

    risks.innerHTML = "";

    obligations.innerHTML = "";

    recommendations.innerHTML = "";



    const lines = text.split("\n");



    let current = "";



    lines.forEach(line => {



        const upper = line.toUpperCase();



        if(upper.includes("SUMMARY")){


            current = "summary";


            return;


        }



        if(upper.includes("RISK")){


            current = "risks";


            return;


        }



        if(upper.includes("OBLIGATION")){


            current = "obligations";


            return;


        }



        if(upper.includes("RECOMMEND")){


            current = "recommendations";


            return;


        }




        if(current === "summary"){


            summary.innerHTML +=
                line + "<br>";


        }



        if(current === "risks"){


            risks.innerHTML +=
                line + "<br>";


        }



        if(current === "obligations"){


            obligations.innerHTML +=
                line + "<br>";


        }



        if(current === "recommendations"){


            recommendations.innerHTML +=
                line + "<br>";


        }



    });



}



// ============================================
// Ask Contract
// ============================================


askBtn.addEventListener("click", async()=>{



    if(question.value.trim() === ""){


        alert(
            "Please enter a question."
        );


        return;


    }



    answer.innerHTML =
        "Thinking...";



    try{


        const response = await fetch(


            `${API_BASE_URL}/ask`,


            {


                method:"POST",



                headers:{


                    "Content-Type":
                    "application/json"


                },



                body:JSON.stringify({



                    question:
                    question.value



                })



            }



        );



        const data =
            await response.json();


        if(!response.ok || data.error){
            throw new Error(data.error || "Server Error");
        }



        answer.innerHTML =
            data.answer;



    }



    catch(error){



        answer.innerHTML =
            "Unable to connect to AI.";



    }



});



// ============================================
// Smooth Reveal Animation
// ============================================


const observer = new IntersectionObserver(
(entries)=>{


    entries.forEach(entry=>{



        if(entry.isIntersecting){



            entry.target.style.opacity = "1";



            entry.target.style.transform =
                "translateY(0)";



        }



    });



});



document
.querySelectorAll(
    ".card,.feature,.upload-card,.chat-card"
)
.forEach(el=>{



    el.style.opacity = "0";



    el.style.transform =
        "translateY(40px)";



    el.style.transition =
        ".7s";



    observer.observe(el);



});