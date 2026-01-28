import type { Database } from "bun:sqlite";
import { getAllPostwiseCandidatesSqlite } from "@/server/modules/common/getAllPostwiseCandidatesSqlite";
import type { TPostwiseCandidates } from "@/server/modules/registration/types";
import type { IDatabaseRepository } from "./IDatabaseRepository";
import type { TUUID } from "../../common/types";
import type { TVoteSubmission } from "../types";

export class SqliteDatabaseRepository implements IDatabaseRepository {
    private db: Database;
    public constructor(db: Database) {
        this.db = db;
    }

    public async getAllPostwiseCandidates(): Promise<TPostwiseCandidates[]> {
        return await getAllPostwiseCandidatesSqlite(this.db);
    }

    public async insertVote(session_id: TUUID, votes: TVoteSubmission): Promise<void> {
        const jsonString = JSON.stringify(votes);
        this.db
            .query<[], [string, string]>("INSERT INTO votes(session_id, votes) VALUES(?, ?)")
            .run(session_id, jsonString);
    }

    public async insertVoteSessionUUID(invoker_id: TUUID, session_id: TUUID): Promise<void> {
        this.db
            .query<[], [string, string]>("INSERT INTO sessions(invoker_id, session_id) VALUES (?, ?)")
            .run(invoker_id, session_id);
    }
}
