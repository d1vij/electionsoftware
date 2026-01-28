import type { Database } from "bun:sqlite";
import type { TPostwiseCandidates } from "../types";
import type { IDatabaseRepository } from "./IDatabaseRepository";
import { getAllPostwiseCandidatesSqlite } from "../../common/getAllPostwiseCandidatesSqlite";

export class SqliteDatabaseRepository implements IDatabaseRepository {
    private db: Database;
    public constructor(db: Database) {
        this.db = db;
    }

    public async getAllPostwiseCandidates(): Promise<TPostwiseCandidates[]> {
        return getAllPostwiseCandidatesSqlite(this.db);
    }

    public async updatePostName(post_id: string, newName: string) {
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

    public async deletePost(post_id: string) {
        const results = this.db
            .query<{ post_id: string }, [string]>(`delete from posts where post_id = ? returning post_id`)
            .get(post_id);
        if (!results) {
            throw new Error("no post exists with id " + post_id);
        }

        return results;
    }

    public async createPost(post_id: string, post_name: string): Promise<void> {
        this.db
            .query<[], [string, string]>(`insert into posts(post_id, post_name) values(?, ?)`)
            .run(post_id, post_name);
    }

    public async updateCandidate(candidate_id: string, candidate_name: string): Promise<void> {
        this.db
            .query(
                ` update candidates
            set candidate_name = ?
            where candidate_id = ? `,
            )
            .run(candidate_name, candidate_id);
    }
    public async createCandidate(candidate_id: string, post_id: string, candidate_name: string): Promise<void> {
        this.db
            .query(
                `
                insert into candidates(candidate_id, post_id, candidate_name)
                values (?, ?, ?)
                `,
            )
            .run(candidate_id, post_id, candidate_name);
    }
    public async deleteCandidate(candidate_id: string): Promise<void> {
        this.db.query(`delete from candidates where candidate_id = ?`).run(candidate_id);
    }
}
