/*
* possibly getting a token while sending candidate data or just sending it via another endpoint
* ensuring that even if repeated requests are sent to backend for updating votes, they are uploaded only once
* Even IF multiple create requests are sent to db, its duplicates can be checked while parsing the db objects
*
*
* using mongodb to store vote objects, instead of updating them to a sql table -> so that clashing while updating doesnt occur and
* then parsing all of it using a script
*/

// TODO: make voting div loading when login is done and not when page loads -> essentially removing hiding it with css
// TODO: add database functionality


class Utils {
    static PASSWORD_HASH = "bae35f2615069b212f493f0d5f57d2af94b1c2ad9fbee222f4f96b8d4eaa34db" //divij
    static IMG_PATH = "static/img/"
    static EXT = '.jpg'
    static ENDPOINTS = {
        candidates : "http://localhost:8000/candidates",
        voteapp : "http://localhost:8000/voteapp",
        subtmitvotes: "http://localhost:8000/submitvotes"
    }

    static async sha256(message: string) {
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
    static normalize(str: String) {
        return (str.charAt(0).toUpperCase() + str.substring(1)).replace('_', ' ');
    }
}

// @ts-ignore

const loginDiv = document.getElementById("login_container")!;
const votingDiv = document.getElementById("voting_container")!;
const voteForm   = document.getElementById("vote_form")! as HTMLFormElement;


interface VoteResponse  {
    status : string,
    votes : Record<string, string>
}

async function setupPage(){
	console.assert((!loginDiv.classList.contains("hidden")) && (votingDiv.classList.contains("hidden")),"Incorrect initial class to login and or voting container");

    const res = await fetch(Utils.ENDPOINTS.candidates);
    const candidate_data = await res.json();

    // setting up vote form
    for(const post in candidate_data){
        const candidates = candidate_data[post];

        const candidates_row = document.createElement("div");
        const title = document.createElement("h1");

        title.classList.add("post-title");
        title.textContent = Utils.normalize(post);

        candidates_row.classList.add("candidates-row")
        candidates_row.append(title);

        for(const name of candidates){
            const id = post+name;
            const currCandidateDiv = document.createElement("div");
            currCandidateDiv.classList.add("candidate");

            const currCandidateRadio = document.createElement("input");
            currCandidateRadio.setAttribute("type", "radio");
            currCandidateRadio.setAttribute("name", post);
            currCandidateRadio.setAttribute("value", name);
            currCandidateRadio.setAttribute("id",id);


            const candidate_name = document.createElement("span");
            candidate_name.textContent = name;

            const candidate_img = document.createElement("img");
            candidate_img.setAttribute("src", Utils.IMG_PATH + encodeURIComponent(name) + Utils.EXT);

            const l = document.createElement("label");
            l.setAttribute("for",id);
            l.classList.add("candidate-label");
            l.append(candidate_img)
            l.append(candidate_name)


            currCandidateDiv.append(currCandidateRadio);
            currCandidateDiv.append(l);
            candidates_row.append(currCandidateDiv);
        }

        voteForm.append(candidates_row);
    }
    const sb = document.createElement("button");
    sb.setAttribute("type", "submit");
    sb.textContent = "Submit Vote";
    voteForm.append(sb)
    console.log("Setup done");
}

async function submitVote(event : Event) {
    try{
        event.preventDefault();
        const form = event.target as HTMLFormElement;
        const formData = new FormData(form);

        const response = await fetch(Utils.ENDPOINTS.subtmitvotes, {
            method: "POST",
            body: formData
        });

        const result : VoteResponse = await response.json();
        if(result.status=="success"){
            console.log(result.votes);
            toggleVisibility();
            voteForm.reset();
        }
        else{
            throw new Error("Vote processing failed"+result.status);
        }

    } catch (err) {
        console.log("Error : ", err);
    }
}

function toggleVisibility (){
    loginDiv.classList.toggle("hidden");
    votingDiv.classList.toggle("hidden");
}

async function loadVoting(){
    const pe = document.getElementById("password") as HTMLInputElement
    const ph = await Utils.sha256(pe.value);
    if(ph === Utils.PASSWORD_HASH){
        pe.value = "";
        toggleVisibility();
    } else {
        console.log("Incorrect passwrod", pe.value)
    }
}



window.addEventListener("load", setupPage);

voteForm.addEventListener("submit", submitVote);
document.getElementById("submit_password")?.addEventListener("click", loadVoting);




