import type { TPostwiseCandidates } from "../types";

export interface RegistrationRepository {
    getAllCandidatesPostwise(): Promise<TPostwiseCandidates[]>;
    updateCandidates(posts: TPostwiseCandidates[]): Promise<void>;
}
