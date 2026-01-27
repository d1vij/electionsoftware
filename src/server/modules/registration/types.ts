import { t } from "elysia";

const UpdationType = t.Union([
    t.Literal("updated"),
    t.Literal("created"),
    t.Literal("deleted"),
    t.Literal("as-is"),
]);

export const PostwiseCandidatesUpdation = t.Object({
    post_id: t.String(),
    post_name: t.String(),
    status: UpdationType,

    candidates: t.Array(
        t.Object({
            candidate_id: t.String(),
            candidate_name: t.String(),
            status: UpdationType,
        }),
    ),
});
export type TPostwiseCandidatesUpdation = typeof PostwiseCandidatesUpdation.static;

export const PostwiseCandidates = t.Object({
    post_id: t.String(),
    post_name: t.String(),
    candidates: t.Array(
        t.Object({
            candidate_id: t.String(),
            candidate_name: t.String(),
        }),
    ),
});

export type TPostwiseCandidates = typeof PostwiseCandidates.static;
