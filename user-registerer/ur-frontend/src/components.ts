/** @d1vij 6/7/25 */
import {
    updatePreviewImage,
    deletePost_EventListener,
    deleteCandidate_EventListener,
    addPostButton_EventListener,
    addCandidateButton_EventListener,
    submitButton_EventListener
} from "./eventlisteners"


export async function createCreatePostButton(parent: HTMLElement) {
    const _createPostButton = document.createElement("button");
    _createPostButton.classList.add("create-post-button");
    _createPostButton.addEventListener("click", addPostButton_EventListener);
    _createPostButton.innerText = "Create new Post";

    parent.append(_createPostButton);

    return _createPostButton;
}

export async function createPostDiv(parent: HTMLElement, id: string): Promise<HTMLDivElement> {
    const _postDivElm = document.createElement("div");
    _postDivElm.classList.add("post-div")
    _postDivElm.setAttribute("data-post-id", id);

    parent.appendChild(_postDivElm);

    return _postDivElm;
}

export async function createPostTitle(parent: HTMLDivElement, predefined?: string): Promise<HTMLHeadingElement> {
    const _title = document.createElement("h2");
    _title.classList.add("post-title");
    _title.innerText = predefined || "";

    parent.appendChild(_title);

    return _title;
}

export async function createCandidateList(parent: HTMLDivElement, id: string): Promise<HTMLOListElement> {
    const _candidateListElm = document.createElement("ol");
    _candidateListElm.classList.add("candidate-list");
    _candidateListElm.setAttribute("data-post-id", id);

    _candidateListElm.addEventListener("click", deleteCandidate_EventListener);

    parent.appendChild(_candidateListElm);

    return _candidateListElm;
}

export async function createCandidateEntry(parent: HTMLOListElement, id: string, name: string): Promise<HTMLLIElement> {

    const _candidateListItemElm = document.createElement("li");
    _candidateListItemElm.classList.add("candidate-list-item");
    _candidateListItemElm.setAttribute("data-candidate-id", id);
    _candidateListItemElm.innerHTML =
        `
            <span class="candidate-row">
                <p class="candidate-name">${name}</p>
                <img class="candidate-preview-image" data-candidate-id="${id}">
                <input class="image-input" type="file" accept=".png, .jpeg" name="${id}">
                <button class="candidate-delete-button" data-candidate-id="${id}">Delete Candidate</button>
            </span>
        `
    _candidateListItemElm.querySelector<HTMLInputElement>("input.image-input")?.addEventListener("change", updatePreviewImage);
    _candidateListItemElm.querySelector<HTMLButtonElement>("button.candidate-delete-button")?.addEventListener("click", deleteCandidate_EventListener);

    parent.appendChild(_candidateListItemElm);
    return _candidateListItemElm;
}


export async function createAddCandidateButton(parent: HTMLDivElement, id: string) {
    const _addCandidateButton = document.createElement("button");
    _addCandidateButton.classList.add('add-candidate-button');
    _addCandidateButton.setAttribute('data-post-id', id);
    _addCandidateButton.innerText = "Add Candidate"

    _addCandidateButton.addEventListener("click", addCandidateButton_EventListener);


    parent.append(_addCandidateButton);

}

export async function createPostDeleteButton(parent: HTMLDivElement, id: string) {
    const _postDelButton = document.createElement("button");
    _postDelButton.classList.add('post-delete-button'); // TODO: Add this event listener
    _postDelButton.setAttribute('data-post-id', id);
    _postDelButton.innerText = "Delete Post"
    _postDelButton.addEventListener("click", deletePost_EventListener)


    parent.append(_postDelButton);

}

export async function createSubmitButton(parent: HTMLDivElement) {
    const _submitButton = document.createElement("button");
    _submitButton.classList.add("submit-button");
    _submitButton.innerText = "Submit";
    _submitButton.addEventListener("click", submitButton_EventListener);
    parent.appendChild(_submitButton);

    return _submitButton;
}


