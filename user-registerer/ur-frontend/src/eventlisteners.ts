/** @d1vij 6/7/25 */
import type {IPostData, ICandidate} from "./interfaces.ts"
import uuid4 from "uuid4";

import {
    createCandidateEntry,
    createCandidateList,
    createAddCandidateButton,
    createPostDeleteButton,
    createPostDiv,
    createPostTitle,
} from "./components.ts"

import {
    _overlayContentDiv,
    _postsDiv,
    toggleOverlayVisibility,
    getImageUri,
    sendToServer,
    _overlayDiv,
    _contentDiv
} from "./main"

export async function addPostButton_EventListener() { //for post-create-button
    toggleOverlayVisibility();

    _overlayContentDiv.innerHTML = `
    <h1>Create new post</h1>
    <label for="post-title">
        Post Title
        <input id="post-title" type="text" placeholder="head_boy" required>
    </label>
    <button id='create-post'>Create</button>
    `
    document.getElementById("create-post")?.addEventListener('click', async () => {
        toggleOverlayVisibility();

        const POST_ID = uuid4()
        const title = document.querySelector<HTMLInputElement>("input#post-title")!.value;

        if (title === "") {
            alert("Input valid title");
            return;
        }

        const POST_DIV = await createPostDiv(_postsDiv, POST_ID);

        await Promise.all([createPostTitle(POST_DIV, title),
            createCandidateList(POST_DIV, POST_ID),
            createAddCandidateButton(POST_DIV, POST_ID),
            createPostDeleteButton(POST_DIV, POST_ID)
        ])
    })
}

export async function addCandidateButton_EventListener(event: Event) { //for add-candidate-button
    toggleOverlayVisibility();

    console.log("add candidate");

    const target = event.target as HTMLButtonElement;
    const corresponding_POST_ID = target.getAttribute("data-post-id")!;
    const corresponding_CandidateList = document.querySelector<HTMLOListElement>(`ol[data-post-id="${corresponding_POST_ID}"`)!;

    _overlayContentDiv.innerHTML = `
        <h1>Add new Candidate</h1>
        <label for="candidate-name">
            Candidate Name
            <input id="candidate-name" type="text" placeholder="Divij Verma" required>
        </label>
        <button id='create-image'>Create</button>
    `
    document.querySelector<HTMLButtonElement>("button#create-image")?.addEventListener('click', async () => {
        toggleOverlayVisibility();
        const name = document.querySelector<HTMLInputElement>("input#candidate-name")!.value;
        createCandidateEntry(corresponding_CandidateList, uuid4(), name);
    })

}

export async function deleteCandidate_EventListener(event: Event) {
    event.stopPropagation();

    const target = event.target as HTMLButtonElement;
    const targetId = target.getAttribute("data-candidate-id");

    document.querySelector(`li[data-candidate-id="${targetId}"]`)?.remove();
}

export async function deletePost_EventListener(event: Event) {
    event.stopPropagation()

    const target = event.target as HTMLButtonElement;
    const targetId = target.getAttribute("data-post-id");

    document.querySelector(`div[data-post-id="${targetId}"]`)?.remove();
}


export async function submitButton_EventListener(event: Event) {
    //TODO: Directly send images to server rather than image url
    // ~image urls bloat payload

    event.stopPropagation();

    let postsData: IPostData[] = [];
    let imagesFormdata = new FormData();

    console.log("Parsing started");
    document.querySelectorAll<HTMLDivElement>("div.post-div").forEach(post => {
        let candidates_array: ICandidate[] = []

        post.querySelectorAll<HTMLLIElement>("li.candidate-list-item").forEach(candidate => {
            const candidateImageInput = candidate.querySelector<HTMLInputElement>("input.image-input")!;
            imagesFormdata.append(candidateImageInput?.name, candidateImageInput.files![0])

            candidates_array.push({
                name: candidate.querySelector<HTMLParagraphElement>("p.candidate-name")!.innerText,
                candidateId: candidateImageInput.name
            })
        })

        postsData.push({
            name: post.querySelector<HTMLHeadingElement>("h2.post-title")!.innerText,
            candidates: candidates_array
        });
    })
    console.log("parsing ended");

    const candidateGroup = document.querySelector<HTMLInputElement>("input#candidate-group")!.value;
    if(candidateGroup === "") {
        alert("Choose a candidate group!!!");
        return;
    }
    
    await sendToServer(imagesFormdata,candidateGroup, postsData);
}

export async function updatePreviewImage(event: Event) {
    const target = event.target as HTMLInputElement;
    const candidateId = target.name;
    const previewElement = document.querySelector<HTMLImageElement>(`img[data-candidate-id="${candidateId}"]`)!;
    previewElement.src = await getImageUri(target.files![0]);

}
