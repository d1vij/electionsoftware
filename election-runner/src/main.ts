/** @d1vij */
import { Utils,getObjArrayFromFormData } from "./utils.js";

var token: string;

interface IVoteRequest {
    token: string
    vote_data: Object[]
}
interface IStatus {
    status: string
}
interface IPostData {
    name:string,
    candidates:ICandidate[]
}
interface ICandidate {
    name:string,
    candidateId:string
}

type TCandidateData = IPostData[]

/**
 * Static directory
 * /public/candidate-data/images/ + candidateuuid + ext -> for candidate image
 * /public/candidate-data/x -> for candidate data
 * /public/data/password_hash.json -> contains password hash
 **/

function toggleVisibility() {
    loginDiv.classList.toggle("hidden");
    votingDiv.classList.toggle("hidden");
}

async function fetchCandidateData(): Promise<TCandidateData>{
    //prompts for candidate group and fetches it from server 
    try{
        let _userPrompt = prompt("Candidate Group?");
        if(_userPrompt===""){
            alert("Input a valid candidate group");
            return fetchCandidateData();
        }

        const response = await fetch(`/public/candidate-data/${_userPrompt}.json`);
        if(!response.ok) {
            alert(`cannot find candidate group : ${_userPrompt}`);
            return fetchCandidateData();
        }
        return await response.json();
    }catch(err){
        alert(err);
    }
    
    return fetchCandidateData()
}

async function setup() {
    console.assert((!loginDiv.classList.contains("hidden")) && (votingDiv.classList.contains("hidden")), "Incorrect initial class to login and or voting container");
    let response = await fetch("/password-hash")
    Utils.PASSWORD_HASH = (await response.json()).password_hash || "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4";

    const candidateData = await fetchCandidateData()

    // setting up content inside vote form
    for (const post of candidateData) {
        const postTitle = document.createElement("h1");

        postTitle.classList.add("post-title");
        postTitle.textContent = post.name;

        const candidatesRow = document.createElement("div");
        candidatesRow.classList.add("candidates-row")
        candidatesRow.appendChild(postTitle);

        for (const candidate of post.candidates) {

            const currCandidateDiv = document.createElement("div");
            currCandidateDiv.classList.add("candidate");

            /**
             * For arrangement of child nodes in candidate div, input radio 'must' be a sibling of label containing candidate image and name span
             * */
            currCandidateDiv.innerHTML =
                `
                <input type="radio" name="${post.name}" value="${candidate.name}" id="${candidate.candidateId}">  
                <label class="candidate-label" for="${candidate.candidateId}">
                    <img src="/public/candidate-data/images/${candidate.candidateId}.png" alt="Image-for-${candidate.name}">
                    <span>${candidate.name}</span>
                </label>
                `
            candidatesRow.append(currCandidateDiv);
        }

        voteForm.append(candidatesRow);
    }

    const sb = document.createElement("button");
    sb.disabled = true
    sb.setAttribute("type", "submit");
    sb.setAttribute("id", "submit_button");
    sb.textContent = "Submit Vote";
    voteForm.append(sb)
    console.log("Setup done");
}

async function submitVote(event: Event) {
    try {
        event.preventDefault();

        //disabling the submit button once pressed
        (document.getElementById("submit_button") as HTMLButtonElement)!.disabled = true
        const form = event.target as HTMLFormElement;
        const formData = new FormData(form);

        let data: IVoteRequest = {
            token: token,
            vote_data: getObjArrayFromFormData(formData)

        }
        console.log(data)
        const response = await fetch(Utils.ENDPOINTS.submitvotes, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result: IStatus = await response.json();
        if (result.status == "success") {
            setVoteResolution("Voted successfully!")
            toggleVisibility();
            voteForm.reset();
        }
        else {
            setVoteResolution(`Vote Failed : ${result.status} `, true)
            console.log(result.status)
            throw new Error("Vote processing failed");
        }

    } catch (err) {
        console.log("Error : ", err);
    }
}

function setVoteResolution(message: string, errorOccured = false) {
    resolutionHeader.textContent = message
    errorOccured ? resolutionHeader.classList.add("error") : resolutionHeader.classList.remove("error");
}


async function loadVoting() {
    const pe = document.getElementById("password") as HTMLInputElement
    const phash = await Utils.sha256(pe.value);
    if (phash === Utils.PASSWORD_HASH) {
        const tResponse = await fetch(Utils.ENDPOINTS.token);
        token = (await tResponse.json()).token;

        //DEBUG
        console.log(token);
        (document.getElementById("submit_button") as HTMLButtonElement).disabled = false
        pe.value = "";
        setVoteResolution("");
        toggleVisibility();
    } else {
        console.log("Incorrect passwrod", pe.value)
    }
}




const loginDiv = document.getElementById("login_container")!;
const votingDiv = document.getElementById("voting_container")!;
const voteForm = document.getElementById("vote_form")! as HTMLFormElement;
const resolutionHeader = document.getElementById("resolution") as HTMLHeadingElement



window.addEventListener("load", setup);
voteForm.addEventListener("submit", submitVote);
document.getElementById("submit_password")?.addEventListener("click", loadVoting);




