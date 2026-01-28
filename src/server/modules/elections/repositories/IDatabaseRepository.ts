import type { TPostwiseCandidates } from "@/server/modules/registration/types";
import type { TUUID } from "@/server/modules/common/types";
import type { TVoteSubmission } from "../types";

export interface IDatabaseRepository {
    getAllPostwiseCandidates(): Promise<TPostwiseCandidates[]>;

    insertVote(session_id: TUUID, votes: TVoteSubmission): Promise<void>;
    insertVoteSessionUUID(invoker_id: TUUID, session_id: TUUID): Promise<void>
}
