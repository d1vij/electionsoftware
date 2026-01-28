import type { Database } from "bun:sqlite";
import type { TPostwiseCandidates } from "../registration/types";

export async function getAllPostwiseCandidatesSqlite(db: Database): Promise<TPostwiseCandidates[]> {
    const posts = db.query<{ post_id: string; post_name: string }, []>(`select post_id, post_name from posts`).all();

    const postwiseCandidates: TPostwiseCandidates[] = [];

    const candidateQuery = db.query<
        {
            candidate_id: string;
            candidate_name: string;
        },
        { post_id: string }
    >(`select candidate_name, candidate_id from candidates where post_id = $post_id`);
    for (const row of posts) {
        const candidates = candidateQuery.all({
            post_id: row.post_id,
        });

        postwiseCandidates.push({
            post_id: row.post_id,
            post_name: row.post_name,
            candidates: candidates,
        });
    }

    return postwiseCandidates;
}
