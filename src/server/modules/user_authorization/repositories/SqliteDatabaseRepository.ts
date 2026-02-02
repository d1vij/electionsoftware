import type { Database } from "bun:sqlite";
import type { IDatabaseRepository } from "./IDatabaseRepository";
import type { TUUID } from "../../common/types";

export class SqliteDatabaseRepository implements IDatabaseRepository {
    public db: Database;
    public constructor(db: Database) {
        this.db = db;
    }

    public async fetchPasswordHash(identifier: string): Promise<string | null> {
        const results = this.db
            .query<{ password_hash: string }, [string]>(
                "SELECT password_hash FROM authorizeed_users WHERE identifier = ?",
            )
            .get(identifier);

        return results?.password_hash ?? null;
    }

    public async createNewUser(user_id: TUUID, identifier: string, password_hash: string): Promise<void> {
        this.db
            .query<[], [string, string, string]>(
                "INSERT INTO authorizeed_users(id, identifier, password_hash) values(?, ?, ?)",
            )
            .run(user_id, identifier, password_hash);
    }

    public async getUserId(identifier: string): Promise<TUUID | null> {
        const results = this.db
            .query<{ id: TUUID }, [string]>("SELECT id FROM authorizeed_users WHERE identifier = ?")
            .get(identifier);

        return results?.id ?? null;
    }
}
