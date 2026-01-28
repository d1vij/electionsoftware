import type { TPostwiseCandidates } from "../types";

export interface IDatabaseRepository {
    getAllPostwiseCandidates(): Promise<TPostwiseCandidates[]>;

    updatePostName(post_id: string, post_name: string): Promise<void>;
    deletePost(post_id: string): Promise<{ post_id: string }>;
    createPost(post_id: string, post_name: string): Promise<void>;

    updateCandidate(candidate_id: string, candidate_name: string): Promise<void>;
    createCandidate(candidate_id: string, post_id: string, candidate_name: string): Promise<void>;
    deleteCandidate(candidate_id: string): Promise<void>;
}
