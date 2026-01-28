import { Database } from "bun:sqlite";

import type { IDatabaseProvider } from "..";
import type { VoidPromise } from "../../types";

export class SqliteProvider implements IDatabaseProvider<Database> {
    private db;
    public constructor(filepath: string) {
        this.db = new Database(filepath, {
            create: false,
            strict: true,
        });
    }

    public async connect(): VoidPromise {
        this.db.run("PRAGMA journal_mode = WAL;");
        this.db.run("PRAGMA foreign_keys = ON;");
        this.db.query("SELECT 1").get();
    }
    public async disconnect(): VoidPromise {
        this.db.close();
    }
    public async ping(): VoidPromise {}

    public getInstance(): Database {
        return this.db;
    }
}
