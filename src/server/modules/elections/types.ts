import { t } from "elysia";
import { UUID } from "@/server/modules/common/types";

export const VoteSubmission = t.Record(UUID, UUID);
export type TVoteSubmission = typeof VoteSubmission.static;

export const CreateSessionBody = t.Object({
    invoker_id: UUID,
});

export const CreateSessionResponse = t.Union([
    CreateSessionBody,
    t.Object({
        session_id: UUID,
    }),
]);
