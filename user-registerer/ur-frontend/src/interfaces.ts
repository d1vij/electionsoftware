/** @d1vij 6/7/25 */
export interface IPostData {
    name: string,
    candidates: ICandidate[]
}

export interface ICandidate {
    name: string,
    candidateId: string //candidate id is there to reference this candidate with its corresponding image
}