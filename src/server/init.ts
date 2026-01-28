import path from "node:path";
import { SqliteProvider } from "@/server/db/providers";

import {
    LocalFileStorageRegistrationRepository,
    SqliteRegistrationDatabaseRepository,
} from "@/server/modules/registration/repositories";
import type { IDatabaseProvider } from "@/server/db";
import { LocalFileStorageProvider } from "./filestorage/providers/LocalFileStorageProvider";

const DATABASE_TYPE = "sqlite";
const FILESYSTEM_TYPE = "local";

// -----------------------------------------------------
// DATABASE PROVIDERS
export const sqliteProvider = new SqliteProvider(
    path.join(import.meta.dir, "..", "..", "data/app.db"),
);

// FILESTORAGE PROVIDERS
export const localFileStorageProvider = new LocalFileStorageProvider(
    path.join(import.meta.dir, "..", "..", "data/files"),
);

// -----------------------------------------------------
// REPOSITORIES
export const registrationDatabaseRepository =
    DATABASE_TYPE === "sqlite"
        ? new SqliteRegistrationDatabaseRepository(sqliteProvider.getInstance())
        : new SqliteRegistrationDatabaseRepository(
              sqliteProvider.getInstance(),
          );
export const registrationFileStorageRepository =
    FILESYSTEM_TYPE === "local"
        ? new LocalFileStorageRegistrationRepository(localFileStorageProvider)
        : new LocalFileStorageRegistrationRepository(localFileStorageProvider);

// -----------------------------------------------------
// DATABASE
export const databaseProvider: IDatabaseProvider<unknown> =
    DATABASE_TYPE == "sqlite" ? sqliteProvider : sqliteProvider;
