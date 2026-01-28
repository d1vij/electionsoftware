import type { IFileStorageRepository } from "./repositories/IFileStorageRepository";
import type { IDatabaseRepository } from "./repositories/IRegistrationRepository";
import type { TCandidateUpdation, TPostwiseCandidatesUpdation } from "./types";

export abstract class RegistrationService {
    public static async getAllPostwiseCandidates(
        registrationRepo: IDatabaseRepository,
    ) {
        return await registrationRepo.getAllPostwiseCandidates();
    }

    private static async updateCandidates(
        registrationRepo: IDatabaseRepository,
        fileStorageRepo: IFileStorageRepository,
        post_id: string,
        candidates: TCandidateUpdation[],
    ) {
        for (const candidate of candidates) {
            switch (candidate.status) {
                case "updated": {
                    if (candidate.candidate_image === undefined) {
                        throw new Error(
                            `no image provided for ${candidate.candidate_id}`,
                        );
                    }

                    await Promise.all([
                        fileStorageRepo.saveCandidateImage(
                            candidate.candidate_image,
                            candidate.candidate_id,
                        ),
                        registrationRepo.updateCandidate(
                            candidate.candidate_id,
                            candidate.candidate_name,
                        ),
                    ]);
                    break;
                }
                case "created": {
                    if (candidate.candidate_image === undefined) {
                        throw new Error(
                            `no image provided for ${candidate.candidate_id}`,
                        );
                    }

                    await Promise.all([
                        fileStorageRepo.saveCandidateImage(
                            candidate.candidate_image,
                            candidate.candidate_id,
                        ),
                        registrationRepo.createCandidate(
                            candidate.candidate_id,
                            post_id,
                            candidate.candidate_name,
                        ),
                    ]);
                    break;
                }
                case "deleted": {
                    await Promise.all([
                        fileStorageRepo.deleteCandidateImage(
                            candidate.candidate_id,
                        ),
                        registrationRepo.deleteCandidate(
                            candidate.candidate_id,
                        ),
                    ]);
                    break;
                }
                case "as-is":
                    break;
            }
        }
    }

    public static async updatePosts(
        posts: TPostwiseCandidatesUpdation[],
        databaseRepo: IDatabaseRepository,
        fileStorageRepo: IFileStorageRepository,
    ) {
        for (const post of posts) {
            switch (post.status) {
                case "updated": {
                    await databaseRepo.updatePostName(
                        post.post_id,
                        post.post_name,
                    );
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

            await RegistrationService.updateCandidates(
                databaseRepo,
                fileStorageRepo,
                post.post_id,
                post.candidates,
            );
        }
    }
}
