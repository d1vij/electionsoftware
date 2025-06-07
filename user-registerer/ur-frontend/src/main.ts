/**@d1vij*/
import {createCreatePostButton, createSubmitButton} from "./components.ts";
import type {IPostData} from "./interfaces.ts";

export const _contentDiv = document.querySelector<HTMLDivElement>("div#content")!;
export const _postsDiv = document.querySelector<HTMLDivElement>("div.posts")!;
export const _overlayDiv = document.querySelector<HTMLDivElement>("div#popup")!;
export const _overlayContentDiv = document.querySelector<HTMLDivElement>("div#popup-content")!;

async function main() {
    // let data = (await fetchExistingCandidates()) || [];
    // let data:IPostData[] = (await fetchExistingCandidates()) || [];

    await createCreatePostButton(_contentDiv);
    // await loadExistingContent(data);
    await createSubmitButton(_contentDiv);
}

export function toggleOverlayVisibility() {
    _overlayDiv.classList.toggle("visible")
}


export async function sendToServer(imagesformData: FormData, postsData: IPostData[]) {
    //images upload
    const response1 = await fetch("/post/images", {
        method: "POST",
        body: imagesformData
    })
    const {uploaded} = await response1.json();
    console.log("uploaded images "+uploaded.toString())
    alert("Image data sent!");

    const response2 = await fetch("/post/posts-data", {
        method:"POST",
        headers:{
            'Content-Type':"application/json",
        },
        body: JSON.stringify(postsData)
    })
    console.log(await response2.json());
    alert("Posts data sent!")
}

export async function getImageUri(imageFile: File): Promise<string> {
    return new Promise((resolve, reject) => {
        const filereader = new FileReader();

        filereader.onload = () => {
            resolve(filereader.result as string);
        };

        filereader.onerror = (error) => {
            reject(error);
        };
        filereader.readAsDataURL(imageFile);
    });
}
/**@----------------------------------------------------------------------------------------------->*/


main().catch(console.log);

//TODO:Work on this

// async function fetchExistingCandidates(): Promise<IPostData[]> {
//     try{
//         const response = await fetch("/candidates.json")
//         const candidate_data = await response.json() as IPostData[];
//         return candidate_data
//     }
//     catch (SyntaxError) {
//         return [];
//     }
//
// }
//
// async function loadExistingContent(data: IPostData[]) {
//     data.forEach(post => {
//         const POST_ID = uuid4();
//         const POST_DIV = createPostDiv(_postsDiv, POST_ID);
//         createPostTitle(POST_DIV, post.name);
//
//         const CANDIDATE_LIST = createCandidateList(POST_DIV, POST_ID);
//         post.candidates.forEach(candidate => {
//             createCandidateEntry(CANDIDATE_LIST, uuid4(), candidate.name, candidate.imageDataUrl);
//         })
//
//         createAddCandidateButton(POST_DIV, POST_ID);
//         createPostDeleteButton(POST_DIV, POST_ID);
//     })
// }










