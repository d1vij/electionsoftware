import path from "node:path";
import { SqliteProvider } from "@/server/db/providers";

import {
    RegistrationLocalFileStorageRepository,
    RegistrationSqliteDatabaseRepository,
} from "@/server/modules/registration/repositories";
import { ElectionsSqliteDatabaseRepository } from "./modules/elections/repositories";
import { UserAuthorizationSqliteDatabaseRepository } from "./modules/user_authorization/repositories";

import type { IDatabaseProvider } from "@/server/db";
import { LocalFileStorageProvider } from "./filestorage/providers/LocalFileStorageProvider";

const DATABASE_TYPE = "sqlite";
const FILESYSTEM_TYPE = "local";

// -----------------------------------------------------
// DATABASE PROVIDERS
export const sqliteProvider = new SqliteProvider(path.join(import.meta.dir, "..", "..", "data/app.db"));

// FILESTORAGE PROVIDERS
export const localFileStorageProvider = new LocalFileStorageProvider(
    path.join(import.meta.dir, "..", "..", "data/files"),
);

// -----------------------------------------------------
// REPOSITORIES
export const registrationDatabaseRepository =
    DATABASE_TYPE === "sqlite"
        ? new RegistrationSqliteDatabaseRepository(sqliteProvider.getInstance())
        : new RegistrationSqliteDatabaseRepository(sqliteProvider.getInstance());
export const registrationFileStorageRepository =
    FILESYSTEM_TYPE === "local"
        ? new RegistrationLocalFileStorageRepository(localFileStorageProvider)
        : new RegistrationLocalFileStorageRepository(localFileStorageProvider);

export const electionsDatabaseRepository =
    DATABASE_TYPE === "sqlite"
        ? new ElectionsSqliteDatabaseRepository(sqliteProvider.getInstance())
        : new ElectionsSqliteDatabaseRepository(sqliteProvider.getInstance());

export const userAuthorizationDatabaseRepository =
    DATABASE_TYPE === "sqlite"
        ? new UserAuthorizationSqliteDatabaseRepository(sqliteProvider.getInstance())
        : new UserAuthorizationSqliteDatabaseRepository(sqliteProvider.getInstance());

// -----------------------------------------------------
// DATABASE
export const databaseProvider: IDatabaseProvider<unknown> =
    DATABASE_TYPE === "sqlite" ? sqliteProvider : sqliteProvider;
