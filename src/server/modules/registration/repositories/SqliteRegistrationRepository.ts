import { Database } from "bun:sqlite";
import type { RegistrationRepository } from "./RegistrationRepository";
import type {
    TPostwiseCandidates,
    TPostwiseCandidatesUpdation,
} from "../types";

export class SqliteRegistrationRepository implements RegistrationRepository {
    private db: Database;
    public constructor(db: Database) {
        this.db = db;
    }

    public async getAllCandidatesPostwise(): Promise<TPostwiseCandidates[]> {
        const posts = this.db
            .query<
                { post_id: string; post_name: string },
                []
            >(`select post_id, post_name from posts`)
            .all();

        const postwiseCandidates: TPostwiseCandidates[] = [];

        const candidateQuery = this.db.query<
            { candidate_id: string; candidate_name: string },
            { post_id: string }
        >(
            `select candidate_name, candidate_id from candidates where post_id = $post_id`,
        );
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

    private async updatePostName(post_id: string, newName: string) {
        this.db
            .query<[], { $post_name: string; $post_id: string }>(
                `
            update posts
            set post_name = $post_name
            where post_id = $post_id
        `,
            )
            .run({ $post_name: newName, $post_id: post_id });
    }

    public async updateCandidates(
        posts: TPostwiseCandidatesUpdation[],
    ): Promise<void> {
        for (const post of posts) {
            switch (post.status) {
                case "updated": {
                    await this.updatePostName(post.post_id, post.post_name);
                    break;
                }
                case "created":
                case "deleted":
                case "as-is":
            }
        }
    }
}
