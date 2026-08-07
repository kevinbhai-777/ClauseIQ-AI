// ============================================
// CLAUSEIQ
// Frontend JavaScript
// ============================================


// ===============================
// Elements
// ===============================


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

            "http://127.0.0.1:8000/analyze",

            {

                method:"POST",

                body:formData

            }

        );



        if(!response.ok){


            throw new Error(
                "Server Error"
            );


        }



        const data = await response.json();



        parseAnalysis(data.analysis);



    }



    catch(error){



        summary.innerHTML =
            "❌ Unable to connect to backend.";



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


            "http://127.0.0.1:8000/ask",


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



        if(!response.ok){


            throw new Error();


        }



        const data =
            await response.json();



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