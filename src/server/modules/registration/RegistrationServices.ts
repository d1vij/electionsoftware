import { file } from "elysia";
import type { IFileStorageRepository } from "./repositories/IFileStorageRepository";
import type { IDatabaseRepository } from "./repositories/IDatabaseRepository";
import type { TCandidateImage, TCandidateImageUpload, TCandidateUpdation, TPostwiseCandidatesUpdation } from "./types";
import { collapseTextChangeRangesAcrossMultipleVersions } from "typescript";

export async function getAllPostwiseCandidates(registrationRepo: IDatabaseRepository) {
    return await registrationRepo.getAllPostwiseCandidates();
}

export async function updateCandidates(
    registrationRepo: IDatabaseRepository,
    post_id: string,
    candidates: TCandidateUpdation[],
) {
    for (const candidate of candidates) {
        switch (candidate.status) {
            case "updated": {
                await Promise.all([registrationRepo.updateCandidate(candidate.candidate_id, candidate.candidate_name)]);
                break;
            }
            case "created": {
                await Promise.all([
                    registrationRepo.createCandidate(candidate.candidate_id, post_id, candidate.candidate_name),
                ]);
                break;
            }
            case "deleted": {
                await Promise.all([registrationRepo.deleteCandidate(candidate.candidate_id)]);
                break;
            }
            case "as-is":
                break;
        }
    }
}

export async function updatePosts(posts: TPostwiseCandidatesUpdation[], databaseRepo: IDatabaseRepository) {
    for (const post of posts) {
        switch (post.status) {
            case "updated": {
                await databaseRepo.updatePostName(post.post_id, post.post_name);
                break;
            }
            case "created": {
                await databaseRepo.createPost(post.post_id, post.post_name);
                break;
            }

            case "deleted": {
                await databaseRepo.deletePost(post.post_id);
                break;
            }
            case "as-is":
                break;
        }

        await updateCandidates(databaseRepo, post.post_id, post.candidates);
    }
}
export async function uploadCandidateImages(fileStorageRepo: IFileStorageRepository, imageData: TCandidateImageUpload) {
    const promises: Promise<void>[] = [];
    for (const id in imageData) {
        const image = imageData[id];
        if (image === undefined) throw new Error(`unable to get image file corresponding to id ${id}`);
        promises.push(fileStorageRepo.saveCandidateImage(image, id));
    }

    await Promise.all(promises);
}
