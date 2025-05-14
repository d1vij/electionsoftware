// always compile to js
var token: string;

interface VoteRequest {
    token: string
    vote_data: Object[]
}

interface Status {
    status: string
}


class Utils {
    static BASE_URL = "" // add backend url if any
    static PASSWORD_HASH = "bae35f2615069b212f493f0d5f57d2af94b1c2ad9fbee222f4f96b8d4eaa34db" //divij
    static IMG_PATH = "public/img/"
    static EXT = '.png'
    static ENDPOINTS = {
        candidates: `${Utils.BASE_URL}/getcandidates`,
        token: `${Utils.BASE_URL}/gettoken`,
        voteapp: `${Utils.BASE_URL}/voteapp`,
        subtmitvotes: `${Utils.BASE_URL}/submitvotes`
    }

    static async sha256(message: string) {
        //bad of js to not have a default hashing library or function
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
    static normalize(str: String) {
        return (str.charAt(0).toUpperCase() + str.substring(1)).replace('_', ' ');
    }
}

function toggleVisibility() {
    loginDiv.classList.toggle("hidden");
    votingDiv.classList.toggle("hidden");
}

function getObjArrayFromFormData(e: FormData): Object[] {
    /*
    converts form data into array of objects of format
    [
        {
          "name": "divij",
          "post": "head_boy"
        },
        {
          "name": "abc",
          "post": "head_girl"
        }
      ]
     */

    let arr: Object[] = []
    e.forEach((name, post) => { // value, key isntead of key, value
        arr.push({
            "name": name,
            "post": post
        })
    })
    return arr
}

async function setupPage() {
    console.assert((!loginDiv.classList.contains("hidden")) && (votingDiv.classList.contains("hidden")), "Incorrect initial class to login and or voting container");

    const res = await fetch(Utils.ENDPOINTS.candidates);
    const candidateData = await res.json();

    // setting up content inside vote form
    for (const post in candidateData) {
        const candidates = candidateData[post];

        const candidatesRow = document.createElement("div"); // all candidates for same post in a common row div
        const postTitle = document.createElement("h1");

        postTitle.classList.add("post-title");
        postTitle.textContent = Utils.normalize(post); // TODO: Work on normalize function

        candidatesRow.classList.add("candidates-row")
        candidatesRow.append(postTitle);

        for (const name of candidates) {
            const id = post + name;
            const currCandidateDiv = document.createElement("div");
            currCandidateDiv.classList.add("candidate");

            const currCandidateRadio = document.createElement("input");
            currCandidateRadio.setAttribute("type", "radio");
            currCandidateRadio.setAttribute("name", post);
            currCandidateRadio.setAttribute("value", name);
            currCandidateRadio.setAttribute("id", id);


            const candidate_name = document.createElement("span");
            candidate_name.textContent = name;

            const candidate_img = document.createElement("img");
            candidate_img.setAttribute("src", Utils.IMG_PATH + encodeURIComponent(name) + Utils.EXT);

            const l = document.createElement("label");
            l.setAttribute("for", id);
            l.classList.add("candidate-label");
            l.append(candidate_img)
            l.append(candidate_name)


            currCandidateDiv.append(currCandidateRadio);
            currCandidateDiv.append(l);
            candidatesRow.append(currCandidateDiv);
        }

        voteForm.append(candidatesRow);
    }

    const sb = document.createElement("button");
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

        let data: VoteRequest = {
            token: token,
            vote_data: getObjArrayFromFormData(formData)

        }
        console.log(data)
        const response = await fetch(Utils.ENDPOINTS.subtmitvotes, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result: Status = await response.json();
        if (result.status == "success") {
            voteResolution("Voted successfully!")
            toggleVisibility();
            voteForm.reset();
        }
        else {
            voteResolution(`Vote Failed : ${result.status} `, true)
            console.log(result.status)
            throw new Error("Vote processing failed");
        }

    } catch (err) {
        console.log("Error : ", err);
    }
}

function voteResolution(message: string, e = false) {
    resolutionHeader.textContent = message
    e ? resolutionHeader.classList.add("error") : resolutionHeader.classList.remove("error");
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
        voteResolution("");
        toggleVisibility();
    } else {
        console.log("Incorrect passwrod", pe.value)
    }
}

const loginDiv = document.getElementById("login_container")!;
const votingDiv = document.getElementById("voting_container")!;
const voteForm = document.getElementById("vote_form")! as HTMLFormElement;
const resolutionHeader = document.getElementById("resolution") as HTMLHeadingElement



window.addEventListener("load", setupPage);
voteForm.addEventListener("submit", submitVote);
document.getElementById("submit_password")?.addEventListener("click", loadVoting);




