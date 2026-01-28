import { t } from "elysia";

const Candidate = t.Object({
    candidate_name: t.String(),
    candidate_id: t.String(),
});
export type TCandidate = typeof Candidate.static;

const UpdationType = t.Union([
    // Status would be updated if any of the candidates are also updated
    // this includes candiate deletion, creation, updation
    t.Literal("updated"),
    t.Literal("created"),
    t.Literal("deleted"),
    t.Literal("as-is"),
]);

const CandidateImage = t.File({
    type: "image/*",
    maxSize: "25m",
});
export type TCandidateImage = typeof CandidateImage.static;

const CandidateUpdation = t.Intersect([
    Candidate,
    t.Object({
        status: UpdationType,
        candidate_image: t.Optional(CandidateImage),
    }),
]);

export type TCandidateUpdation = typeof CandidateUpdation.static;

export const PostwiseCandidatesUpdation = t.Object({
    post_id: t.String(),
    post_name: t.String(),
    status: UpdationType,

    candidates: t.Array(CandidateUpdation),
});

export type TPostwiseCandidatesUpdation =
    typeof PostwiseCandidatesUpdation.static;

export const PostwiseCandidates = t.Object({
    post_id: t.String(),
    post_name: t.String(),
    candidates: t.Array(Candidate),
});

export type TPostwiseCandidates = typeof PostwiseCandidates.static;
